#!/usr/bin/env python3
"""Mostra o diff da branch, commit a commit e estilo VS Code, para o usuário revisar.

Uso:
    python3 diff.py <pasta-da-tarefa> --base <ref> [--fase N] [--porta N] [--host H] [--sem-abrir] [--ocioso MIN]

Pega os commits da branch que não estão em <ref> (ex.: origin/develop), sem os de merge,
do mais antigo ao mais novo, e o diff de cada um contra o pai. A página tem os commits com
os arquivos de cada um, o diff lado a lado (ou em linha) e um campo só para os
questionamentos. Ao clicar em Enviar, grava <nome>.respostas.json, imprime o texto e
encerra. <nome> é codigo-fase<N>, ou codigo sem --fase. Rode em segundo plano: o
encerramento do processo é o aviso de que o usuário respondeu.

Nunca fica mais de um servidor por <nome>: ao subir, derruba o anterior (pelo <nome>.pid).
Encerra sozinho depois de --ocioso minutos sem acesso à página (padrão 240).

Saída 0: enviado. Saída 2: erro de git (a ref não existe, fora de um repositório).
Saída 3: encerrou por ociosidade ou foi substituído, sem envio.
Só biblioteca padrão.
"""
import argparse
import json
import os
import re
import signal
import subprocess
import sys
import threading
import time
from datetime import datetime
from fnmatch import fnmatch
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

sys.dont_write_bytecode = True  # não sujar scripts/__pycache__ ao importar o revisao
sys.path.insert(0, str(Path(__file__).resolve().parent))
from revisao import abrir_navegador, gravar_json, ler_json  # noqa: E402

RAIZ = Path(__file__).resolve().parent.parent
MODELO = RAIZ / "modelos" / "diff.html"

# Arquivos gerados: aparecem na lista, mas o diff só abre se o usuário pedir.
GERADOS_NOMES = {
    "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb", "poetry.lock", "uv.lock",
    "Pipfile.lock", "Cargo.lock", "go.sum", "composer.lock", "Gemfile.lock",
}
GERADOS_GLOBS = ["*/__snapshots__/*", "*.snap", "*.min.js", "*.min.css"]
LIMITE_LINHAS = 6000
CAB_TRECHO = re.compile(r"^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@(.*)$")


def git(raiz, *args):
    return subprocess.run(
        ["git", "-C", str(raiz), *args], capture_output=True, text=True, encoding="utf-8", errors="replace"
    )


def gerado(caminho):
    return Path(caminho).name in GERADOS_NOMES or any(fnmatch(caminho, g) for g in GERADOS_GLOBS)


def arquivos_alterados(raiz, base, topo):
    partes = git(raiz, "diff", "--name-status", "-z", "-M", "--no-ext-diff", base, topo).stdout.split("\0")
    saida, i = [], 0
    while i < len(partes) and partes[i]:
        status = partes[i]
        if status[0] in "RC":
            saida.append((status[0], partes[i + 2], partes[i + 1]))
            i += 3
        else:
            saida.append((status[0], partes[i + 1], None))
            i += 2
    return saida


VAZIO = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"  # a árvore vazia do git (pai do commit raiz)


def commits_da_branch(raiz, base_ref):
    """Commits da branch fora de base_ref, sem merge, do mais antigo ao mais novo."""
    fmt = "%H%x1f%h%x1f%s%x1f%an%x1f%ad%x1f%P%x1e"
    saida = git(raiz, "log", "--no-merges", "--reverse", "--date=format:%d/%m %H:%M",
                f"--format={fmt}", f"{base_ref}..HEAD").stdout
    commits = []
    for bloco in saida.split("\x1e"):
        bloco = bloco.strip("\n")
        if not bloco:
            continue
        h, curto, titulo, autor, data, pais = bloco.split("\x1f")
        pai = pais.split()[0] if pais.split() else VAZIO
        corpo = git(raiz, "log", "-1", "--format=%b", h).stdout.strip()
        arquivos = sorted(
            (diff_do_arquivo(raiz, pai, h, s, c, a) for s, c, a in arquivos_alterados(raiz, pai, h)),
            key=lambda a: a["caminho"],
        )
        commits.append({"hash": h, "curto": curto, "titulo": titulo, "corpo": corpo, "autor": autor,
                        "data": data, "arquivos": arquivos})
    return commits


def diff_do_arquivo(raiz, base, topo, status, caminho, antigo):
    """O arquivo inteiro como contexto: a página dobra os trechos iguais."""
    caminhos = [antigo, caminho] if antigo else [caminho]
    texto = git(raiz, "diff", "--no-color", "--no-ext-diff", "-M", "-U1000000", base, topo, "--", *caminhos).stdout
    arq = {
        "caminho": caminho, "antigo": antigo, "status": status, "binario": False, "grande": False,
        "gerado": gerado(caminho), "adicionadas": 0, "removidas": 0, "linhas": [],
        "comando": f"git diff {base[:10]} {topo[:10]} -- {caminho}",
    }
    na = nb = 0
    dentro = False
    for linha in texto.splitlines():
        if linha.startswith("Binary files") or linha.startswith("GIT binary patch"):
            arq["binario"] = True
            continue
        m = CAB_TRECHO.match(linha)
        if m:
            na, nb = int(m.group(1)), int(m.group(3))
            if dentro:
                arq["linhas"].append(["h", None, None, linha])
            dentro = True
            continue
        if not dentro or not linha or linha[0] not in " +-":
            continue
        if linha[0] == "+":
            arq["linhas"].append(["a", None, nb, linha[1:]])
            arq["adicionadas"] += 1
            nb += 1
        elif linha[0] == "-":
            arq["linhas"].append(["d", na, None, linha[1:]])
            arq["removidas"] += 1
            na += 1
        else:
            arq["linhas"].append(["c", na, nb, linha[1:]])
            na += 1
            nb += 1
    if len(arq["linhas"]) > LIMITE_LINHAS:
        arq["grande"] = True
        arq["linhas"] = []
    return arq


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pasta", type=Path)
    ap.add_argument("--base", required=True, help="a branch de integração, ex.: origin/develop")
    ap.add_argument("--fase", type=int)
    ap.add_argument("--porta", type=int, default=0, help="0 = uma porta livre")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--sem-abrir", action="store_true", help="não abrir o navegador")
    ap.add_argument("--ocioso", type=float, default=240, help="minutos sem acesso até encerrar sozinho (0 = nunca)")
    args = ap.parse_args()

    pasta = args.pasta.resolve()
    pasta.mkdir(parents=True, exist_ok=True)
    nome = f"codigo-fase{args.fase}" if args.fase else "codigo"
    arq_resp = pasta / f"{nome}.respostas.json"
    arq_rasc = pasta / f"{nome}.rascunho.json"
    arq_pid = pasta / f"{nome}.pid"

    r = git(pasta, "rev-parse", "--show-toplevel")
    if r.returncode != 0:
        print(f"[trilho] {pasta} não está num repositório git", file=sys.stderr)
        sys.exit(2)
    raiz = Path(r.stdout.strip())
    r = git(raiz, "rev-parse", "--verify", "--quiet", args.base + "^{commit}")
    if r.returncode != 0:
        print(f"[trilho] {args.base} não é um commit deste repositório", file=sys.stderr)
        sys.exit(2)
    base = r.stdout.strip()
    topo = git(raiz, "rev-parse", "HEAD").stdout.strip()
    branch = git(raiz, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    pendentes = [l for l in git(raiz, "status", "--porcelain").stdout.splitlines() if not l[3:].startswith(".trilho/")]

    commits = commits_da_branch(raiz, args.base)
    tarefa = pasta.name

    # O rascunho vale mesmo com commits novos: é texto do usuário, não do diff.
    rascunho = ler_json(arq_rasc)
    if not rascunho:
        anterior = ler_json(arq_resp)
        rascunho = {"texto": anterior.get("texto", "")} if anterior and anterior.get("topo") == topo else None

    try:
        antigo = int(arq_pid.read_text().strip())
        if antigo != os.getpid():
            os.kill(antigo, signal.SIGTERM)
    except (OSError, ValueError):
        pass
    arq_pid.write_text(str(os.getpid()))

    carga = json.dumps(
        {
            "tarefa": tarefa, "nome": nome, "fase": args.fase, "branch": branch, "base_ref": args.base,
            "base": base, "topo": topo, "commits": commits, "pendentes": len(pendentes),
            "rascunho": (rascunho or {}).get("texto", ""),
        },
        ensure_ascii=False,
    ).replace("</", "<\\/")
    pagina = MODELO.read_text(encoding="utf-8").replace("__DADOS__", carga).encode("utf-8")

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

        def do_POST(self):
            try:
                n = int(self.headers.get("Content-Length") or 0)
                dados = json.loads(self.rfile.read(n).decode("utf-8") or "{}")
            except (ValueError, json.JSONDecodeError):
                self._json(400, {"ok": False, "erro": "corpo inválido"})
                return
            texto = (dados.get("texto") or "").strip()
            if self.path == "/rascunho":
                gravar_json(arq_rasc, {"topo": topo, "texto": texto})
                self._json(200, {"ok": True})
                return
            if self.path != "/enviar":
                self.send_error(404)
                return
            respostas = {
                "tarefa": tarefa, "fase": args.fase, "branch": branch, "base_ref": args.base,
                "base": base, "topo": topo, "commits": [c["curto"] for c in commits],
                "enviado_em": datetime.now().astimezone().isoformat(timespec="seconds"),
                "texto": texto,
            }
            gravar_json(arq_resp, respostas)
            if arq_rasc.exists():
                arq_rasc.unlink()
            self._json(200, {"ok": True})
            print(f"[trilho] revisão do diff gravada em {arq_resp}", flush=True)
            if texto:
                print("questionamentos do usuário:\n" + texto, flush=True)
                print("Pergunta se responde no chat antes de seguir; pedido de mudança vira tarefa.", flush=True)
            else:
                print("sem questionamentos: o usuário não tem nada a apontar no diff.", flush=True)
            fim.set()

    servidor = ThreadingHTTPServer((args.host, args.porta), Handler)
    url = f"http://localhost:{servidor.server_address[1]}/"
    extra = f"; {len(pendentes)} arquivo(s) com mudança não commitada fora do diff" if pendentes else ""
    print(f"[trilho] diff de {branch} contra {args.base} ({len(commits)} commits, sem merges) em {url} (esperando o Enviar){extra}", flush=True)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    if not args.sem_abrir:
        try:
            abrir_navegador(url)
        except OSError:
            pass

    def sair_sem_respostas(motivo):
        print(f"[trilho] {nome}: servidor encerrado sem envio ({motivo})", flush=True)
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
