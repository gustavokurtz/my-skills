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
3. **Ache a causa de desenho e a família.** Escreva também, em uma linha, o que no sistema permite essa classe de falha, e compare com "Defeitos" no `estado.md` (e com os aprendizados do `projeto.md`). Mesmo mecanismo de um defeito anterior: é família.
4. **Classifique a correção:** raiz ou sintoma (ver "Porquê e como" no `SKILL.md`). Raiz dentro do escopo e primeiro da família: corrija. Fora do escopo, só dá para remendar, ou segundo da família: lance o arquiteto (abaixo), pare e traga ao usuário a causa e as opções, local e estrutural.
5. **Registre o defeito** em "Defeitos" no `estado.md`: sintoma, causa imediata com `arquivo:linha`, mecanismo de desenho em uma linha e o que foi feito.

Se uma correção não resolveu, a hipótese estava errada: volte ao passo 2 em vez de empilhar outra correção em cima. Correção que falhou na rodada real (eval, tela) também aciona o arquiteto antes da próxima tentativa.

## Arquiteto

Um subagente com contexto limpo, que não herda o viés desta sessão nem a hipótese dela: ele lê o sistema e o histórico de defeitos e propõe a correção local e a estrutural. Lance **um** (Agent tool, tipo general-purpose, `model: "fable"`) quando:

- é o segundo defeito da mesma família;
- uma correção falhou na rodada real;
- o usuário pedir uma visão crítica ou "um subagente mais capaz" para uma correção.

A instrução dele é o conteúdo de `referencias/arquiteto.md`, mais os sintomas (com ids de thread, trace, teste), o caminho do `estado.md` e do `roteiro.md` e o que já foi tentado e desfeito. **Não passe a sua hipótese nem peça "a menor mudança":** isso prende o arquiteto ao remendo. Verifique os `arquivo:linha` e as medições que ele trouxer antes de repassar, e leve ao usuário as opções no formato de "Como falar com o usuário" (`SKILL.md`). Quem escolhe é ele.

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

1. **Hipótese:** o que você acha que causa a diferença, em uma linha, tirada do código e do texto que o modelo recebe (ver "Dois tipos de incerteza" no `SKILL.md`). Sem hipótese, não há rodada.
2. **Mudança mínima** que testa essa hipótese. Uma por rodada, para saber o que funcionou.
3. **Rode e leia a evidência, não só o placar:** o que o sistema fez e por quê (trace, debug, log).
4. **Registre no `estado.md`:** hipótese, resultado, evidência (id de thread ou trace, commit). Hipótese descartada fica registrada para ninguém tentar de novo.

Confira efeitos fora do alvo: uma mudança que corrige um ponto pode quebrar outro (ex.: um texto que o modelo vê em todo turno muda todos os turnos). No replay, os controles incluem os casos vizinhos que recebem o texto alterado (outras falas, outros cenários com o mesmo estado), não só as falas do defeito. Na rodada real, rode o cenário completo, não só o ponto que você está corrigindo.

Mudança no produto e mudança na régua do eval vão em commits separados: desfazer uma não pode deixar a outra para trás, e cada uma se mede sozinha.

- **Atingiu a meta:** marque `feito` no `estado.md` e commite.
- **Orçamento esgotado:** aplique o plano B se ele foi combinado. Se não houver, pare e traga ao usuário o que aprendeu e as opções.

Rodadas dentro do orçamento não são desvio: não precisam de aprovação.

## Tarefa com `Quem roda: dev`

Quem executa é o usuário; você prepara e lê.

Um bloqueio de ambiente registrado no `estado.md` por outra sessão ("não consigo rodar X, o usuário roda") é hipótese, não regra. Em cada sessão, tente uma vez o comando não destrutivo antes de passá-lo ao usuário. Só delegue o que é destrutivo, caro por decisão dele (eval com custo de LLM), ou o que bloqueou nesta sessão.

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
4. Confira se o `estado.md` registra o que a fase ensinou (defeitos, aprendizados, decisões, hipóteses descartadas), não só o status das tarefas.
5. Mostre ao usuário o que mudou no código, junto com o resultado do review e as decisões da execução desta fase (cada uma com o porquê). Ele precisa conhecer as duas coisas antes da próxima fase. O "o que mudou" é uma explicação, não um relatório. Para cada mudança que importa:
   - **Onde:** `arquivo:linha` e a função.
   - **Antes → agora:** o comportamento, em uma frase com as palavras do domínio.
   - **Por quê:** a causa ou o pedido que exigiu a mudança.
   - **O trecho:** até ~10 linhas do código novo, quando ele ajuda a entender. Mudança mecânica (renome, teste, texto) entra numa linha só, agrupada.

## Quando rodar a suíte inteira

A suíte do `projeto.md` fecha a fase e vem antes de commitar código de produção. Mudança só no instrumento de medição (o script do eval, a régua dele e o teste dele) roda o teste desse instrumento e entrega o comando ao usuário. A suíte fica para o fim da fase.
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
