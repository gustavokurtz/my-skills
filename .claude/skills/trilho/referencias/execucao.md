# Execução

Trabalhe uma tarefa de cada vez, na ordem do roteiro. A próxima é sempre a primeira que não está `feito` nem `esperando o dev` no `estado.md`.

## O estado a cada tarefa

O `estado.md` acompanha a execução tarefa a tarefa, para que uma sessão que caia no meio saiba onde parou:

- **Ao começar** uma tarefa, marque-a `em andamento` e atualize "Próximo passo" e "Atualizado em".
- **Ao terminar**, marque `feito` e atualize "Onde paramos", "Próximo passo" e "Atualizado em". O `estado.md` entra no commit da própria tarefa. Não anote o hash: ele ainda não existe quando você edita o arquivo, e o commit cita o id da tarefa, o que basta para achá-lo no `git log`.

## Antes de cada tarefa

Diga ao usuário, em uma linha, o porquê e o como da tarefa. Ex.: "T3: o frete vinha 0 porque `calcularFrete` roda antes de `validarCarrinho` (`checkout.ts:42`); vou mover a chamada para depois da validação." Se você não consegue escrever essa linha, ainda não entendeu o bastante: leia mais antes de editar.

## Quando algo falha sem explicação

Teste vermelho que não devia, erro inesperado, comportamento estranho:

1. **Reproduza** e leia o erro inteiro.
2. **Rastreie até onde ele nasce**, não onde aparece. Escreva a hipótese em uma linha e a evidência que a confirma.
3. **Classifique a correção:** raiz ou sintoma (ver "Porquê e como" no `SKILL.md`). Raiz dentro do escopo: corrija. Fora do escopo, ou só dá para remendar: pare e traga ao usuário a causa e as opções.
4. **Registre a causa** em "Aprendizados" no `estado.md`, com `arquivo:linha`.

Se uma correção não resolveu, a hipótese estava errada: volte ao passo 2 em vez de empilhar outra correção em cima.

## Tarefa com `Teste:`

1. **Teste primeiro.** Escreva o teste e rode. Ele precisa falhar **pelo motivo certo**: o comportamento ainda não existe. Se falhar por import, sintaxe ou setup, corrija isso antes, porque um teste que falha pelo motivo errado não prova nada.
2. **Implemente o mínimo** para o teste passar, seguindo o padrão local.
3. **Rode o teste e os testes relacionados.** Tudo verde.
4. **Marque `feito`** no `estado.md` (ver "O estado a cada tarefa").
5. **Commite** o código e o `estado.md` juntos. Siga a convenção do `projeto.md` e cite o id da tarefa no corpo (`T3`).

## Tarefa com `Verificar por:`

Execute a verificação e mostre o resultado. Só então marque `feito` no `estado.md` e commite como numa tarefa com teste (se a tarefa não mudou código, o commit leva só o `estado.md`).

## Tarefa empírica (`Meta:` / `Orçamento:`)

O resultado só aparece rodando, então a tarefa é um ciclo. Cada rodada:

1. **Hipótese:** o que você acha que causa a diferença, em uma linha.
2. **Mudança mínima** que testa essa hipótese. Uma por rodada, para saber o que funcionou.
3. **Rode e leia a evidência, não só o placar:** o que o sistema fez e por quê (trace, debug, log).
4. **Registre no `estado.md`:** hipótese, resultado, evidência (id de thread ou trace, commit). Hipótese descartada fica registrada para ninguém tentar de novo.

Confira efeitos fora do alvo: uma mudança que corrige um ponto pode quebrar outro (ex.: um texto que o modelo vê em todo turno muda todos os turnos). Rode o cenário completo, não só o ponto que você está corrigindo.

- **Atingiu a meta:** marque `feito` no `estado.md` e commite.
- **Orçamento esgotado:** aplique o plano B se ele foi combinado. Se não houver, pare e traga ao usuário o que aprendeu e as opções.

Rodadas dentro do orçamento não são desvio: não precisam de aprovação.

## Tarefa com `Quem roda: dev`

Quem executa é o usuário; você prepara e lê.

1. **Entregue os comandos** prontos para copiar (diretório, variáveis, flags) e diga o que ele deve colar de volta (relatório, ids de trace ou thread, saída).
2. **Marque `esperando o dev: <o que ele roda>`** no `estado.md`, aponte o "Próximo passo" para "ler o resultado da Tn" e commite.
3. **Siga com as tarefas da fase que não dependem desse resultado.** Se só restarem tarefas que dependem dele, pare e diga que está esperando.
4. **Com o resultado em mãos,** leia a evidência como em qualquer tarefa: `Verificar por:` ou `Meta:`, e marque `feito`. Se for empírica, cada ida e volta conta uma rodada do orçamento; a próxima rodada volta ao passo 1.

## Fim de fase

A fase só fecha com todas as tarefas dela `feito`, inclusive as do dev.

Roteiro sem fases conta como uma fase só, que termina com a última tarefa.

1. Rode a suíte completa e o lint/typecheck do `projeto.md`.
2. Confira o critério da fase.
3. Faça o code review da fase (abaixo). Sempre.
4. Confira se o `estado.md` registra o que a fase ensinou (aprendizados, causas, decisões, hipóteses descartadas), não só o status das tarefas.
5. Mostre ao usuário, junto com o resultado do review, as decisões da execução desta fase, cada uma com o porquê. Ele precisa conhecê-las antes da próxima fase.
6. Faça o handoff (`referencias/handoff.md`) e peça o `/clear`. Sempre, mesmo que a fase tenha sido curta: a próxima fase começa numa sessão limpa. Na última fase, não: siga para a entrega na mesma sessão (ver "Fim da execução").

## Code review da fase

Revisar a cada fase evita acumular bug para o fim e abrir outra sessão só para corrigir. Lance **um** subagente (Agent tool, tipo general-purpose, `model: "opus"`) com contexto limpo, como juiz: quem escreveu o código tende a aprovar o próprio trabalho, e um revisor que não viu a conversa lê só o que está nos arquivos. Passe o modelo explicitamente: sem ele, o revisor herda o modelo da sessão, e o juiz precisa ser forte mesmo quando a sessão roda num modelo mais leve. É um por fase, então o custo é pequeno.

A instrução dele é o conteúdo de `referencias/revisor.md`, mais:

- o caminho do `roteiro.md`;
- o intervalo `<base>..HEAD`, com `<base>` = o "Último review" do `estado.md` ou, na primeira fase, `git merge-base <integração> HEAD` (use `origin/<integração>` se houver remoto);
- as tarefas da fase (ex.: "T4 a T7") e se é a última fase.

O revisor só reporta achados com confiança ≥ 80. Mesmo assim, verifique cada um antes de agir, porque o revisor também erra. Corrija o que for real, rode os testes afetados e commite. Quando discordar de um achado, diga isso explicitamente ao usuário.

Registre no `estado.md` o "Último review" (o hash do HEAD que o revisor leu e a fase) e, em "Aprendizados", os achados corrigidos.

## Quando a realidade diverge do roteiro

- **Detalhe de implementação** (outro arquivo, outra função, teste em outro lugar): decida, registre em "Decisões da execução" no `estado.md` e siga.
- **Objetivo, escopo ou abordagem** precisariam mudar, ou a correção na raiz sai do escopo: pare e proponha o ajuste (ver "Autonomia" no `SKILL.md`). Com a aprovação, edite o `roteiro.md` e registre no `estado.md` o que mudou e por quê.

## Fim da execução

Quando a última tarefa virar `feito`, faça o fim de fase da última fase, com o code review. Depois mude a etapa do `estado.md` para `entrega` e o "Próximo passo" para "entrega: verificação completa e push/PR", leia `referencias/entrega.md` e siga.

Não dê a tarefa por pronta antes da entrega. Se o contexto estiver pesado, pode fazer o handoff antes, porque o `estado.md` já aponta para a entrega.
