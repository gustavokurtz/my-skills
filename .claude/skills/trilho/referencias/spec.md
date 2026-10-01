# Etapa: spec (só fluxo grande)

A spec é o resumo dos requisitos. Ela tem dois leitores: a LLM que vai planejar (talvez numa sessão sem nenhum contexto desta conversa) e o usuário, que precisa conseguir ler e aprovar em poucos minutos.

Escreva `spec.md` na pasta da tarefa a partir de `modelos/spec.md`.

## Regras

- **O quê e o porquê, não o como.** O como vai no plano. A exceção são as decisões da entrevista que restringem o como ("usar a fila que já existe, não criar outra"): elas entram na seção Decisões.
- **Requisitos numerados (`R1`, `R2`…), cada um com critérios de aceite observáveis.** Use o formato "Quando <situação>, <comportamento esperado>." Cada critério vai virar um teste na execução. Se um critério não dá para testar, ele está vago: reescreva.
- **Fora de escopo é explícito.** É o que mais evita trabalho que ninguém pediu.
- **Premissas:** o que você decidiu sem perguntar. O usuário revisa no gate.
- **Pendências precisam estar vazias** para a spec ir ao gate. Se sobrou alguma, volte à entrevista.
- **Curta.** Se passar de uma ou duas telas, provavelmente são duas tarefas, ou o como invadiu a spec.

## GATE 1

Apresente um resumo de poucas linhas (requisitos, o que fica fora, decisões principais) e o caminho do arquivo. Espere aprovação explícita.

- Ajustes pedidos: edite a spec e reapresente.
- Aprovada: marque `**Status:** aprovada` na spec, atualize `etapa` para `plano` no `progresso.json` e siga para `referencias/plano.md`.

Depois de aprovada, a spec só muda com nova aprovação.
