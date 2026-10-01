# Etapa: entrevista (só fluxo grande)

O objetivo é eliminar toda pendência que levaria a construir algo que o usuário não quer. Cada pergunta respondida agora é uma rodada de correção a menos depois.

## 1. Explorar antes de perguntar

Leia o código que a tarefa toca, os padrões que já existem, os testes que já existem e os pontos de integração. **Não pergunte o que o código responde.** Pergunta cuja resposta estava no repo gasta o tempo do usuário e mostra que você não fez a lição de casa.

## 2. Mapear as decisões

Antes de perguntar, liste para você mesmo o que precisa ser decidido:

- **Escopo:** o que entra e o que fica de fora.
- **Comportamento:** casos de borda, erros, estados vazios.
- **Efeitos colaterais:** quem já usa o código que vai mudar, dados existentes, migração, compatibilidade. Para cada efeito, tenha uma mitigação proposta.
- **Caminho:** a menor solução que atende. Se existir uma opção mais elaborada, ela precisa se justificar por um requisito, não por "pode ser útil depois".

## 3. Perguntar

As perguntas devem ser **da tarefa e ancoradas no código**, nunca genéricas.

- Ruim: "Como você quer tratar erros?"
- Bom: "`calcularFrete` hoje devolve 0 para carrinho vazio, e o novo fluxo chama ele antes da validação. Mantemos o 0 ou passamos a lançar `CarrinhoVazioError`?"

Formato:

- **Decisão fechada:** use AskUserQuestion com 2 a 4 opções. A recomendada vem primeiro, com "(Recomendado)", e cada descrição traz o trade-off. Junte até 4 perguntas independentes numa chamada; as que dependem de uma resposta anterior vêm depois dela.
- **Pergunta aberta** (objetivo, contexto de negócio, algo que você não consegue enumerar): faça em texto.
- **Sempre traga recomendação.** O usuário quer decidir, não pensar do zero.

## 4. Quando parar

Não existe teto de perguntas, mas cada pergunta precisa mudar alguma coisa. Antes de perguntar, teste: "se a resposta fosse a outra, o código ou o escopo mudaria?". Se não mudaria, não pergunte. Decida você e registre a escolha como premissa na spec, onde o usuário vai vê-la no gate.

Pare quando não sobrar pendência que mude código ou escopo.

## 5. Fechar

Resuma as decisões em poucas linhas, atualize `etapa` para `spec` no `progresso.json` e siga para `referencias/spec.md`.
