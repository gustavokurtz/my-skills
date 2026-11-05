#!/usr/bin/env python3
"""Serve o discovery ou a spec de uma tarefa do trilho para o usuário responder no navegador.

Uso:
    python3 revisao.py <pasta-da-tarefa> discovery|spec [--porta N] [--host H] [--sem-abrir]

Lê <pasta>/<etapa>.json, valida, renderiza modelos/revisao.html e espera o usuário.
Cada mudança na página é salva em <etapa>.rascunho.json. Ao clicar em Enviar, grava
<etapa>.respostas.json, imprime o resumo das respostas e encerra. Rode em segundo
plano: o encerramento do processo é o aviso de que as respostas chegaram.

Nunca fica mais de um servidor por etapa: ao subir, ele derruba o anterior da mesma
pasta e etapa (pelo <etapa>.pid). E encerra sozinho depois de --ocioso minutos sem
nenhum acesso à página (padrão 240).

Saída 0: respostas gravadas. Saída 2: o JSON da etapa tem erro (a lista vai no stderr).
Saída 3: encerrou por ociosidade ou foi substituído, sem respostas.
Só biblioteca padrão.
"""
import argparse
import hashlib
import json
import os
import shutil
import signal
import subprocess
import sys
import threading
import time
import webbrowser
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MODELO = RAIZ / "modelos" / "revisao.html"

ADERENCIAS = {"bate", "parcial", "nao_bate"}
TIPOS_REQ = {"requisito", "comportamento", "restricao"}
STATUS_SPEC = {"aprovado", "ajustar", "rejeitado"}
STATUS_DECIDIDO = {"concordo", "discordo"}
STATUS_ENTENDIMENTO = {"certo", "errado"}
ID_ENTENDIMENTO = "ENT"


def hash_item(item):
    bruto = json.dumps(item, sort_keys=True, ensure_ascii=False)
    return hashlib.sha1(bruto.encode("utf-8")).hexdigest()[:12]


def itens_revisaveis(doc):
    """Itens que recebem resposta, na ordem da página."""
    if doc["etapa"] == "spec":
        return list(doc.get("requisitos", [])) + list(doc.get("fora_de_escopo", []))
    entendimento = {"id": ID_ENTENDIMENTO, "texto": doc.get("entendimento", "")}
    return [entendimento] + list(doc.get("perguntas", [])) + list(doc.get("decidido", []))


def validar(doc, etapa):
    erros = []
    if doc.get("etapa") != etapa:
        erros.append(f'"etapa" deve ser "{etapa}", veio {doc.get("etapa")!r}')
        return erros
    for campo in ("tarefa", "titulo", "versao"):
        if not doc.get(campo):
            erros.append(f'falta "{campo}"')

    vistos = {ID_ENTENDIMENTO} if etapa == "discovery" else set()

    def novo_id(item, onde):
        i = item.get("id")
        if not i:
            erros.append(f"item sem id em {onde}: {str(item)[:60]}")
        elif i in vistos:
            erros.append(f"id repetido: {i}")
        vistos.add(i)
        return i

    if etapa == "spec":
        objetivos = doc.get("objetivos") or []
        if not objetivos:
            erros.append('falta "objetivos"')
        ids_obj = {novo_id(o, "objetivos") for o in objetivos}
        reqs = doc.get("requisitos") or []
        if not reqs:
            erros.append('falta "requisitos"')
        cobertos = set()
        for r in reqs:
            i = novo_id(r, "requisitos")
            for campo in ("texto", "porque", "justificativa"):
                if not r.get(campo):
                    erros.append(f'{i}: falta "{campo}"')
            if r.get("tipo") not in TIPOS_REQ:
                erros.append(f'{i}: "tipo" deve ser um de {sorted(TIPOS_REQ)}')
            if r.get("aderencia") not in ADERENCIAS:
                erros.append(f'{i}: "aderencia" deve ser um de {sorted(ADERENCIAS)}')
            origem = r.get("origem") or []
            if not origem:
                erros.append(f'{i}: falta "origem" (ids dos objetivos)')
            for o in origem:
                if o not in ids_obj:
                    erros.append(f"{i}: origem {o} não é um objetivo")
                cobertos.add(o)
        for f in doc.get("fora_de_escopo") or []:
            i = novo_id(f, "fora_de_escopo")
            if not f.get("texto") or not f.get("porque"):
                erros.append(f'{i}: fora de escopo precisa de "texto" e "porque"')
        for o in objetivos:
            if o.get("id") not in cobertos and not o.get("lacuna"):
                erros.append(
                    f'{o.get("id")}: nenhum requisito cobre este objetivo; '
                    'cubra ou marque "lacuna" com o motivo'
                )
    else:
        if not doc.get("entendimento"):
            erros.append('falta "entendimento"')
        perguntas = doc.get("perguntas") or []
        if not perguntas:
            erros.append('falta "perguntas"')
        for p in perguntas:
            i = novo_id(p, "perguntas")
            if not p.get("pergunta"):
                erros.append(f'{i}: falta "pergunta"')
            opcoes = p.get("opcoes") or []
            if p.get("aberta"):
                continue
            if not 2 <= len(opcoes) <= 4:
                erros.append(f"{i}: precisa de 2 a 4 opções (ou \"aberta\": true)")
            ids_op = set()
            for op in opcoes:
                if not op.get("id") or not op.get("rotulo"):
                    erros.append(f'{i}: opção sem "id" ou "rotulo"')
                if op.get("id") in ids_op:
                    erros.append(f"{i}: opção repetida {op.get('id')}")
                ids_op.add(op.get("id"))
            if sum(1 for op in opcoes if op.get("recomendada")) > 1:
                erros.append(f"{i}: mais de uma opção recomendada")
        for d in doc.get("decidido") or []:
            i = novo_id(d, "decidido")
            if not d.get("texto") or not d.get("porque"):
                erros.append(f'{i}: decidido precisa de "texto" e "porque"')
    return erros


def ler_json(caminho):
    if not caminho.exists():
        return None
    try:
        return json.loads(caminho.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None


def gravar_json(caminho, dados):
    tmp = caminho.with_suffix(caminho.suffix + ".tmp")
    tmp.write_text(json.dumps(dados, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(tmp, caminho)


def resumo(doc, respostas):
    linhas = [f"[trilho] respostas do {doc['etapa']} v{doc['versao']} gravadas em {respostas['_arquivo']}"]
    itens = respostas["itens"]
    contagem = {}
    pendentes = []
    for item in itens_revisaveis(doc):
        r = itens.get(item["id"], {})
        chave = r.get("status") or ("respondida" if r.get("escolha") else "sem resposta")
        contagem[chave] = contagem.get(chave, 0) + 1
        aprovado = r.get("status") in ("aprovado", "concordo", "certo") or (
            doc["etapa"] == "discovery" and r.get("escolha") and not r.get("comentario")
        )
        if not aprovado:
            partes = [item["id"]]
            if r.get("status"):
                partes.append(r["status"])
            if r.get("escolha"):
                partes.append(f"escolha={r['escolha']}")
            if r.get("comentario"):
                partes.append(f"comentário: {r['comentario']}")
            if len(partes) == 1:
                partes.append("sem resposta")
            pendentes.append(" | ".join(partes))
    linhas.append("contagem: " + ", ".join(f"{k}={v}" for k, v in sorted(contagem.items())))
    if pendentes:
        linhas.append("itens para tratar:")
        linhas += [f"  - {p}" for p in pendentes]
    if respostas.get("geral"):
        linhas.append(f"comentário geral: {respostas['geral']}")
    linhas.append("Comentário que é pergunta: responda no chat antes de seguir.")
    return "\n".join(linhas)


def abrir_navegador(url):
    try:
        wsl = "microsoft" in Path("/proc/version").read_text().lower()
    except OSError:
        wsl = False
    if wsl:
        if shutil.which("wslview"):
            subprocess.Popen(["wslview", url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        if shutil.which("cmd.exe"):
            subprocess.Popen(
                ["cmd.exe", "/c", "start", "", url],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                cwd="/mnt/c" if Path("/mnt/c").is_dir() else None,
            )
            return
    webbrowser.open(url)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta", type=Path)
    ap.add_argument("etapa", choices=["discovery", "spec"])
    ap.add_argument("--porta", type=int, default=0, help="0 = uma porta livre")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--sem-abrir", action="store_true", help="não abrir o navegador")
    ap.add_argument("--ocioso", type=float, default=240, help="minutos sem acesso até encerrar sozinho (0 = nunca)")
    args = ap.parse_args()

    pasta = args.pasta.resolve()
    arq_doc = pasta / f"{args.etapa}.json"
    arq_resp = pasta / f"{args.etapa}.respostas.json"
    arq_rasc = pasta / f"{args.etapa}.rascunho.json"
    arq_pid = pasta / f"{args.etapa}.pid"

    if not arq_doc.exists():
        print(f"[trilho] não achei {arq_doc}", file=sys.stderr)
        sys.exit(2)
    try:
        doc = json.loads(arq_doc.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"[trilho] {arq_doc} não é JSON válido: {e}", file=sys.stderr)
        sys.exit(2)
    erros = validar(doc, args.etapa)
    if erros:
        print(f"[trilho] {arq_doc.name} tem {len(erros)} erro(s):", file=sys.stderr)
        for e in erros:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(2)

    hashes = {item["id"]: hash_item(item) for item in itens_revisaveis(doc)}
    anteriores = ler_json(arq_resp)
    if anteriores and anteriores.get("versao") == doc["versao"]:
        # Mesma versão já respondida: a página abre com essas respostas para editar.
        rascunho = {"versao": doc["versao"], "itens": anteriores.get("itens", {}), "geral": anteriores.get("geral", "")}
        anteriores = None
    else:
        rascunho = ler_json(arq_rasc)
        if rascunho and rascunho.get("versao") != doc["versao"]:
            rascunho = None

    # Derruba o servidor anterior da mesma etapa (rodada velha, sessão que caiu).
    try:
        antigo = int(arq_pid.read_text().strip())
        if antigo != os.getpid():
            os.kill(antigo, signal.SIGTERM)
    except (OSError, ValueError):
        pass
    arq_pid.write_text(str(os.getpid()))

    modelo = MODELO.read_text(encoding="utf-8")
    carga = json.dumps(
        {"doc": doc, "hashes": hashes, "anteriores": anteriores, "rascunho": rascunho},
        ensure_ascii=False,
    ).replace("</", "<\\/")
    pagina = modelo.replace("__DADOS__", carga).encode("utf-8")

    fim = threading.Event()
    ultimo_acesso = [time.monotonic()]

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *a):
            ultimo_acesso[0] = time.monotonic()

        def _json(self, codigo, dados):
            corpo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
            self.send_response(codigo)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(corpo)))
            self.end_headers()
            self.wfile.write(corpo)

        def do_GET(self):
            if self.path.split("?")[0] not in ("/", "/index.html"):
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(pagina)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(pagina)

        def _corpo(self):
            n = int(self.headers.get("Content-Length") or 0)
            return json.loads(self.rfile.read(n).decode("utf-8") or "{}")

        def do_POST(self):
            try:
                dados = self._corpo()
            except (ValueError, json.JSONDecodeError):
                self._json(400, {"ok": False, "erro": "corpo inválido"})
                return
            itens = dados.get("itens") if isinstance(dados.get("itens"), dict) else {}
            if self.path == "/rascunho":
                gravar_json(arq_rasc, {"versao": doc["versao"], "itens": itens, "geral": dados.get("geral", "")})
                self._json(200, {"ok": True})
                return
            if self.path != "/enviar":
                self.send_error(404)
                return
            # spec: todo item tem status. discovery: pergunta tem escolha; decidido tem status.
            decididos = {d["id"] for d in doc.get("decidido", [])}
            limpos = {}
            for item in itens_revisaveis(doc):
                r = itens.get(item["id"]) or {}
                if args.etapa == "spec":
                    validos = STATUS_SPEC
                elif item["id"] == ID_ENTENDIMENTO:
                    validos = STATUS_ENTENDIMENTO
                elif item["id"] in decididos:
                    validos = STATUS_DECIDIDO
                else:
                    validos = set()
                limpos[item["id"]] = {
                    "status": r.get("status") if r.get("status") in validos else None,
                    "escolha": r.get("escolha") or None,
                    "comentario": (r.get("comentario") or "").strip(),
                    "hash": hashes[item["id"]],
                }
            respostas = {
                "etapa": args.etapa,
                "tarefa": doc["tarefa"],
                "versao": doc["versao"],
                "enviado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
                "itens": limpos,
                "geral": (dados.get("geral") or "").strip(),
            }
            gravar_json(arq_resp, respostas)
            if arq_rasc.exists():
                arq_rasc.unlink()
            self._json(200, {"ok": True})
            respostas["_arquivo"] = str(arq_resp)
            print(resumo(doc, respostas), flush=True)
            fim.set()

    servidor = ThreadingHTTPServer((args.host, args.porta), Handler)
    url = f"http://localhost:{servidor.server_address[1]}/"
    print(f"[trilho] {args.etapa} v{doc['versao']} em {url} (esperando o Enviar)", flush=True)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    if not args.sem_abrir:
        try:
            abrir_navegador(url)
        except OSError:
            pass
    def sair_sem_respostas(motivo):
        print(f"[trilho] {args.etapa}: servidor encerrado sem respostas ({motivo})", flush=True)
        try:
            if arq_pid.read_text().strip() == str(os.getpid()):
                arq_pid.unlink()
        except OSError:
            pass
        os._exit(3)

    signal.signal(signal.SIGTERM, lambda *_: sair_sem_respostas("substituído ou derrubado"))
    try:
        passo = min(30.0, max(1.0, args.ocioso * 60 / 4)) if args.ocioso else 30.0
        while not fim.wait(passo):
            if args.ocioso and time.monotonic() - ultimo_acesso[0] > args.ocioso * 60:
                sair_sem_respostas(f"{args.ocioso:g} min sem acesso")
    except KeyboardInterrupt:
        sair_sem_respostas("interrompido")
    servidor.shutdown()
    try:
        arq_pid.unlink()
    except OSError:
        pass


if __name__ == "__main__":
    main()
