# Entrega

Só considere a tarefa pronta depois de, nesta ordem:

## 1. Verificação completa

Rode a suíte de testes inteira, o lint, o typecheck e o build, conforme o `projeto.md`. Falhou: conserte e volte ao início desta lista.

## 2. Code review por subagente

Lance **um** subagente (Agent tool, tipo general-purpose) com contexto limpo. Quem escreveu o código tende a aprovar o próprio trabalho; um revisor que não viu a conversa lê só o que está nos arquivos.

A instrução dele é o conteúdo de `referencias/revisor.md`, mais:

- o caminho do `roteiro.md`;
- o intervalo de commits da tarefa (`<base>..HEAD`).

O revisor só reporta achados com confiança ≥ 80. Mesmo assim, verifique cada um antes de agir, porque o revisor também erra. Corrija o que for real e commite. Quando discordar de um achado, diga isso explicitamente ao usuário.

## 3. Registro

Preencha a seção Resultado do `estado.md` (commits, resultado dos testes, achados do review, o que ficou de fora e por quê) e mude a etapa para `concluida`.

## 4. Fechamento

Responda com:

- o que foi feito, em uma ou duas frases;
- os commits criados;
- o resultado dos testes;
- o resumo do review;
- o roteiro de validação manual (do "Pronto quando"), para o usuário rodar;
- o caminho da pasta da tarefa.

Não espere o resultado da validação manual. Se o usuário relatar um problema, ele vira uma nova rodada de execução.

Nada de relatório longo: os arquivos já são o registro.
