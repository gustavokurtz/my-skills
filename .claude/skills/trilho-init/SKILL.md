---
name: trilho-init
description: Inicializa o Trilho no projeto atual. Descobre comandos de teste, lint, typecheck e build, convenções de código e de commit e regras fixas do projeto, e grava tudo em `.trilho/projeto.md`. Rodar uma vez por projeto, ou de novo quando o projeto mudar.
disable-model-invocation: true
---

# Trilho — init

Monte o `.trilho/projeto.md`, a fonte da verdade que o `trilho` lê antes de qualquer tarefa. O desenvolvedor não deveria precisar entregar nada de bandeja: **descubra tudo o que o repo responde** e pergunte só o que não dá para inferir.

## 1. Já existe?

Se `.trilho/projeto.md` já existe, isto é uma atualização. Descubra tudo de novo, compare com o arquivo, mostre só o que mudou e atualize.

## 2. Descobrir

Leia, sem perguntar:

- **Comandos:** scripts do `package.json`, `Makefile`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `composer.json` etc. Os workflows de CI (`.github/workflows/`, `.gitlab-ci.yml`) são a melhor prova de quais comandos rodam de verdade.
- **Testes:** framework, onde ficam, como são nomeados e como rodar um arquivo só.
- **Lint, format e typecheck.**
- **Branch de integração:** a branch padrão do remoto e o padrão das branches existentes.
- **Commits:** `git log --oneline -30`. Identifique a convenção, o idioma e se o repo usa coautoria ou emoji.
- **Regras escritas:** `CLAUDE.md`, `CONTRIBUTING.md`, `README`, ADRs.
- **Stack e estrutura:** onde ficam rotas, serviços, modelos e testes. Para cada padrão, um arquivo de referência.
- **Áreas sensíveis:** migrations, seeds e scripts que falam com banco ou serviço externo. Para cada um, descubra para onde aponta.

## 3. Validar

Rode o comando de teste uma vez para confirmar que funciona. **Antes, verifique para onde ele aponta:** se o teste toca um banco ou serviço que não é local, pergunte antes de rodar.

## 4. Lacunas

- **Sem testes:** sugira criar o setup mínimo idiomático da stack (framework, um teste de exemplo, o script). Se o usuário não quiser, registre isso no `projeto.md`, reaproveite o que existir e siga. Nesse caso, as tarefas do trilho vão usar verificação alternativa justificada.
- **Sem lint ou typecheck:** a mesma coisa. Sugira, e se o usuário recusar, registre e siga.

## 5. Regras fixas

Mostre as convenções que você descobriu e pergunte só o que o repo não responde. Use AskUserQuestion quando der para dar opções, e texto quando a pergunta for aberta. Por exemplo:

- o que nunca deve ser feito neste projeto;
- quais áreas exigem cuidado extra;
- decisões de arquitetura que não estão escritas em lugar nenhum.

Seja breve. Isso é o mínimo que toda tarefa futura precisa respeitar, não uma entrevista sobre o projeto inteiro.

## 6. Gravar

Escreva `.trilho/projeto.md` a partir de `modelo-projeto.md` (ao lado deste arquivo) e crie `.trilho/tarefas/`. Mostre um resumo do que foi descoberto. Lembre que `.trilho/` deve ser versionado no git.
