# Projeto — <nome>

**Atualizado em:** AAAA-MM-DD

## Comandos

| Ação | Comando | Quando rodar | Observação |
|---|---|---|---|
| Testes (todos) | `<ex: npm test>` | fim de fase e entrega, se entrou código de produção depois da última vez que passou | leva ~<N> min (medido em AAAA-MM-DD) |
| Teste (um arquivo) | `<ex: npx vitest run caminho>` | a cada tarefa; na entrega, quando só mudou o que não é produção | |
| Lint | `<ex: npm run lint>` | fim de fase e entrega | |
| Typecheck | `<ex: npx tsc --noEmit>` | fim de fase e entrega | |
| Build | `<ex: npm run build>` | entrega | |

A coluna "Quando rodar" é decisão do usuário e vence o padrão do trilho. Quando ele corrigir quando um comando roda, atualize a coluna.

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

## Armadilhas

O que já deu errado neste projeto e como evitar. Começa vazia; as tarefas do trilho acrescentam na entrega.

- nenhuma
