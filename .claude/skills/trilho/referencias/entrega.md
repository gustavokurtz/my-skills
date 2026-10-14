# Entrega

A entrega é uma etapa obrigatória, não um extra: a tarefa só termina depois dela. Siga esta ordem. O code review já rodou no fim de cada fase (`referencias/execucao.md`), e push e PR só acontecem depois dele.

## 1. Verificação completa

Rode a suíte de testes inteira, o lint, o typecheck e o build, conforme o `projeto.md`. Falhou: conserte e volte ao início desta lista.

## 2. Review conferido

Confira se o `estado.md` registra o review da última fase. Se não registrar (tarefa antiga, ou o review ficou de fora), faça agora o "Code review da fase" de `referencias/execucao.md`, como última fase, antes de seguir.

## 3. Registro

Preencha a seção Resultado do `estado.md` (commits, resultado dos testes, achados dos reviews, o que ficou de fora e por quê), marque a linha Entrega como `feito` e mude a etapa para `concluida`.

O `estado.md` morre com a tarefa. Releia os Aprendizados, as Decisões da execução e o que o usuário disse: o que uma tarefa futura, sem relação com esta, precisaria saber (comando que só funciona de um jeito, armadilha do projeto, convenção que o usuário corrigiu) sobe para o `.trilho/projeto.md`, uma linha cada, na seção que couber (Comandos, Convenções de código, Regras fixas, Áreas sensíveis ou Armadilhas; crie a seção se ela não existir). O que só vale para esta tarefa fica no `estado.md`. Nada durável: siga sem mexer no `projeto.md`.

Commite o `estado.md` e o `projeto.md` juntos.

## 4. Push e PR

Faça o que o campo `Entrega:` do roteiro diz, e nada além:

- **Só commits na branch:** não faça push.
- **Push da branch:** `git push -u origin <branch>`.
- **Push + PR:** faça o push e abra o PR para a branch de integração (`gh pr create`), seguindo o template de PR do repo, se houver. Na descrição: o pedido em uma frase, o que mudou, o resultado dos testes, o resumo dos reviews e a validação manual.

Roteiro sem o campo `Entrega:` (tarefa antiga): pergunte antes do push. Push recusado (hook, conflito, permissão): pare e traga o erro ao usuário, sem contornar.

## 5. Fechamento

Responda com:

- o que foi feito, em uma ou duas frases;
- os commits criados;
- o resultado dos testes;
- o resumo dos reviews;
- o que subiu para o `projeto.md`, se algo subiu;
- o link do PR, se abriu um;
- o roteiro de validação manual (do "Pronto quando"), para o usuário rodar;
- o caminho da pasta da tarefa.

Não espere o resultado da validação manual. Se o usuário relatar um problema, ele vira uma nova rodada de execução.

Nada de relatório longo: os arquivos já são o registro.
