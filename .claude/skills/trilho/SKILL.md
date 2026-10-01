---
name: trilho
description: Workflow de desenvolvimento com triagem, entrevista, spec, plano com tracking, TDD e code review. Use quando o usuário pedir para planejar uma tarefa ("vamos planejar", "planeja isso", "cria o plano", "cria a spec"), executar ou continuar um plano ("executa o plano", "continua de onde paramos", "onde paramos?"), ou mencionar uma spec, plano ou tarefa em `.trilho/`. Não use para perguntas, explicações ou edições pontuais que o usuário não pediu para planejar.
---

# Trilho

Perguntas certas antes do código economizam rodadas de correção depois. O estado do trabalho vive em arquivos dentro de `.trilho/`, não na conversa: qualquer sessão (sua ou de outra pessoa) retoma o trabalho só lendo esses arquivos.

## Antes de tudo: o projeto

Leia `.trilho/projeto.md`. Ele é a fonte da verdade para comandos de teste, lint, typecheck e build, convenção de commit, branch de integração e regras fixas do projeto.

Se o arquivo não existir, diga ao usuário que `/trilho-init` cria esse arquivo e pergunte se ele quer rodar agora. Se não quiser, descubra só o mínimo que a tarefa precisa (comando de teste, padrão de commit pelo `git log`) e siga sem gravar nada.

## Retomando uma tarefa

Quando o usuário mencionar uma tarefa, spec ou plano que já existe, ou pedir para continuar:

1. Leia `progresso.json`, `plano.md` e `spec.md` (se existir) da tarefa.
2. Confira com `git log` e `git status` o que de fato foi feito. Se alguém trabalhou fora do fluxo, o progresso pode estar desatualizado; nesse caso, reconcilie.
3. Recapitule em poucas linhas onde paramos (etapa, fase, última tarefa concluída) e qual é o próximo passo.
4. Siga pela referência da etapa atual (tabela abaixo).

## Triagem (tarefa nova)

Primeiro, explore o código que a tarefa toca: o suficiente para diagnosticar, não para planejar. Depois classifique:

- **Fluxo grande:** várias questões em aberto, vários problemas ou várias features; decisões de escopo ou de design que o usuário precisa tomar.
- **Fluxo pequeno:** um problema só, com solução clara no contexto do código atual; no máximo dúvidas pontuais.
- **Sem trilho:** mudança de uma linha, texto ou formatação. Vá direto ao código.

Apresente o diagnóstico com AskUserQuestion. A rota recomendada vem primeiro, com "(Recomendado)", e a descrição diz o porquê ("toca checkout e frete, e há duas decisões de escopo em aberto"). Quem decide é o usuário.

Decidida a rota (grande ou pequeno), crie a pasta da tarefa e o `progresso.json`.

## Fluxos

```
Grande:   entrevista → spec (GATE 1) → plano (GATE 2) → /clear → execução → entrega
Pequeno:                               plano (GATE)    →         execução → entrega
```

O fluxo pequeno faz tudo que o grande faz, menos a entrevista e a spec. Ele continua explorando o código e perguntando o que bloquear o plano.

Ao entrar em cada etapa, leia a referência dela:

| Etapa | Referência |
|---|---|
| entrevista | `referencias/entrevista.md` |
| spec | `referencias/spec.md` |
| plano | `referencias/plano.md` |
| execucao | `referencias/execucao.md` |
| entrega | `referencias/entrega.md` |

## Arquivos da tarefa

```
.trilho/tarefas/AAAA-MM-DD-<slug>/
  spec.md          # só no fluxo grande (modelo: modelos/spec.md)
  plano.md         # modelos/plano.md
  progresso.json   # modelos/progresso.json
```

Use a data real do sistema e um slug curto em kebab-case.

**`progresso.json` guarda só ids e status.** O conteúdo de cada tarefa vive no `plano.md`, e o JSON não repete nada dele. Isso existe porque um JSON enxuto é difícil de reescrever por engano, e porque ele responde rápido a pergunta "onde paramos?". Altere apenas:

- `etapa`: ao passar de uma etapa para a próxima (`entrevista`, `spec`, `plano`, `execucao`, `entrega`, `concluida`).
- `tarefas`: preenchida quando o plano é aprovado. Cada item tem `id`, `fase` e `passou`.
- `passou`: vira `true` **só com evidência**: o teste da tarefa passou, ou a verificação alternativa justificada no plano foi executada e deu certo.

## Regras que valem em todas as etapas

- **Gates são aprovação explícita.** Não avance de etapa com gate pendente.
- **Divergência não se resolve em silêncio.** Quando a realidade divergir do plano: pare, analise, proponha o ajuste, espere aprovação e só então execute (detalhes em `referencias/execucao.md`).
- **Siga o padrão local.** Antes de criar algo, procure código parecido no repo e siga o padrão que já existe.
- **A menor solução que resolve.** Se uma abstração, opção de configuração ou camada extra não é exigida por um requisito, ela não entra.
- **Nunca commite com teste quebrado.** Se o usuário pedir explicitamente para commitar assim, registre no corpo do commit o que está falhando.
