# Roteiro — <título da tarefa>

**Tarefa:** AAAA-MM-DD-<slug>
**Branch:** `<nome da branch>` (sai de `<integração>`)
**Entrega:** só commits na branch | push da branch | push + PR para `<integração>`

## Pedido

O que o usuário pediu, reescrito de forma clara e fiel: cada ideia, restrição, nome e número dele, com o porquê quando ele deu. Sem requisitos novos.

## Contexto no código

- `caminho/do/arquivo.ts` — o que existe hoje e por que importa para a tarefa
- Padrão a seguir: `caminho/exemplo.ts`

## Decisões

| Questão | Decisão | Porquê |
|---|---|---|
| … | … | … |
| … | … (decidido por mim) | … |

## Fora de escopo

- …

## Incertezas

O que só se descobre rodando. "nenhuma" se a tarefa é toda determinística.

- **I1** — <o que não se sabe>. Sondagem: <o experimento mais barato que responde>, em T1.

## Tarefas

<!-- Branch, push, PR e code review não entram aqui: o review roda no fim de cada fase; push e PR, na entrega. -->

### Fase 1 — <o que fica funcionando ao fim da fase>

- **T1** — <ação verificável>
  - Como: <o que fazer, em uma ou duas linhas>
  - Teste: <teste a escrever antes de implementar>
- **T2** — <ação verificável>
  - Como: …
  - Verificar por: <comando ou passo concreto> (sem teste porque <motivo>)
- **T3** — <tarefa empírica>
  - Como: …
  - Meta: <resultado mensurável>. Orçamento: <rodadas ou custo>. Se esgotar: <plano B, ou "parar e trazer ao usuário">
- **T4** — <tarefa que o usuário executa>
  - Como: …
  - Quem roda: dev (<motivo: custo de LLM, credencial, ambiente dele, prova na tela>)
  - Verificar por / Meta: …

**Fim da fase 1:** <o que deve estar verde ou demonstrável>

## Pronto quando

- <critério observável>

Validação manual (o usuário roda no final):

1. <passo> → <resultado esperado>
