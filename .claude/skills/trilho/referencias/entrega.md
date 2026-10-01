# Etapa: entrega

Só considere a tarefa pronta depois de, nesta ordem:

## 1. Verificação completa

Rode a suíte de testes inteira, o lint, o typecheck e o build, conforme o `projeto.md`. Falhou: conserte e volte ao início desta lista.

## 2. Code review por subagente

Lance **um** subagente (Agent tool, tipo general-purpose) com contexto limpo. Quem escreveu o código tende a aprovar o próprio trabalho; um revisor que não viu a conversa lê só o que está nos arquivos.

Passe para ele:

- o caminho da `spec.md` (fluxo grande) ou do `plano.md` (fluxo pequeno);
- o intervalo de commits da tarefa (`git diff <base>..HEAD`).

Peça uma lista priorizada de:

- **Cobertura:** algum requisito ou critério de aceite sem implementação ou sem teste?
- **Correção:** bugs, casos de borda e erros não tratados.
- **Excesso:** overengineering, código morto, `console.log` esquecido, código comentado, segredo hardcoded, import não usado.

Verifique cada achado antes de agir, porque o revisor também erra. Corrija o que for real. Quando discordar de um achado, diga isso explicitamente ao usuário.

## 3. Validação manual e2e

Apresente ao usuário o roteiro de validação manual do plano e espere o resultado. Se aparecer um problema, trate como desvio (`referencias/execucao.md`).

## 4. Registro

Preencha a seção Resultado do plano: commits, resultado dos testes, achados do review e o que ficou de fora e por quê. Atualize `etapa` para `concluida`.

## 5. Fechamento

Responda com:

- o que foi feito, em uma ou duas frases;
- os commits criados;
- o resultado dos testes;
- o resumo do review;
- o caminho da pasta da tarefa.

Nada de relatório longo: os arquivos já são o registro.
