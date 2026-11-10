# Planejamento

O planejamento tem três produtos, nesta ordem:

1. **Perguntas** no chat: as decisões que só o usuário toma.
2. **Spec** (`spec.md`): o que vai ser feito e por quê, para ele ler.
3. **Plano** (`plano.md`): como fazer, que uma sessão nova, sem nada desta conversa, executa lendo só `projeto.md`, `spec.md`, `plano.md` e `estado.md`, sem perguntar nada.

Nada disso passa por aprovação formal. Ele responde as perguntas, lê a spec quando quiser e muda o que quiser editando o `spec.md` ou falando no chat.

**Pedido de feature gera um trilho que termina com ela funcionando.** Protótipo, docs e esboços são tarefas da primeira fase dele, não um trilho à parte. Se você propuser um trilho só de planejamento ou documentação, diga isso com essas palavras ("este trilho não entrega código; a implementação é outro trilho depois"), e o recap de cada retomada repete.

## 1. Branch

Antes de escrever qualquer arquivo, deixe a tarefa na branch dela. É a primeira ação do planejamento.

- **Na branch de integração** (do `projeto.md`): rode `git fetch` e crie a branch pelo padrão de nome do `projeto.md`, com o slug da tarefa, a partir da integração atualizada (ex.: `git switch -c feat/<slug> --no-track origin/<integração>`). Use `--no-track` para a branch não rastrear a integração; o upstream é definido no push da entrega.
- **Já em outra branch:** pergunte se a tarefa é dessa branch ou se é para criar uma nova.
- **Árvore com mudanças não commitadas:** pergunte antes de trocar de branch, para não levar trabalho do usuário junto sem querer.
- **Worktree:** só se o `projeto.md` pedir.

O nome e a base vão para o cabeçalho do plano.

## 2. Pesquisar

Entenda como o código funciona hoje antes de decidir qualquer coisa: o que a tarefa toca, os padrões e testes que já existem, os pontos de integração e quem mais usa o código que vai mudar. **Não pergunte o que o código responde.**

Em bug, a pesquisa vai até a causa: reproduza (teste, comando, log) e rastreie até onde o comportamento diverge do esperado. Se a causa não aparecer lendo nem reproduzindo de forma barata, ela é uma incerteza empírica e vira sondagem no plano.

**Leia direto** quando a tarefa toca poucos arquivos e você já sabe quais são. **Use subagentes** quando a área é ampla (vários módulos, fluxo que atravessa camadas, código que você não sabe onde fica) ou quando o bug não tem causa conhecida. Eles devolvem conclusões em vez de arquivos inteiros, e a sessão de planejamento fica leve.

- Lance de 1 a 3 subagentes em paralelo, numa mensagem só (Agent tool, tipo `Explore`, `model: "sonnet"`), cada um com uma pergunta diferente. Ex.: "onde está e como funciona o fluxo de X", "quem chama Y e o que depende do retorno dele", "como o projeto faz Z hoje (padrão e testes)". Passe o modelo explicitamente, como no revisor, para não depender do padrão do tipo.
- A instrução de cada um é o conteúdo de `referencias/pesquisador.md` mais a pergunta dele.
- Antes de decidir em cima de uma conclusão, confira os `arquivo:linha` que a sustentam. O subagente também erra.

**Se a tarefa mexe em UI** (tela, componente, layout, estilo): carregue a skill `frontend-design` (Skill tool, `frontend-design:frontend-design`) antes de decidir o desenho. Se o projeto tem um protótipo navegável (ou dá para fazer uma página solta rápida), faça um esboço e mande o link junto das perguntas: ele julga o desenho vendo, não lendo. Diga que o app de verdade só muda na execução. Se a skill não estiver instalada, siga sem ela e avise.

## 3. Mapear

Liste para você mesmo:

- **Porquês:** o problema em uma frase; em bug, a causa com `arquivo:linha` (não o sintoma); em feature, a motivação do pedido; e por que a abordagem resolve a causa, não só o sintoma (ver "Porquê e como" no `SKILL.md`).
- **Escopo:** o que entra. O que não vai ser feito não aparece nas perguntas nem na spec. A exceção é deixar de fora algo que o usuário pediu: isso nunca é decisão sua, vira pergunta.
- **Comportamento:** casos de borda, erros, estados vazios.
- **Efeitos colaterais:** quem já usa o código que vai mudar, dados existentes, migração, compatibilidade. Para cada efeito, uma mitigação.
- **Caminho:** a menor solução que resolve a causa. Uma opção mais elaborada precisa se justificar pelo pedido, não por "pode ser útil depois". Se a correção na raiz sai do escopo pedido, isso vira pergunta.
- **Incertezas empíricas:** o que nem você nem o usuário sabem e só aparece rodando. Isso não vira pergunta sobre o resultado: vira sondagem no plano, com meta e orçamento combinados nas perguntas.

O comportamento e os porquês viram requisitos da spec; o caminho vira o plano.

## 4. Perguntas

Uma rodada no chat, com AskUserQuestion (até 4 perguntas por chamada; a recomendada é a primeira opção, com "(Recomendado)"). Pergunta aberta (objetivo, contexto de negócio) vai em texto, curta. Antes das perguntas, se ajudar, diga em até 3 linhas o que você entendeu do pedido (em bug, a causa), em linguagem simples.

**O que vira pergunta.** Antes de cada uma, teste: "se a resposta fosse a outra, o código ou o escopo mudaria? E o que o usuário já disse resolve?". Pergunte só se mudaria e o que ele disse não resolve. O que uma fala dele já resolve vai para "O que ficou decidido" na spec, sem perguntar de novo. As perguntas são da tarefa e ancoradas no código, nunca genéricas:

- Ruim: "Como você quer tratar erros?"
- Bom: "Hoje o frete vem 0 com carrinho vazio, e o novo fluxo calcula antes de validar. Mantemos o 0 ou mostramos um erro?"

Cada opção diz o que o usuário final vê. Tipos:

- **Produto:** o que o usuário final vê ou faz (texto, fluxo, valor pré-preenchido, regra de negócio, o que acontece quando dá errado), com um exemplo concreto por opção.
- **Desenho:** só a decisão técnica que muda o que o usuário vê, contraria uma decisão registrada (ADR, `CLAUDE.md`, diga qual) ou afeta o trabalho de outras pessoas. As outras decisões técnicas você toma e põe no plano.
- **Escopo:** a correção na raiz sai do escopo (opções: raiz × remendo consciente, com o que cada uma afeta), ou algo que ele pediu ficaria de fora (incluir × depois).
- **Incerteza:** a incerteza empírica relevante, com **meta** (ex.: "eval 7/7 com 2 repetições"), **orçamento** (rodadas, custo), **plano B** se acabar, **quem roda** e **o que fecha a rodada** (defeito novo sem relação com a mudança vira ponto em aberto, não correção na hora). O orçamento é o teto: cada rodada com custo ainda pede o "pode" dele na execução.
- **Entrega:** fixa, em toda tarefa: "Só commits na branch" (ele faz push e PR), "Push da branch" ou "Push + PR para `<integração>`". Sem opção recomendada: é preferência dele.

**Perguntas para outro time** (contrato de API externa, comportamento de sistema de terceiro): filtre antes, **só eles sabem a resposta?** Se o nosso código, uma decisão registrada ou o próprio usuário resolvem, ela não vai. As que passam, mostre no chat, cada uma em poucas linhas: o que vem hoje, o que fazemos com isso, a dúvida e o que o usuário final vê se vier diferente. Ele tira o que quiser; depois monte o texto para enviar, pedindo resposta de todas.

**Regra que o usuário escreveu** (formato, faixa, texto) não vira pergunta com reinterpretações dela como opções. Ela vai para a spec ao pé da letra, onde ele disse. Só pergunte o que a regra não responde.

**Ao receber as respostas:**

1. **Resposta que é dúvida** ("não entendi", "mas como fica X?"): responda em uma ou duas frases antes de qualquer outra coisa. Não grave nada no lugar de responder.
2. **Ele disse que você entendeu errado:** corrija o entendimento e refaça só as perguntas que dependiam dele.
3. **Respostas dadas:** siga para a spec. Uma segunda rodada só se uma resposta abriu uma decisão nova.

## 5. Spec

A spec diz **o quê e por quê**, sem o como. Ela nasce do pedido, da pesquisa e das respostas, e não traz pergunta em aberto. Escreva `spec.md` na pasta da tarefa seguindo `modelos/spec.md`.

**Escreva para ele ler sem esforço.** É um texto amigável, como se você explicasse a um colega: frases curtas, as palavras do domínio e as dele, exemplos com valores de verdade. Nada de nome de função, campo, status ou sigla que ele não usou; nada de tabela, linha separadora ou bloco de código. Se ele precisar reler uma frase para entender, reescreva.

- **O problema:** até 3 linhas.
- **O que você quer** (O1, O2…): os objetivos, fiéis às palavras e aos números dele. Sem objetivo que ele não deu.
- **O que vai mudar** (R1, R2…): cada requisito uma coisa só, verificável, com "Quando <situação>, <o que acontece>", um exemplo concreto, o porquê (com o objetivo que ele serve) e como a gente confere.
- **⚠️ Vai além do pedido:** só no requisito que cresceu o escopo ou existe por outro motivo (efeito colateral, decisão), em uma frase. Em correção estrutural que deixa casos da mesma família sem cobertura, diga quais. É o sinal de escopo crescendo; não esconda.
- **O que ficou decidido:** as respostas das perguntas e o que você decidiu que ele precisa conhecer (só o que muda o que ele vê), cada um com a fonte.

Objetivo sem requisito é uma lacuna: cubra, ou diga no objetivo por que ficou de fora.

**Antes de abrir, confira cada requisito:** dá para verificar? Tem uma leitura só? O exemplo é concreto? Ele descreve o quê, e não o como (arquivo, função ou estrutura vai para o plano)? Contradiz uma resposta dele? O tamanho acompanha a tarefa: um bug pequeno tem de 2 a 5 requisitos, não 16.

**Não abra o arquivo:** ele abre no editor dele. No chat, uma linha com o caminho do `spec.md` e, se houver, quantos requisitos têm ⚠️. Não espere resposta: siga para o plano. Se ele comentar no chat enquanto isso, trate antes de fechar o plano: edite o `spec.md` e ajuste o que dependia.

## 6. Plano

Escreva `plano.md` a partir de `modelos/plano.md`. O plano não passa por aprovação do usuário: é como cumprir a spec.

- **Decisões:** as respostas dele e as técnicas que você tomou, marcadas "(decidido por mim)", cada uma com o porquê.
- **Tarefas:**
  - cada uma é uma ação verificável, não um tema, e cabe num passo de trabalho (se vai encostar em oito arquivos, quebre);
  - cada uma diz em `Atende:` os requisitos que cumpre, e em `Como:` o que fazer. **Todo requisito da spec aparece em pelo menos um `Atende:`;** confira antes de fechar;
  - ordem por dependência **e por risco**: a sondagem da maior incerteza vem primeiro, antes de construir em volta dela;
  - branch, push, PR e code review **não são tarefas**: a branch já existe (passo 1), o review roda no fim de cada fase e push e PR são da entrega (`referencias/entrega.md`);
  - cada uma declara como é verificada: `Teste:` (escrito antes, TDD), ou `Verificar por:` com um comando ou passo concreto e o motivo de não ter teste, ou, se for empírica, `Meta:`, `Orçamento:` e `Se esgotar:`;
  - a que o usuário executa leva `Quem roda: dev` e o motivo (custo de LLM que ele aprova, credencial ou ambiente dele, prova visual). Sem a marca, quem roda é você.
- **Fases:** só se houver mais de umas 8 tarefas ou não couber numa sessão. Cada fase entrega algo funcionando, termina com um critério claro e passa por um code review.
- **Pronto quando:** cada requisito verificado pelo "como a gente confere" dele, e o passo a passo da validação manual para o usuário, com o requisito de cada passo.
- **Curto.** Seção sem conteúdo fica "nenhuma". O plano é o mais curto que se basta.

**Antes de fechar, questione o plano** (para você, sem perguntar a ele): o que pode quebrar, qual o passo mais arriscado e que opção você descartou e por quê. O que mudar o plano entra nele: o risco vira tarefa mais cedo ou verificação, e a opção descartada vai para Decisões com o porquê, para ninguém tentar de novo sem saber.

## 7. Fechar

1. Crie o `estado.md` a partir de `modelos/estado.md`, com todas as tarefas `pendente` (inclusive a linha Entrega, no fim) e o próximo passo apontando para a primeira.
2. Commite `spec.md`, `plano.md` e `estado.md` na branch da tarefa, seguindo a convenção do `projeto.md`.
3. Diga em até 3 linhas o caminho do plano: fases, a maior incerteza e quem roda o quê. Lembre que ele pode editar o `spec.md` antes do `/clear` ou depois: a próxima sessão confere.
4. Faça o handoff (`referencias/handoff.md`). Sempre, mesmo com plano curto: você não mede o próprio contexto, e a execução rende mais numa sessão limpa.
