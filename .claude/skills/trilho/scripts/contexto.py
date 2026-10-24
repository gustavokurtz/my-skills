#!/usr/bin/env python3
"""Hook do trilho: avisa o modelo quando o contexto da sessão fica grande.

O modelo não mede o próprio contexto e tende a se achar leve, mas a qualidade
cai com o contexto cheio, mesmo numa janela de 1M. Este hook lê o último `usage` do transcript
(input + cache_creation + cache_read, a mesma soma da statusline) e, acima dos
limites, injeta um aviso para fazer o handoff.

- aviso (TRILHO_CONTEXTO_AVISO, padrão 300000): terminar a tarefa atual e fazer o handoff;
- limite (TRILHO_CONTEXTO_LIMITE, padrão 400000): parar e fazer o handoff agora.

Para não repetir o aviso a cada tool, ele só volta depois de o contexto crescer
mais 25k desde o último aviso. Qualquer falha sai em silêncio: o hook nunca
pode atrapalhar a sessão.
"""
import json
import os
import sys
import tempfile

AVISO = int(os.environ.get("TRILHO_CONTEXTO_AVISO", "300000"))
LIMITE = int(os.environ.get("TRILHO_CONTEXTO_LIMITE", "400000"))
REPETE_A_CADA = 25000
CAUDA = 512 * 1024


def tokens_do_contexto(caminho):
    with open(caminho, "rb") as f:
        f.seek(0, os.SEEK_END)
        f.seek(max(0, f.tell() - CAUDA))
        linhas = f.read().decode("utf-8", "ignore").splitlines()
    for linha in reversed(linhas):
        try:
            j = json.loads(linha)
        except ValueError:
            continue
        if j.get("type") != "assistant" or j.get("isSidechain"):
            continue
        u = (j.get("message") or {}).get("usage") or {}
        total = (
            u.get("input_tokens", 0)
            + u.get("cache_creation_input_tokens", 0)
            + u.get("cache_read_input_tokens", 0)
        )
        if total:
            return total
    return 0


def main():
    entrada = json.load(sys.stdin)
    if entrada.get("agent_id"):
        return  # subagente: o contexto dele não é o da sessão
    tokens = tokens_do_contexto(entrada["transcript_path"])
    if tokens < AVISO:
        return

    marca = os.path.join(
        tempfile.gettempdir(), f"trilho-contexto-{entrada.get('session_id', 'x')}"
    )
    try:
        with open(marca) as f:
            ultimo = int(f.read().strip() or 0)
    except (OSError, ValueError):
        ultimo = 0
    if ultimo and tokens - ultimo < REPETE_A_CADA:
        return
    with open(marca, "w") as f:
        f.write(str(tokens))

    k = f"{tokens // 1000}k"
    if tokens >= LIMITE:
        texto = (
            f"[trilho] contexto em {k} tokens, acima do limite de {LIMITE // 1000}k: "
            "a qualidade já está caindo. Pare agora, sem começar nada novo: deixe o "
            "código num ponto commitável (ou registre o que está pela metade), faça o "
            "handoff (referencias/handoff.md) e peça o /clear ao usuário."
        )
    else:
        texto = (
            f"[trilho] contexto em {k} tokens (aviso em {AVISO // 1000}k). Termine a "
            "tarefa em andamento, sem abrir outra, e faça o handoff "
            "(referencias/handoff.md) pedindo o /clear ao usuário. Se estiver no meio "
            "de uma rodada empírica ou esperando o dev, faça o handoff assim que a "
            "rodada fechar."
        )
    evento = entrada.get("hook_event_name", "PostToolUse")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": evento, "additionalContext": texto}}))


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
