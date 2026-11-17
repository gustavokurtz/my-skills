#!/usr/bin/env bash
# Põe o texto da entrada padrão no clipboard do Windows (WSL).
# UTF-16LE para os acentos não quebrarem; CRLF e sem quebra de linha no fim para colar limpo.
set -euo pipefail
texto=$(cat)
printf '%s' "${texto//$'\n'/$'\r\n'}" | iconv -f utf-8 -t utf-16le | clip.exe
