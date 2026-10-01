# Plano — <título da tarefa>

**Tarefa:** AAAA-MM-DD-<slug>
**Fluxo:** grande | pequeno
**Spec:** `spec.md` | — (fluxo pequeno)
**Branch:** <nome da branch>

## Objetivo e critério de pronto

Só no fluxo pequeno; no grande, a spec cumpre esse papel. O que muda para quem usa, e como saber que acabou, de forma observável: "POST /orders devolve 422 com corpo inválido e existe teste cobrindo isso".

## Abordagem

O desenho da solução em 3 a 5 linhas. Se uma alternativa foi considerada e descartada, registre em uma linha por quê.

## Arquivos afetados

- `caminho/do/arquivo.ts` — o que muda

## Tarefas

### Fase 1 — <o que fica funcionando ao fim da fase>

- **T1** — <ação verificável>
  - Como: <o que fazer, em uma ou duas linhas>
  - Teste: <teste a escrever antes de implementar>
  - Cobre: R1
- **T2** — <ação verificável>
  - Como: …
  - Sem teste: <justificativa>. Verificar por: <comando ou passo concreto>
  - Cobre: R2

**Checkpoint 1:** <o que deve estar verde ou demonstrável>

### Fase 2 — <…>

- **T3** — …

**Checkpoint 2:** …

## Validação manual (e2e)

1. <passo> → <resultado esperado>
2. <passo> → <resultado esperado>

## Desvios

Preencher durante a execução: o que mudou em relação ao plano aprovado e por quê.

- (nenhum até agora)

## Resultado

Preencher na entrega: commits, resultado dos testes, achados do review, o que ficou de fora e por quê.
