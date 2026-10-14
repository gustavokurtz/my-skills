---
name: trilho
description: Workflow de desenvolvimento que explora o código, pergunta só o que muda a solução, escreve um roteiro executável e executa com autonomia (TDD, handoff entre sessões, code review). Use quando o usuário pedir para planejar ("vamos planejar", "planeja isso", "cria o roteiro"), executar ou continuar ("executa", "continua de onde paramos", "onde paramos?", "continua <slug>"), fazer handoff de uma tarefa do trilho ("handoff", "vou dar clear", "salva onde paramos") ou mencionar uma tarefa em `.trilho/`. Não use para perguntas, explicações ou edições pontuais que o usuário não pediu para planejar.
---

# Trilho

O usuário já disse o que quer. Seu trabalho é entender o código, perguntar só o que muda a solução, escrever um roteiro que uma sessão nova executa sem perguntar nada, e executar com autonomia. O estado do trabalho vive em `.trilho/`, não na conversa.

## Dois tipos de incerteza

- **De decisão:** o que o usuário quer. Some perguntando, no planejamento.
- **Empírica:** o que o sistema vai fazer de fato. Só some rodando. Exemplos: comportamento de LLM (prompt, juiz, tool, eval), performance, integração externa instável, bug sem causa conhecida.

Planejar por mais tempo não reduz a incerteza empírica. Descubra cedo e barato: a sondagem da maior incerteza vem antes de construir em volta dela, e a iteração tem meta e orçamento combinados no roteiro, em vez de virar exceção a cada rodada.

## Antes de tudo: o projeto

Leia `.trilho/projeto.md`. Ele é a fonte da verdade para comandos de teste, lint, typecheck e build, convenção de commit, branch de integração, regras fixas e armadilhas do projeto.

Se o arquivo não existir, diga ao usuário que `/trilho-init` cria esse arquivo e pergunte se ele quer rodar agora. Se não quiser, descubra só o mínimo que a tarefa precisa (comando de teste, padrão de commit pelo `git log`) e siga sem gravar nada.

## Fluxo

```
branch → explorar → perguntar (entrega + 0 a N) → roteiro.md → [handoff + /clear, se o contexto pesou] → executar (code review a cada fase) → entrega (verificação, push/PR)
```

É um fluxo só, para qualquer tamanho. O que muda é a profundidade de cada passo: uma tarefa pequena tem zero perguntas e um roteiro de 15 linhas; uma grande tem várias fases e alguns handoffs. Mudança trivial (uma linha, um texto, formatação): faça direto e avise que não abriu roteiro.

Ao entrar em cada passo, leia a referência dele. Os caminhos `referencias/` e `modelos/` desta skill ficam em `${CLAUDE_SKILL_DIR}`.

| Passo | Referência |
|---|---|
| planejamento | `referencias/planejamento.md` |
| execução | `referencias/execucao.md` |
| handoff | `referencias/handoff.md` |
| entrega | `referencias/entrega.md` |

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
- a ação é destrutiva, irreversível ou toca banco ou serviço remoto;
- uma ambiguidade mudaria o resultado e nada do que o usuário disse resolve.

Todo o resto (detalhe de implementação, teste que precisou ir para outro arquivo, mais uma rodada dentro do orçamento): decida, registre no `estado.md` e siga. Divergência não se resolve em silêncio, mas também não precisa de aprovação.

## Regras que valem sempre

- **Siga o padrão local.** Antes de criar algo, procure código parecido no repo e siga o padrão que já existe.
- **A menor solução que resolve.** Se uma abstração, opção de configuração ou camada extra não é exigida pelo pedido, ela não entra.
- **Teste que confere texto de prompt não prova comportamento.** Ele prova que você escreveu a frase, não que o modelo obedece. Para comportamento de LLM, a evidência é a rodada real (eval, trace).
- **Teste que já existia quebrou:** conserte a causa, não o teste. Se o teste estiver errado, diga isso ao usuário em vez de ajustá-lo em silêncio.
- **Nunca commite deixando vermelho um teste que estava verde.** Se o usuário pedir explicitamente para commitar assim, registre no corpo do commit o que está falhando.

## Armadilhas

Falhas que já aconteceram e custaram retrabalho.

- **Branch rastreando a integração.** `git switch -c <branch> origin/<integração>` configura a integração como upstream da branch nova: o `git status` mostra "ahead of origin/<integração>" e o `git pull` traz a integração. Crie com `--no-track`; o upstream vem no `git push -u` da entrega.
- **Rodadas de ajuste sem meta.** Uma tarefa determinística que vira empírica no meio (o teste passa, mas o comportamento real não) leva a ajustes emendados sem fim, com um pedido de desvio a cada rodada. Não emende: proponha ao usuário, uma vez, meta, orçamento e plano B, registre no roteiro e siga como tarefa empírica.
- **Verde no arquivo, vermelho na suíte.** O teste da tarefa passar não fecha a fase. Verde é a suíte do `projeto.md`, não o arquivo que você rodou.
- **Implementar durante o planejamento.** O roteiro registra decisões (o quê, onde, como verificar), não o código. Se está escrevendo implementação no roteiro, volte ao nível de decisão.
- **Referência perdida depois de compactar.** Depois de um `/compact`, este arquivo volta ao contexto, mas as referências lidas antes não. Releia a referência do passo atual antes de seguir.
