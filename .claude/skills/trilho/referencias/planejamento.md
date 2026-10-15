# Planejamento

O objetivo é um `roteiro.md` que uma sessão nova, sem nada desta conversa, executa lendo só `projeto.md`, `roteiro.md` e `estado.md`, sem perguntar nada, e cujos porquês o usuário confirmou.

## 1. Branch

Antes de escrever qualquer arquivo, deixe a tarefa na branch dela. É a primeira ação do planejamento.

- **Na branch de integração** (do `projeto.md`): rode `git fetch` e crie a branch pelo padrão de nome do `projeto.md`, com o slug da tarefa, a partir da integração atualizada (ex.: `git switch -c feat/<slug> --no-track origin/<integração>`). Use `--no-track` para a branch não rastrear a integração; o upstream é definido no push da entrega.
- **Já em outra branch:** pergunte se a tarefa é dessa branch ou se é para criar uma nova.
- **Árvore com mudanças não commitadas:** pergunte antes de trocar de branch, para não levar trabalho do usuário junto sem querer.
- **Worktree:** só se o `projeto.md` pedir.

O nome e a base vão para o cabeçalho do roteiro.

## 2. Pesquisar

Entenda como o código funciona hoje antes de decidir qualquer coisa: o que a tarefa toca, os padrões e testes que já existem, os pontos de integração e quem mais usa o código que vai mudar. **Não pergunte o que o código responde.**

Em bug, a pesquisa vai até a causa: reproduza (teste, comando, log) e rastreie até onde o comportamento diverge do esperado. Se a causa não aparecer lendo nem reproduzindo de forma barata, ela é uma incerteza empírica e vira sondagem no roteiro.

**Leia direto** quando a tarefa toca poucos arquivos e você já sabe quais são. **Use subagentes** quando a área é ampla (vários módulos, fluxo que atravessa camadas, código que você não sabe onde fica) ou quando o bug não tem causa conhecida. Eles devolvem conclusões em vez de arquivos inteiros, e a sessão de planejamento fica leve para as perguntas e o roteiro.

- Lance de 1 a 3 subagentes em paralelo, numa mensagem só (Agent tool, tipo `Explore`, `model: "sonnet"`), cada um com uma pergunta diferente. Ex.: "onde está e como funciona o fluxo de X", "quem chama Y e o que depende do retorno dele", "como o projeto faz Z hoje (padrão e testes)". Passe o modelo explicitamente, como no revisor, para não depender do padrão do tipo.
- A instrução de cada um é o conteúdo de `referencias/pesquisador.md` mais a pergunta dele.
- Antes de decidir em cima de uma conclusão, confira os `arquivo:linha` que a sustentam. O subagente também erra.

**Se a tarefa mexe em UI** (tela, componente, layout, estilo): carregue a skill `frontend-design` (Skill tool, `frontend-design:frontend-design`) antes de decidir o desenho, e leve as escolhas visuais para a seção Decisões do roteiro. Se a skill não estiver instalada, siga sem ela e avise o usuário.

## 3. Mapear

Liste para você mesmo:

- **Porquês:** o problema em uma frase; em bug, a causa com `arquivo:linha` (não o sintoma); em feature, a motivação do pedido; e por que a abordagem resolve a causa, não só o sintoma (ver "Porquê e como" no `SKILL.md`).
- **Escopo:** o que entra e o que fica de fora.
- **Comportamento:** casos de borda, erros, estados vazios.
- **Efeitos colaterais:** quem já usa o código que vai mudar, dados existentes, migração, compatibilidade. Para cada efeito, uma mitigação.
- **Caminho:** a menor solução que resolve a causa. Uma opção mais elaborada precisa se justificar pelo pedido, não por "pode ser útil depois". Se a correção na raiz sai do escopo pedido, isso vira pergunta no passo 4.
- **Incertezas empíricas:** o que nem você nem o usuário sabem e só aparece rodando. Isso não vira pergunta: vira sondagem no roteiro.

## 4. Confirmar os porquês e perguntar

**Os porquês.** Antes das perguntas, mostre em texto, curto:

- **Problema:** o que está errado ou faltando.
- **Causa** (bug) ou **motivação** (feature), com `arquivo:linha` quando houver.
- **Abordagem:** o que vai mudar e por que resolve na raiz.
- **Decisões que eu tomaria sozinha:** cada uma em uma linha, com o porquê.

A primeira pergunta da rodada confirma esse bloco ("Os porquês acima batem com o que você sabe?", opções "Batem" e "Corrigir"). Ela vai na mesma chamada do AskUserQuestion das outras perguntas, para não abrir uma rodada só para isso. Se o usuário corrigir, ajuste e confirme de novo só a parte que mudou. Nada de roteiro com porquê não confirmado.

**As perguntas.** Antes de cada uma, teste: "se a resposta fosse a outra, o código ou o escopo mudaria? E o que o usuário já disse resolve?". Pergunte só se mudaria e não resolve. Caso contrário, decida e registre em Decisões, marcado como "(decidido por mim)". Fora a confirmação dos porquês e a pergunta de entrega, **zero perguntas é um resultado válido.**

**O que você decide e o que você pergunta:**

- **Decisão técnica** (onde fica o código, que padrão seguir, nome, estrutura de teste, como reaproveitar): decida, e mostre no bloco dos porquês.
- **Produto e negócio** (o que o usuário final vê ou faz: texto, fluxo de tela, valor pré-preenchido, o que aparece ou some, regra de negócio): pergunte, com a sua recomendação, mesmo que tenha um bom palpite. Só decida se o que o usuário disse já responde.
- **Raiz fora do escopo:** se corrigir a causa toca outro módulo, muda um contrato ou afeta outros usos, pergunte com as duas opções (corrigir na raiz × remendo consciente) e o que cada uma afeta.

**Pergunta fixa: entrega.** Toda tarefa pergunta o que fazer com o git ao final, para que nenhuma tarefa de push ou PR seja criada sem o usuário querer. Use AskUserQuestion (junto com as outras perguntas), sem recomendação, porque é preferência do usuário:

- **Só commits na branch:** o usuário faz push e PR;
- **Push da branch;**
- **Push + PR para `<integração>`.**

A resposta vai para o campo `Entrega:` do roteiro e só é executada na entrega, depois do code review.

As perguntas são da tarefa e ancoradas no código, nunca genéricas.

- Ruim: "Como você quer tratar erros?"
- Bom: "`calcularFrete` hoje devolve 0 para carrinho vazio, e o novo fluxo chama ele antes da validação. Mantemos o 0 ou passamos a lançar `CarrinhoVazioError`?"

Formato:

- **Decisão fechada:** AskUserQuestion com 2 a 4 opções. A recomendada vem primeiro, com "(Recomendado)", e cada descrição traz o trade-off. Junte até 4 perguntas independentes numa chamada.
- **Pergunta aberta** (objetivo, contexto de negócio): em texto.
- **Incerteza empírica relevante:** combine numa pergunta só, com recomendação, a **meta** (ex.: "eval 7/7 com 2 repetições"), o **orçamento** (rodadas, custo), o **plano B** se o orçamento acabar (ex.: "tirar a decisão do prompt e passar para código") e **quem roda** (você ou o usuário).

## 5. Escrever o roteiro

Escreva `roteiro.md` na pasta da tarefa a partir de `modelos/roteiro.md`.

- **Pedido:** o que o usuário pediu, reescrito de forma clara e fiel. Cada ideia, restrição, nome e número dele continua lá, com o porquê quando ele deu. Corrija a forma, não o conteúdo, e não acrescente requisitos. É a referência de "o que ele quis" para as próximas sessões.
- **Porquê:** o bloco confirmado no passo 4 (problema, causa ou motivação, abordagem), com a data da confirmação.
- **Tarefas:**
  - cada uma é uma ação verificável, não um tema, e cabe num passo de trabalho (se vai encostar em oito arquivos, quebre);
  - cada uma diz em `Porquê:` o que resolve, em uma linha, e em `Como:` o que fazer;
  - ordem por dependência **e por risco**: a sondagem da maior incerteza vem primeiro, antes de construir em volta dela;
  - branch, push, PR e code review **não são tarefas**: a branch já existe (passo 1), o review roda no fim de cada fase e push e PR são da entrega (`referencias/entrega.md`);
  - cada uma declara como é verificada: `Teste:` (escrito antes, TDD), ou `Verificar por:` com um comando ou passo concreto e o motivo de não ter teste, ou, se for empírica, `Meta:`, `Orçamento:` e `Se esgotar:`;
  - a que o usuário executa leva `Quem roda: dev` e o motivo (custo de LLM que ele aprova, credencial ou ambiente dele, prova na tela). Sem a marca, quem roda é você.
- **Fases:** só se houver mais de umas 8 tarefas ou não couber numa sessão. Cada fase entrega algo funcionando, termina com um critério claro e passa por um code review.
- **Pronto quando:** critério observável e o roteiro de validação manual para o usuário.
- **Curto.** Seção sem conteúdo fica "nenhuma". O roteiro é o mais curto que se basta.

## 6. Fechar

1. Crie o `estado.md` a partir de `modelos/estado.md`, com todas as tarefas `pendente` (inclusive a linha Entrega, no fim) e o próximo passo apontando para a primeira.
2. Commite o `roteiro.md` e o `estado.md` na branch da tarefa, seguindo a convenção do `projeto.md`.
3. Mostre um resumo de até 5 linhas: o pedido em uma frase, as incertezas e o caminho do roteiro. Os porquês o usuário já confirmou; não repita.
4. Faça o handoff (`referencias/handoff.md`). Sempre, mesmo com roteiro curto: você não mede o próprio contexto, e a execução rende mais numa sessão limpa.
