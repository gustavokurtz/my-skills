# Planejamento

O planejamento tem três produtos, nesta ordem, e cada um só começa quando o anterior fecha:

1. **Discovery** (`discovery.json`): as decisões que só o usuário toma, respondidas por ele numa tela.
2. **Spec** (`spec.json`): o contrato do que vai ser feito e por quê, aprovado por ele item a item.
3. **Plano** (`plano.md`): como fazer, que uma sessão nova, sem nada desta conversa, executa lendo só `projeto.md`, `spec.json`, `plano.md` e `estado.md`, sem perguntar nada.

Discovery e spec são lidos e respondidos numa página no navegador (ver "A tela de revisão", no fim). O chat não leva bloco de porquês nem pedido de "batem?": a validação está na spec, em cada requisito.

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

**Leia direto** quando a tarefa toca poucos arquivos e você já sabe quais são. **Use subagentes** quando a área é ampla (vários módulos, fluxo que atravessa camadas, código que você não sabe onde fica) ou quando o bug não tem causa conhecida. Eles devolvem conclusões em vez de arquivos inteiros, e a sessão de planejamento fica leve para o discovery, a spec e o plano.

- Lance de 1 a 3 subagentes em paralelo, numa mensagem só (Agent tool, tipo `Explore`, `model: "sonnet"`), cada um com uma pergunta diferente. Ex.: "onde está e como funciona o fluxo de X", "quem chama Y e o que depende do retorno dele", "como o projeto faz Z hoje (padrão e testes)". Passe o modelo explicitamente, como no revisor, para não depender do padrão do tipo.
- A instrução de cada um é o conteúdo de `referencias/pesquisador.md` mais a pergunta dele.
- Antes de decidir em cima de uma conclusão, confira os `arquivo:linha` que a sustentam. O subagente também erra.

**Se a tarefa mexe em UI** (tela, componente, layout, estilo): carregue a skill `frontend-design` (Skill tool, `frontend-design:frontend-design`) antes de decidir o desenho, e leve as escolhas visuais que mudam o que o usuário vê para o discovery (`desenho`), e o resto para as Decisões do plano. Se a skill não estiver instalada, siga sem ela e avise o usuário.

## 3. Mapear

Liste para você mesmo:

- **Porquês:** o problema em uma frase; em bug, a causa com `arquivo:linha` (não o sintoma); em feature, a motivação do pedido; e por que a abordagem resolve a causa, não só o sintoma (ver "Porquê e como" no `SKILL.md`).
- **Escopo:** o que entra e o que fica de fora.
- **Comportamento:** casos de borda, erros, estados vazios.
- **Efeitos colaterais:** quem já usa o código que vai mudar, dados existentes, migração, compatibilidade. Para cada efeito, uma mitigação.
- **Caminho:** a menor solução que resolve a causa. Uma opção mais elaborada precisa se justificar pelo pedido, não por "pode ser útil depois". Se a correção na raiz sai do escopo pedido, isso vira pergunta no passo 4.
- **Incertezas empíricas:** o que nem você nem o usuário sabem e só aparece rodando. Isso não vira pergunta sobre o resultado: vira sondagem no plano, com meta e orçamento combinados no discovery (`incerteza`).

O comportamento e os porquês viram requisitos da spec; o caminho vira o plano.

## 4. Discovery

O discovery junta numa tela tudo o que o usuário precisa decidir antes de existir uma spec. Escreva `discovery.json` na pasta da tarefa seguindo `modelos/discovery.json`.

- **`entendimento`:** o problema e o que você entendeu do pedido, em até 5 linhas de linguagem simples (ver "Como falar com o usuário" no `SKILL.md`). Em bug, a causa nos dois níveis, imediata e de desenho, dita com as palavras do domínio. Na tela, ele marca "Entendeu certo" ou "Entendeu errado" (o item `ENT` nas respostas).
- **`achados`** (opcional): o que a pesquisa encontrou e que muda a conversa, cada um com a prova técnica em `prova` (fica recolhida na tela).
- **`perguntas`:** as decisões, uma por item, com 2 a 4 opções. A recomendada leva `"recomendada": true` (nunca na de entrega, que é preferência dele). Cada opção diz em `efeito` o que o usuário final vê. Pergunta aberta (objetivo, contexto de negócio) leva `"aberta": true` e nenhuma opção.
- **`decidido`:** o que você decidiu sem perguntar e que ele precisa conhecer: decisão técnica que passa no teste abaixo e decisão que uma fala dele já responde. Cada item com `porque` e `fonte` (a fala dele, com a data, ou o `arquivo:linha`). Ele concorda ou discorda na tela, e é isso que evita perguntar de novo o que ele já disse.

**O que vira pergunta.** Antes de cada uma, teste: "se a resposta fosse a outra, o código ou o escopo mudaria? E o que o usuário já disse resolve?". Pergunte se mudaria e o que ele disse não resolve. Se uma fala dele resolve, o item vai para `decidido`, citando a fala. As perguntas são da tarefa e ancoradas no código, nunca genéricas:

- Ruim: "Como você quer tratar erros?"
- Bom: "`calcularFrete` hoje devolve 0 para carrinho vazio, e o novo fluxo chama ele antes da validação. Mantemos o 0 ou passamos a lançar `CarrinhoVazioError`?"

**Tipos de pergunta (`tema`):**

- **`produto`:** o que o usuário final vê ou faz (texto, fluxo de tela, valor pré-preenchido, o que aparece ou some, regra de negócio, o que acontece quando dá errado). Uma pergunta para cada decisão, com um exemplo concreto em cada opção.
- **`desenho`:** a decisão técnica que muda o que o usuário vê, contraria uma decisão registrada (ADR, `CLAUDE.md`) ou afeta o trabalho de outras pessoas. Diga qual decisão registrada ela contraria. As outras decisões técnicas (onde fica o código, que padrão seguir, nome, estrutura de teste) você toma e põe em `decidido` se ele precisar saber, ou só no plano.
- **`escopo`:** a correção na raiz sai do escopo (toca outro módulo, muda um contrato, afeta outros usos). Opções: corrigir na raiz × remendo consciente, com o que cada uma afeta.
- **`incerteza`:** a incerteza empírica relevante. Uma pergunta com a **meta** (ex.: "eval 7/7 com 2 repetições"), o **orçamento** (rodadas, custo), o **plano B** se o orçamento acabar (ex.: "tirar a decisão do prompt e passar para código") e **quem roda**.
- **`entrega`:** fixa, em toda tarefa: o que fazer com o git no final, para que nenhum push ou PR aconteça sem ele querer. Opções: "Só commits na branch" (ele faz push e PR), "Push da branch" e "Push + PR para `<integração>`".

**Regra que o usuário escreveu** (formato, faixa, texto) não vira pergunta com reinterpretações dela como opções. Ela vai para a spec ao pé da letra, onde ele disse. Só pergunte o que a regra não responde.

**Sem tela quando não precisa.** Se a única pergunta for a de entrega, faça-a no chat (AskUserQuestion) e vá direto para a spec. Mudança trivial nem chega aqui (ver "Fluxo" no `SKILL.md`).

**Ao receber as respostas** (`discovery.respostas.json`):

1. **Comentário que é pergunta ou dúvida** ("não entendi", "mas como fica X?", "que tool?"): responda no chat, em linguagem simples, antes de qualquer outra coisa. Não grave nada em arquivo no lugar de responder.
2. **Entendeu errado** (`ENT`): corrija o entendimento antes de tudo e refaça as perguntas que dependiam dele; as respostas dadas em cima do entendimento errado não valem até ele confirmar de novo.
3. **Discordo, outra resposta ou correção de desenho** (o quê, onde ou como): atualize o `discovery.json`, suba a `versao` e abra nova rodada só com o que mudou ou o que a correção criou. Até duas rodadas é o normal numa tarefa com fluxo novo; não economize a segunda.
4. **Tudo respondido** (com o entendimento certo): siga para a spec.

## 5. Spec

A spec é o contrato: **o quê e por quê**, sem o como. Ela nasce do pedido, da pesquisa e das respostas do discovery, e não traz pergunta nem decisão em aberto. Escreva `spec.json` seguindo `modelos/spec.json`.

- **`problema`:** o que está errado ou faltando, em até 3 linhas.
- **`objetivos`** (O1, O2…): o que o usuário quer alcançar, tirado do pedido e da dor dele, fiel às palavras e aos números dele. Sem objetivo novo que ele não deu.
- **`requisitos`** (R1, R2…): cada um uma coisa só, verificável, com:
  - `tipo`: `comportamento` (o que acontece em uma situação), `requisito` (o que precisa existir ou valer) ou `restricao` (o que não pode mudar ou acontecer);
  - `texto`: na forma "Quando <situação>, o sistema <resposta>" para comportamento; em linguagem do domínio, sem nome de função, campo ou status;
  - `exemplo`: o que o usuário final vê, concreto (esperado, com valores);
  - `porque`: o que ele resolve;
  - `origem`: os objetivos que ele serve;
  - `aderencia` e `justificativa`: se ele **bate** com o objetivo de origem, é **parcial** (cobre só parte, ou vai além do pedido) ou **não bate** (exigido por outra coisa, como um efeito colateral ou uma decisão do discovery), com a justificativa em uma frase. Seja honesto: `parcial` e `nao_bate` são o que mostra a ele o escopo que cresceu;
  - `nao_cobre`: o que este requisito deixa de fora na mesma família (outros estados, outras falas, outros casos vizinhos). Em correção estrutural, liste a superfície que continua sem cobertura;
  - `criterio`: como se verifica (o teste, o cenário do eval, o passo na tela);
  - `prova` (opcional): o detalhe técnico, recolhido na tela.
- **`fora_de_escopo`** (F1, F2…): o que fica de fora, cada um com o porquê. Ele também aprova.
- **`decisoes`:** o resumo das respostas do discovery, só para leitura.

Objetivo sem requisito é uma lacuna: cubra, ou marque `"lacuna"` no objetivo com o motivo. O script recusa a spec com objetivo descoberto.

**Antes de abrir a tela, confira cada requisito:** dá para verificar? Tem uma leitura só? O exemplo é concreto? A origem é real? Ele descreve o quê, e não o como (nome de arquivo, função ou estrutura vai para o plano)? Ele contradiz uma resposta do discovery? O tamanho acompanha a tarefa: um bug pequeno tem de 2 a 5 requisitos, não 16.

**Ao receber as respostas** (`spec.respostas.json`):

1. **Comentário que é pergunta:** responda no chat antes de qualquer outra coisa, como no discovery.
2. **Ajustar ou rejeitar:** redesenhe a spec. Não é remendo no item: releia o objetivo e a justificativa, porque um requisito rejeitado pode mudar outros. Suba a `versao` e abra nova rodada. A tela fecha sozinha os itens aprovados que não mudaram e marca o que mudou.
3. **Tudo aprovado** (todo requisito e todo fora de escopo com `aprovado`): commite `discovery.json`, `spec.json` e as respostas, e siga para o plano. Item sem resposta não está aprovado.

## 6. Plano

Escreva `plano.md` a partir de `modelos/plano.md`. O plano não passa por aprovação do usuário: ele aprovou o contrato, e o plano é como cumpri-lo.

- **Decisões:** as do discovery, com a resposta do usuário, e as técnicas que você tomou, marcadas "(decidido por mim)", cada uma com o porquê.
- **Tarefas:**
  - cada uma é uma ação verificável, não um tema, e cabe num passo de trabalho (se vai encostar em oito arquivos, quebre);
  - cada uma diz em `Atende:` os requisitos que cumpre, e em `Como:` o que fazer. **Todo requisito aprovado aparece em pelo menos um `Atende:`;** confira antes de fechar;
  - ordem por dependência **e por risco**: a sondagem da maior incerteza vem primeiro, antes de construir em volta dela;
  - branch, push, PR e code review **não são tarefas**: a branch já existe (passo 1), o review roda no fim de cada fase e push e PR são da entrega (`referencias/entrega.md`);
  - cada uma declara como é verificada: `Teste:` (escrito antes, TDD), ou `Verificar por:` com um comando ou passo concreto e o motivo de não ter teste, ou, se for empírica, `Meta:`, `Orçamento:` e `Se esgotar:`;
  - a que o usuário executa leva `Quem roda: dev` e o motivo (custo de LLM que ele aprova, credencial ou ambiente dele, prova na tela). Sem a marca, quem roda é você.
- **Fases:** só se houver mais de umas 8 tarefas ou não couber numa sessão. Cada fase entrega algo funcionando, termina com um critério claro e passa por um code review.
- **Pronto quando:** cada requisito verificado pelo `criterio` dele, e o passo a passo da validação manual para o usuário, com o requisito de cada passo.
- **Curto.** Seção sem conteúdo fica "nenhuma". O plano é o mais curto que se basta.

## 7. Fechar

1. Crie o `estado.md` a partir de `modelos/estado.md`, com todas as tarefas `pendente` (inclusive a linha Entrega, no fim) e o próximo passo apontando para a primeira.
2. Commite o `plano.md` e o `estado.md` na branch da tarefa, seguindo a convenção do `projeto.md`.
3. Diga em até 3 linhas o caminho do plano: fases, a maior incerteza e quem roda o quê. O quê e o porquê ele já aprovou; não repita.
4. Faça o handoff (`referencias/handoff.md`). Sempre, mesmo com plano curto: você não mede o próprio contexto, e a execução rende mais numa sessão limpa.

## A tela de revisão

O script `scripts/revisao.py` valida o JSON da etapa, serve a página (`modelos/revisao.html`) e espera o usuário. Cada mudança na página vira rascunho (`<etapa>.rascunho.json`). Ao clicar em Enviar, ele grava `<etapa>.respostas.json`, imprime o resumo das respostas e encerra.

1. **Rode em segundo plano** (Bash com `run_in_background: true`):
   `python3 <pasta da skill>/scripts/revisao.py .trilho/tarefas/<slug> discovery` (ou `spec`).
   Ele tenta abrir o navegador sozinho (no WSL, o do Windows). Saída 2 é erro no JSON: o stderr lista cada um; corrija e rode de novo.
2. **Avise em uma ou duas linhas**: o endereço que ele imprimiu e o que pede atenção (ex.: "2 requisitos marcados ⚠️ parcial"). Nada do conteúdo da tela no chat. Termine o turno.
3. **O encerramento do script é o aviso** de que as respostas chegaram: leia o resumo da saída e o `<etapa>.respostas.json`, e siga o "Ao receber as respostas" da etapa. Não pergunte se ele terminou.
4. **Se ele responder no chat em vez da tela**, trate a resposta do chat como resposta, registre no próximo JSON o que ela decidiu e **desligue o servidor** que ficou esperando (TaskStop no processo em segundo plano, ou `kill $(cat <pasta>/<etapa>.pid)`). Sem perguntar: servidor esquecido rodando é trabalho que ele não pediu.
5. **Nova rodada:** edite o JSON, suba a `versao` e rode o script de novo. Ele derruba sozinho o servidor anterior da mesma etapa, e os itens já aprovados e sem mudança aparecem fechados.
6. **Ao sair do planejamento** (plano escrito, handoff, ou o usuário mudou de assunto), confira que nenhum servidor da tarefa ficou de pé (`ls <pasta>/*.pid`) e desligue o que sobrou. Ele também encerra sozinho depois de 4 horas sem acesso.

Commite o JSON da etapa e as respostas. O `<etapa>.rascunho.json` e o `<etapa>.pid` são temporários e não entram no commit.

No OpenCode, sem aviso de processo em segundo plano: rode com `nohup … &`, mostre o endereço e peça que ele diga "respondi" depois de enviar. Aí leia o `<etapa>.respostas.json`.
