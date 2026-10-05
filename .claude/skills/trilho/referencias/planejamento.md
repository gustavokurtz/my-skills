# Planejamento

O objetivo é um `roteiro.md` que uma sessão nova, sem nada desta conversa, executa lendo só `projeto.md`, `roteiro.md` e `estado.md`, sem perguntar nada.

## 1. Explorar

Leia o código que a tarefa toca, os padrões que já existem, os testes que já existem e os pontos de integração. **Não pergunte o que o código responde.**

**Se a tarefa mexe em UI** (tela, componente, layout, estilo): carregue a skill `frontend-design` (Skill tool, `frontend-design:frontend-design`) antes de decidir o desenho, e leve as escolhas visuais para a seção Decisões do roteiro. Se a skill não estiver instalada, siga sem ela e avise o usuário.

## 2. Mapear

Liste para você mesmo:

- **Escopo:** o que entra e o que fica de fora.
- **Comportamento:** casos de borda, erros, estados vazios.
- **Efeitos colaterais:** quem já usa o código que vai mudar, dados existentes, migração, compatibilidade. Para cada efeito, uma mitigação.
- **Caminho:** a menor solução que atende. Uma opção mais elaborada precisa se justificar pelo pedido, não por "pode ser útil depois".
- **Incertezas empíricas:** o que nem você nem o usuário sabem e só aparece rodando. Isso não vira pergunta: vira sondagem no roteiro.

## 3. Perguntar só o que muda a solução

Antes de cada pergunta, teste: "se a resposta fosse a outra, o código ou o escopo mudaria? E o que o usuário já disse resolve?". Pergunte só se mudaria e não resolve. Caso contrário, decida e registre em Decisões, marcado como "(decidido por mim)". **Zero perguntas é um resultado válido.**

As perguntas são da tarefa e ancoradas no código, nunca genéricas.

- Ruim: "Como você quer tratar erros?"
- Bom: "`calcularFrete` hoje devolve 0 para carrinho vazio, e o novo fluxo chama ele antes da validação. Mantemos o 0 ou passamos a lançar `CarrinhoVazioError`?"

Formato:

- **Decisão fechada:** AskUserQuestion com 2 a 4 opções. A recomendada vem primeiro, com "(Recomendado)", e cada descrição traz o trade-off. Junte até 4 perguntas independentes numa chamada.
- **Pergunta aberta** (objetivo, contexto de negócio): em texto.
- **Incerteza empírica relevante:** combine numa pergunta só, com recomendação, a **meta** (ex.: "eval 7/7 com 2 repetições"), o **orçamento** (rodadas, custo) e o **plano B** se o orçamento acabar (ex.: "tirar a decisão do prompt e passar para código").

## 4. Escrever o roteiro

Escreva `roteiro.md` na pasta da tarefa a partir de `modelos/roteiro.md`.

- **Pedido:** o que o usuário pediu, reescrito de forma clara e fiel. Cada ideia, restrição, nome e número dele continua lá, com o porquê quando ele deu. Corrija a forma, não o conteúdo, e não acrescente requisitos. É a referência de "o que ele quis" para as próximas sessões.
- **Tarefas:**
  - cada uma é uma ação verificável, não um tema, e cabe num passo de trabalho (se vai encostar em oito arquivos, quebre);
  - ordem por dependência **e por risco**: a sondagem da maior incerteza vem primeiro, antes de construir em volta dela;
  - cada uma declara como é verificada: `Teste:` (escrito antes, TDD), ou `Verificar por:` com um comando ou passo concreto e o motivo de não ter teste, ou, se for empírica, `Meta:`, `Orçamento:` e `Se esgotar:`.
- **Fases:** só se houver mais de umas 8 tarefas ou não couber numa sessão. Cada fase entrega algo funcionando e termina com um critério claro.
- **Pronto quando:** critério observável e o roteiro de validação manual para o usuário.
- **Curto.** Seção sem conteúdo fica "nenhuma". O roteiro é o mais curto que se basta.

## 5. Fechar

1. Crie o `estado.md` a partir de `modelos/estado.md`, com todas as tarefas `pendente` e o próximo passo apontando para a primeira.
2. Mostre um resumo de até 5 linhas: o pedido em uma frase, as decisões que você tomou sozinha, as incertezas e o caminho do roteiro. Não espere aprovação; o usuário interrompe se quiser corrigir.
3. Decida pelo peso do contexto:
   - **Leve** (exploração curta, poucos arquivos lidos): diga "sigo aqui, contexto leve" e vá para `referencias/execucao.md`.
   - **Pesado:** faça o handoff (`referencias/handoff.md`).
