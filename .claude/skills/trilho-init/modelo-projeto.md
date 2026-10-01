# Projeto — <nome>

**Atualizado em:** AAAA-MM-DD

## Comandos

| Ação | Comando | Observação |
|---|---|---|
| Testes (todos) | `<ex: npm test>` | |
| Teste (um arquivo) | `<ex: npx vitest run caminho>` | |
| Lint | `<ex: npm run lint>` | |
| Typecheck | `<ex: npx tsc --noEmit>` | |
| Build | `<ex: npm run build>` | |

Comando inexistente: escreva `—` e diga o que usar no lugar (ex.: "sem testes; o usuário optou por não configurar; verificação alternativa por execução manual").

## Branches

- Integração: `<ex: develop>`
- Padrão de nome: `<ex: feat/<slug>>`

## Commits

Convenção encontrada no `git log`, com 2 ou 3 exemplos reais. Se o repo não tem padrão, use este:

Conventional Commits, assunto no imperativo, em português, até 72 caracteres, sem ponto final. Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`. Sem coautoria, assinatura de ferramenta ou emoji, a menos que o repo já use.

```
<tipo>(<escopo>): <o que muda>

<por que muda, se não for óbvio pelo assunto>
```

## Stack e estrutura

- Stack: …
- Onde fica cada coisa: rotas em `…`, serviços em `…`, testes em `…`

## Convenções de código

Padrões locais a seguir, cada um com um arquivo de referência.

- … (ver `caminho/exemplo.ts`)

## Regras fixas

O que vale para toda tarefa, sem exceção.

- …

## Áreas sensíveis

O que exige perguntar antes de rodar ou alterar.

- … (ex.: `npm run migrate` aponta para `DATABASE_URL`; nunca rodar contra banco remoto sem perguntar)
