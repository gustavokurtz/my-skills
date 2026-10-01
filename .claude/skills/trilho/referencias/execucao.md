# Etapa: execução

Trabalhe uma tarefa de cada vez, na ordem do plano. A próxima tarefa é sempre a primeira com `passou: false` no `progresso.json`.

## Ciclo de cada tarefa

1. **Teste primeiro.** Escreva o teste descrito na tarefa e rode. Ele precisa falhar **pelo motivo certo**: o comportamento ainda não existe. Se falhar por erro de import, de sintaxe ou de setup, corrija isso primeiro, porque um teste que falha pelo motivo errado não prova nada.
2. **Implemente o mínimo** para o teste passar, seguindo o padrão local.
3. **Rode o teste da tarefa e os testes relacionados.** Tudo verde.
4. **Marque `passou: true`** no `progresso.json`.
5. **Commite.** Uma tarefa costuma ser um bom tamanho de commit. Siga a convenção do `projeto.md` e cite o id da tarefa no corpo (`T3`).

Tarefa marcada `Sem teste`: execute o `Verificar por:` do plano e mostre o resultado antes de marcar `passou`.

Se um teste que já existia quebrar, conserte a causa, não o teste. Se o teste estiver genuinamente errado, diga isso explicitamente ao usuário em vez de ajustá-lo em silêncio.

## Checkpoint (fim de cada fase)

1. Rode a suíte completa e o lint/typecheck do `projeto.md`.
2. Confira o critério do checkpoint escrito no plano.
3. Recapitule em poucas linhas o que a fase entregou e o que vem na próxima.
4. Pergunte com AskUserQuestion: **seguir para a próxima fase** ou **pausar** (`/clear` e retomar depois com "continua o plano <slug>"). Se o contexto já estiver pesado, recomende pausar.

## Desvios

Quando a realidade divergir do plano (a abordagem não funciona, apareceu uma dependência, um requisito estava errado):

1. **Pare.** Não improvise em cima do plano.
2. **Analise:** o que mudou, o impacto e as opções, incluindo a mais simples.
3. **Proponha o ajuste** ao usuário. Se mudar um requisito, mude também a spec, e isso exige nova aprovação.
4. **Com a aprovação**, registre na seção Desvios do plano o que mudou e por quê, edite ou adicione as tarefas e atualize `tarefas` no `progresso.json`.
5. Só então volte a executar.

Um plano que não bate com o que foi feito mente para quem ler depois, inclusive para a próxima sessão.

## Fim da execução

Com todas as tarefas em `passou: true`, atualize `etapa` para `entrega` e siga para `referencias/entrega.md`.
