#!/usr/bin/env bash
# Instala o refinamento no Ctrl+G do Claude Code para o usuário atual.
#
# Grava em ~/.claude/settings.json o campo env.VISUAL apontando para o
# refinar-editor. Vale para qualquer shell e terminal, e só dentro do Claude
# Code (o resto do sistema não muda). Preserva o resto do arquivo e pode rodar
# de novo sem duplicar nada.
set -euo pipefail

editor="$(cd "$(dirname "$(readlink -f "$0")")" && pwd)/refinar-editor"
chmod +x "$editor"
settings="$HOME/.claude/settings.json"
mkdir -p "$(dirname "$settings")"
[[ -f "$settings" ]] || echo '{}' > "$settings"

if command -v python3 > /dev/null; then
  python3 - "$settings" "$editor" <<'PY'
import json, sys
caminho, editor = sys.argv[1], sys.argv[2]
with open(caminho) as f:
    dados = json.load(f)
dados.setdefault("env", {})["VISUAL"] = editor
with open(caminho, "w") as f:
    json.dump(dados, f, indent=2, ensure_ascii=False)
    f.write("\n")
PY
elif command -v jq > /dev/null; then
  jq --arg e "$editor" '.env.VISUAL = $e' "$settings" > "$settings.tmp" && mv "$settings.tmp" "$settings"
else
  echo "Precisa de python3 ou jq. Ou acrescente à mão em $settings:" >&2
  echo "  \"env\": { \"VISUAL\": \"$editor\" }" >&2
  exit 1
fi

echo "env.VISUAL gravado em $settings"
echo "Abra uma sessão nova do Claude Code, digite o rascunho e aperte Ctrl+G."
