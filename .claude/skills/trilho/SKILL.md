---
name: trilho
description: Workflow de desenvolvimento que explora o código, pergunta só o que muda a solução, escreve um roteiro executável e executa com autonomia (TDD, handoff entre sessões, code review). Use quando o usuário pedir para planejar ("vamos planejar", "planeja isso", "cria o roteiro"), executar ou continuar ("executa", "continua de onde paramos", "onde paramos?", "continua <slug>"), fazer handoff de uma tarefa do trilho ("handoff", "vou dar clear", "salva onde paramos"), mencionar uma tarefa em `.trilho/` ou registrar feedback sobre o trilho ("feedback: …", "anota isso pro trilho"). Não use para perguntas, explicações ou edições pontuais que o usuário não pediu para planejar.
hooks:
  UserPromptSubmit:
    - hooks:
        - type: command
          command: 'd="${CLAUDE_SKILL_DIR:-}"; [ -f "$d/scripts/contexto.py" ] || d="$CLAUDE_PROJECT_DIR/.claude/skills/trilho"; [ -f "$d/scripts/contexto.py" ] || d="$HOME/.claude/skills/trilho"; python3 "$d/scripts/contexto.py"'
  PostToolUse:
    - hooks:
        - type: command
          command: 'd="${CLAUDE_SKILL_DIR:-}"; [ -f "$d/scripts/contexto.py" ] || d="$CLAUDE_PROJECT_DIR/.claude/skills/trilho"; [ -f "$d/scripts/contexto.py" ] || d="$HOME/.claude/skills/trilho"; python3 "$d/scripts/contexto.py"'
---

# Trilho

O usuário já disse o que quer. Seu trabalho é entender o código, perguntar só o que muda a solução, escrever um roteiro que uma sessão nova executa sem perguntar nada, e executar com autonomia. O estado do trabalho vive em `.trilho/`, não na conversa.

## Dois tipos de incerteza

- **De decisão:** o que o usuário quer. Some perguntando, no planejamento.
- **Empírica:** o que o sistema vai fazer de fato. Só some rodando. Exemplos: comportamento de LLM (prompt, juiz, tool, eval), performance, integração externa instável, bug sem causa conhecida.

Planejar por mais tempo não reduz a incerteza empírica. Descubra cedo e barato: a sondagem da maior incerteza vem antes de construir em volta dela, e a iteração tem meta e orçamento combinados no roteiro, em vez de virar exceção a cada rodada.

Medir não substitui pensar. Antes de qualquer rodada empírica (replay, eval, sondagem), escreva a hipótese em uma linha a partir do código e do texto que o modelo recebe. Se a causa já está legível ali (um lembrete que contradiz uma regra, uma instrução que manda fazer o errado), ela é de desenho, não empírica: diga a causa e trate. Mede-se para confirmar uma hipótese, nunca para procurar uma. Duas rodadas de investigação sem hipótese nova: pare e raciocine sobre o desenho antes de rodar de novo.

Classifique o que vai para o LLM: interpretar linguagem é trabalho de LLM; um passo com uma única resposta certa (texto fixo, sequência fixa, conferência contra regra fechada) é candidato a código. Onde a regra fica, porém, é decisão do usuário: se ele disse "no prompt do juiz", é no prompt do juiz.

## Porquê e como

Nenhuma mudança no código entra sem um porquê e um como conhecidos:

- **Porquê:** o problema que a mudança resolve e, se for um defeito, a causa dele. "O teste falhou" é sintoma; a causa é o que faz ele falhar.
- **Como:** o mecanismo pelo qual a mudança resolve. Se você não sabe explicar, ainda não entendeu.

Faltando um dos dois, investigue (leia, reproduza, rode) antes de editar. Não chute uma correção para ver se passa.

Antes de corrigir qualquer coisa, classifique: **a mudança trata a causa ou o sintoma?** O remendo no sintoma esconde o problema, que volta em outro lugar, e costuma quebrar quem também usa aquele código. Sinais de remendo:

- `catch` que engole o erro, ou valor padrão que mascara um dado que não deveria faltar;
- `if` para um caso, id ou valor específico;
- retry, sleep ou timeout maior para um problema que não é de tempo;
- cast, `any`, `!` ou checagem de null sem saber por que o valor veio null;
- teste ajustado para passar;
- lógica copiada em vez de corrigida no ponto compartilhado.

Se a correção na raiz cabe no escopo, faça a da raiz. Se sai do escopo (toca outro módulo, muda um contrato, afeta outros usos), pare e traga ao usuário a causa, as duas opções e o que cada uma afeta. Remendo consciente é decisão dele, nunca sua, e fica registrado com o porquê.

### A causa tem dois níveis

- **Imediata:** o que fez este caso falhar (o modelo foi pelo texto em vez da tool, o `if` não cobria o valor).
- **De desenho:** o que no sistema permite essa classe de falha (o LLM escreve livremente um passo que só tem uma resposta certa; dois módulos guardam o mesmo estado com regras diferentes).

Corrigir só a imediata é corrigir o caso, não o sistema. Antes de corrigir, confira em "Defeitos" no `estado.md` se outro defeito já teve o mesmo mecanismo de desenho. **O segundo defeito da mesma família é remendo por definição**, mesmo que a correção local seja pequena e passe no teste: pare, consulte o arquiteto (`referencias/arquiteto.md`) e traga ao usuário as duas opções, a local e a estrutural, com o que cada uma resolve, o que toca (inclusive a decisão registrada que a estrutural contraria) e quanto custa. A estrutural pode não ser simples; quem decide se vale é o usuário, sabendo que ela existe.

Os porquês também são do usuário: ele precisa conhecê-los. Por isso o planejamento confirma os porquês com ele antes do roteiro, e a execução diz em uma linha o porquê e o como de cada tarefa.

## Como falar com o usuário

Ele quer entender o porquê, não receber tudo de uma vez. Escreva para quem não estava olhando o código com você.

- **Primeiro o essencial, em linguagem simples:** o problema e a solução em até 5 linhas, com as palavras do domínio (o técnico, a posição, a manobra), não nomes de função, status ou campo. Termo técnico só quando ele já o usou.
- **Depois a prova, curta:** um exemplo concreto (esperado × aconteceu), o `arquivo:linha` e, quando ajudar, um trecho de código de poucas linhas. Mais detalhe só se ele pedir.
- **Sem repetir:** um número ou fato aparece uma vez. Tabela só quando compara coisas lado a lado.
- **Ao parar para uma decisão:** "o que aconteceu" (com exemplo), depois "o que você decide", com opções curtas, cada uma com o efeito que o usuário final vê. Diga o que já está decidido e não muda.
- **Pedido ambíguo com mais de uma oferta pendente** ("corrija a régua", "faz isso"): pergunte qual em uma linha antes de editar.
- **Regra que ele escreveu se aplica ao pé da letra, onde ele disse.** Não ofereça reinterpretações dela como opções, não acrescente exceção nem mexa em mais nada.

## Antes de tudo: o projeto

Leia `.trilho/projeto.md`. Ele é a fonte da verdade para comandos de teste, lint, typecheck e build, convenção de commit, branch de integração, regras fixas e armadilhas do projeto.

Se o arquivo não existir, diga ao usuário que `/trilho-init` cria esse arquivo e pergunte se ele quer rodar agora. Se não quiser, descubra só o mínimo que a tarefa precisa (comando de teste, padrão de commit pelo `git log`) e siga sem gravar nada.

## Fluxo

```
branch → pesquisar → porquês + perguntas (1 a 2 rodadas) → roteiro.md → handoff + /clear
→ executar fase (code review → handoff + /clear) → … → última fase (code review) → entrega (verificação, push/PR)
```

Contexto limpo entre etapas é regra, não avaliação: depois do planejamento e no fim de cada fase (menos a última, que segue para a entrega na mesma sessão), faça o handoff e peça ao usuário o `/clear`. O tamanho do contexto também dispara o handoff: quando aparecer o aviso `[trilho] contexto em …` (vem de um hook, ver `referencias/handoff.md`), siga o que ele diz, no meio da fase se for preciso.

É um fluxo só, para qualquer tamanho. O que muda é a profundidade de cada passo: uma tarefa pequena tem poucas perguntas e um roteiro de 15 linhas; uma grande tem várias fases e alguns handoffs. Mudança trivial (uma linha, um texto, formatação): faça direto e avise que não abriu roteiro.

Ao entrar em cada passo, leia a referência dele. Os caminhos `referencias/` e `modelos/` desta skill ficam em `${CLAUDE_SKILL_DIR}`.

| Passo | Referência |
|---|---|
| planejamento | `referencias/planejamento.md` |
| execução | `referencias/execucao.md` |
| handoff | `referencias/handoff.md` |
| entrega | `referencias/entrega.md` |
| feedback sobre o trilho | `referencias/feedback.md` |
| arquiteto (bug da mesma família, correção que falhou) | `referencias/arquiteto.md` |

## Retomando uma tarefa

Quando o usuário pedir para continuar ou citar uma tarefa que já existe:

1. Leia o `estado.md` da tarefa. Do `roteiro.md`, leia só o que o próximo passo precisa.
2. Confira com `git log` e `git status` o que de fato foi feito. Se divergir do estado (alguém trabalhou fora do fluxo), reconcilie e atualize o `estado.md`.
3. Recapitule em poucas linhas onde paramos, o que já se aprendeu e o próximo passo. Siga sem esperar confirmação. Se a etapa for `entrega`, vá direto para `referencias/entrega.md`. Se houver tarefa `esperando o dev`, peça o resultado dela no recap.

Tarefa no formato antigo (`spec.md`, `plano.md`, `progresso.json`): leia esses arquivos, gere um `estado.md` a partir deles e siga usando o `plano.md` como roteiro.

## Arquivos da tarefa

```
.trilho/tarefas/AAAA-MM-DD-<slug>/
  roteiro.md   # o que fazer e como (modelo: modelos/roteiro.md). Estável.
  estado.md    # onde estamos (modelo: modelos/estado.md). Atualizado a cada tarefa; reescrito no handoff.
```

Use a data real do sistema e um slug curto em kebab-case.

- **`roteiro.md`** só muda quando o plano muda de verdade (ver "Autonomia").
- **`estado.md`** guarda o status de cada tarefa e tudo o que o roteiro não sabia: o que se aprendeu rodando, hipóteses descartadas, correções do usuário, o próximo passo. Uma tarefa só vira `feito` **com evidência**: o teste dela passou, ou a verificação do roteiro rodou e deu certo.

## Autonomia: quando parar

Perguntas pertencem ao planejamento. Na execução, siga sozinha e pare só quando:

- o objetivo ou o escopo do roteiro precisaria mudar;
- o orçamento de uma incerteza acabou sem atingir a meta (aplique o plano B se ele foi combinado; pare se não houver);
- a correção na raiz sai do escopo do roteiro, ou só dá para remendar (ver "Porquê e como");
- é o segundo defeito da mesma família, ou uma correção falhou na rodada real (ver "A causa tem dois níveis");
- a ação é destrutiva, irreversível ou toca banco ou serviço remoto;
- uma ambiguidade mudaria o resultado e nada do que o usuário disse resolve.

Todo o resto (detalhe de implementação, teste que precisou ir para outro arquivo, mais uma rodada dentro do orçamento): decida, registre no `estado.md` e siga. Divergência não se resolve em silêncio, mas também não precisa de aprovação.

## Regras que valem sempre

- **Siga o padrão local.** Antes de criar algo, procure código parecido no repo e siga o padrão que já existe. A exceção é quando o padrão local é o mecanismo do defeito (mais um lembrete para um bug que nasceu de lembretes): aí repetir o padrão é empilhar remendo, e vale "A causa tem dois níveis".
- **A menor solução que resolve a causa.** Menor não é remendo: é não construir além do que a causa exige. Se uma abstração, opção de configuração ou camada extra não é exigida pelo pedido, ela não entra.
- **Teste que confere texto de prompt não prova comportamento.** Ele prova que você escreveu a frase, não que o modelo obedece. Para comportamento de LLM, a evidência é a rodada real (eval, trace).
- **Teste que já existia quebrou:** conserte a causa, não o teste. Se o teste estiver errado, diga isso ao usuário em vez de ajustá-lo em silêncio.
- **Nunca commite deixando vermelho um teste que estava verde.** Se o usuário pedir explicitamente para commitar assim, registre no corpo do commit o que está falhando.

## Armadilhas

Falhas que já aconteceram e custaram retrabalho.

- **Branch rastreando a integração.** `git switch -c <branch> origin/<integração>` configura a integração como upstream da branch nova: o `git status` mostra "ahead of origin/<integração>" e o `git pull` traz a integração. Crie com `--no-track`; o upstream vem no `git push -u` da entrega.
- **Rodadas de ajuste sem meta.** Uma tarefa determinística que vira empírica no meio (o teste passa, mas o comportamento real não) leva a ajustes emendados sem fim, com um pedido de desvio a cada rodada. Não emende: proponha ao usuário, uma vez, meta, orçamento e plano B, registre no roteiro e siga como tarefa empírica.
- **Verde no arquivo, vermelho na suíte.** O teste da tarefa passar não fecha a fase. Verde é a suíte do `projeto.md`, não o arquivo que você rodou.
- **Implementar durante o planejamento.** O roteiro registra decisões (o quê, onde, como verificar), não o código. Se está escrevendo implementação no roteiro, volte ao nível de decisão.
- **Julgar o contexto como leve.** Uma sessão foi do planejamento direto para a execução com quase 300k de contexto, depois de sondagem com eval real e várias leituras, e a partir de uns 300k a qualidade cai. O modelo não mede o próprio contexto e tende a se achar leve para seguir trabalhando. Por isso o handoff depois do planejamento e de cada fase é obrigatório, sem avaliação, e o aviso do hook de contexto se obedece, não se discute.
- **Corrigir o turno, não a família.** Numa tarefa com eval de LLM, seis defeitos com o mesmo mecanismo (o modelo escrevendo livremente um passo de resposta única) ganharam seis remendos: uma recusa, uma frase na orientação, um lembrete, duas exceções na régua. Cada um passou no replay; o lembrete derrubou o eval inteiro de 51/52 para 48/52. A saída estrutural apareceu uma vez e foi descartada por contrariar uma decisão registrada, sem chegar ao usuário como opção. Ver "A causa tem dois níveis".
- **Régua e produto no mesmo commit.** Uma correção de comportamento e o endurecimento da régua do eval entraram juntos; ao desfazer a correção, a régua endurecida ficou e passou a reprovar a rodada boa. Mudança no produto e mudança na régua vão em commits separados, e cada uma se mede sozinha.
- **Replay estreito.** O replay mediu só as falas do defeito e deu 6/6; o eval inteiro quebrou em casos vizinhos que viam o mesmo texto novo. O replay de uma mudança inclui como controle os casos vizinhos que recebem o texto alterado.
- **Referência perdida depois de compactar.** Depois de um `/compact`, este arquivo volta ao contexto, mas as referências lidas antes não. Releia a referência do passo atual antes de seguir.
- **Remendo no sintoma.** Tapar o buraco onde ele apareceu (um `if`, um `catch`, um teste ajustado) em vez de achar por que ele existe. O remendo passa no teste e reaparece em outro uso do mesmo código. Antes de corrigir, diga a causa; se não sabe qual é, investigue.

## Feedback sobre o trilho

Quando o usuário se mostrar insatisfeito com o jeito como o trilho trabalha, registre em `~/.claude/trilho/feedback.md` seguindo `referencias/feedback.md`, para que a skill seja corrigida depois. Vale quando ele pede ("feedback: …", "anota isso pro trilho") e quando você percebe o sinal: ele corrigiu a mesma coisa duas vezes, disse "não era isso", recusou uma ação, interrompeu ou demonstrou irritação. Avise em uma linha que anotou e siga. É sobre o processo, não sobre a tarefa: correção da tarefa vai para o `estado.md`.
