# Plano — <título da tarefa>

**Tarefa:** AAAA-MM-DD-<slug>
**Branch:** `<nome da branch>` (sai de `<integração>`)
**Spec:** `spec.json` v<N>, aprovada em AAAA-MM-DD (respostas em `spec.respostas.json`)
**Entrega:** só commits na branch | push da branch | push + PR para `<integração>`

<!-- O quê e o porquê estão na spec aprovada. Este arquivo é só o como. -->

## Contexto no código

- `caminho/do/arquivo.ts` — o que existe hoje e por que importa para a tarefa
- Padrão a seguir: `caminho/exemplo.ts`
- Em bug, a causa nos dois níveis: imediata (`arquivo:linha`) e de desenho

## Decisões

As do discovery (com a resposta do usuário) e as técnicas que eu tomei, cada uma com o porquê.

| Questão | Decisão | Porquê |
|---|---|---|
| … | … (discovery, P1) | … |
| … | … (decidido por mim) | … |

## Incertezas

O que só se descobre rodando. "nenhuma" se a tarefa é toda determinística.

- **I1** — <o que não se sabe>. Sondagem: <o experimento mais barato que responde>, em T1.

## Tarefas

<!-- Branch, push, PR e code review não entram aqui: o review roda no fim de cada fase; push e PR, na entrega.
     Todo requisito aprovado da spec aparece em pelo menos um "Atende:". -->

### Fase 1 — <o que fica funcionando ao fim da fase>

- **T1** — <ação verificável>
  - Atende: R1
  - Como: <o que fazer, em uma ou duas linhas>
  - Teste: <teste a escrever antes de implementar>
- **T2** — <ação verificável>
  - Atende: R2
  - Como: …
  - Verificar por: <comando ou passo concreto> (sem teste porque <motivo>)
- **T3** — <tarefa empírica>
  - Atende: R3
  - Como: …
  - Meta: <resultado mensurável>. Orçamento: <rodadas ou custo>. Se esgotar: <plano B, ou "parar e trazer ao usuário">
- **T4** — <tarefa que o usuário executa>
  - Atende: R3
  - Como: …
  - Quem roda: dev (<motivo: custo de LLM, credencial, ambiente dele, prova na tela>)
  - Verificar por / Meta: …

**Fim da fase 1:** <o que deve estar verde ou demonstrável>

## Pronto quando

Cada requisito aprovado da spec verificado pelo "Como se verifica" dele.

Validação manual (o usuário roda no final):

1. <passo> → <resultado esperado> (R1)
