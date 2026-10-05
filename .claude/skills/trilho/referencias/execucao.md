# Execução

Trabalhe uma tarefa de cada vez, na ordem do roteiro. A próxima é sempre a primeira que não está `feito` no `estado.md`.

## Tarefa com `Teste:`

1. **Teste primeiro.** Escreva o teste e rode. Ele precisa falhar **pelo motivo certo**: o comportamento ainda não existe. Se falhar por import, sintaxe ou setup, corrija isso antes, porque um teste que falha pelo motivo errado não prova nada.
2. **Implemente o mínimo** para o teste passar, seguindo o padrão local.
3. **Rode o teste e os testes relacionados.** Tudo verde.
4. **Marque `feito`** no `estado.md`, com o commit.
5. **Commite.** Siga a convenção do `projeto.md` e cite o id da tarefa no corpo (`T3`).

## Tarefa com `Verificar por:`

Execute a verificação e mostre o resultado antes de marcar `feito`.

## Tarefa empírica (`Meta:` / `Orçamento:`)

O resultado só aparece rodando, então a tarefa é um ciclo. Cada rodada:

1. **Hipótese:** o que você acha que causa a diferença, em uma linha.
2. **Mudança mínima** que testa essa hipótese. Uma por rodada, para saber o que funcionou.
3. **Rode e leia a evidência, não só o placar:** o que o sistema fez e por quê (trace, debug, log).
4. **Registre no `estado.md`:** hipótese, resultado, evidência (id de thread ou trace, commit). Hipótese descartada fica registrada para ninguém tentar de novo.

Confira efeitos fora do alvo: uma mudança que corrige um ponto pode quebrar outro (ex.: um texto que o modelo vê em todo turno muda todos os turnos). Rode o cenário completo, não só o ponto que você está corrigindo.

- **Atingiu a meta:** marque `feito`.
- **Orçamento esgotado:** aplique o plano B se ele foi combinado. Se não houver, pare e traga ao usuário o que aprendeu e as opções.

Rodadas dentro do orçamento não são desvio: não precisam de aprovação.

## Fim de fase

1. Rode a suíte completa e o lint/typecheck do `projeto.md`.
2. Confira o critério da fase.
3. Atualize o `estado.md`.
4. Contexto pesado: faça o handoff (`referencias/handoff.md`). Leve: siga para a próxima fase.

## Quando a realidade diverge do roteiro

- **Detalhe de implementação** (outro arquivo, outra função, teste em outro lugar): decida, registre em "Decisões da execução" no `estado.md` e siga.
- **Objetivo, escopo ou abordagem** precisariam mudar: pare e proponha o ajuste (ver "Autonomia" no `SKILL.md`). Com a aprovação, edite o `roteiro.md` e registre no `estado.md` o que mudou e por quê.

## Fim da execução

Com todas as tarefas `feito`, siga para `referencias/entrega.md`.
