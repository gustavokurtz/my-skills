# Etapa: plano

O plano é a lista de tarefas e de como cada uma vai ser feita. Ele precisa se bastar: uma sessão nova, sem nada desta conversa, tem que conseguir executá-lo lendo só `projeto.md`, `spec.md` e `plano.md`.

Escreva `plano.md` na pasta da tarefa a partir de `modelos/plano.md`.

- No fluxo grande, a fonte é a spec aprovada.
- No fluxo pequeno, não há spec. O plano traz o objetivo e o critério de pronto, e antes de escrevê-lo você pergunta o que for ambíguo **num ponto que muda o desenho da solução**.

## Tarefas

- **Cada tarefa é uma ação verificável, não um tema.** "Adicionar índice em `users.email`" serve. "Melhorar performance" não.
- **Cada tarefa cabe num passo de trabalho.** Se ela vai encostar em oito arquivos, quebre.
- **Ordem por dependência.** O que precisa existir primeiro vem primeiro.
- **Cada tarefa declara como vai ser verificada:**
  - `Teste:` qual teste é escrito antes da implementação (TDD).
  - Ou `Sem teste:` com a justificativa (migration, config, docs, CI…) e `Verificar por:` com um comando ou passo concreto que prova que funcionou. "Sem teste" sem justificativa não é aceito.
- **Rastreabilidade (fluxo grande):** cada tarefa diz quais requisitos cobre (`Cobre: R1, R3`). Antes de apresentar, confira que todo critério de aceite da spec é coberto por pelo menos uma tarefa.

## Fases e checkpoints

Se o plano tem mais de umas 8 tarefas, ou não cabe numa sessão, divida em fases. Cada fase:

- entrega algo funcionando e testado, não metade de uma coisa;
- termina num **checkpoint** com um critério claro ("POST /pedidos aceita cupom e os testes de R1 e R2 passam").

Plano pequeno pode ter uma fase só.

## Validação manual

Escreva o roteiro e2e que o usuário vai executar no final: passos concretos e o resultado esperado de cada um.

## GATE 2 (no fluxo pequeno, o único gate)

Apresente as fases, as tarefas (uma linha cada) e o caminho do arquivo. Espere aprovação explícita.

Aprovado:

1. Preencha `tarefas` no `progresso.json` (um item por tarefa, com `fase` e `passou: false`) e atualize `etapa` para `execucao`.
2. **Fluxo grande:** recomende `/clear` e retomar com "executa o plano <slug>". A sessão nova executa só a partir dos arquivos, e isso é o teste de que eles se bastam.
3. **Fluxo pequeno:** pode seguir direto para `referencias/execucao.md`.
