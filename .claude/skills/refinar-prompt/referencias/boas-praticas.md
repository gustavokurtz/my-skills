# Boas práticas oficiais que fundamentam esta skill

Resumo (parafraseado) do que os provedores recomendam. Consulte quando precisar decidir _como_ melhorar um prompt sem descaracterizá-lo. Pesquisado em setembro/2026; as páginas mudam, então em caso de dúvida real vale reabrir as fontes.

## Sumário

1. Anthropic: prompting geral
2. Anthropic: Claude Code
3. OpenAI
4. Como isso vira regra na skill

---

## 1. Anthropic: prompting geral

Fonte: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices

- **Seja claro e direto.** Modelos Claude respondem bem a instruções explícitas; se quiser algo "além do básico", peça explicitamente em vez de esperar que o modelo deduza.
- **Regra de ouro:** mostre o prompt a um colega com pouco contexto da tarefa. Se ele ficaria confuso, o Claude também ficará. Pense no modelo como um funcionário novo e brilhante que não conhece suas normas.
- **Dê contexto e motivo.** Explicar _por que_ uma instrução existe permite ao modelo generalizar melhor (ex.: "a resposta será lida em voz alta por um sistema de texto-para-fala, então evite reticências" funciona melhor que "nunca use reticências").
- **Exemplos** são uma das formas mais confiáveis de guiar formato, tom e estrutura. Devem ser relevantes, variados e delimitados (tags `<example>`). De 3 a 5 costuma ser bom.
- **Tags XML** ajudam quando o prompt mistura instruções, contexto, exemplos e dados variáveis. Use nomes consistentes e descritivos.
- **Dados longos no topo, pergunta no fim.** Em entradas grandes (20k+ tokens), pôr o material antes e a consulta depois melhora a qualidade.
- **Diga o que fazer, não só o que evitar.** "Escreva em parágrafos corridos" funciona melhor que "não use markdown".
- **Combine o estilo do prompt com o estilo desejado na saída.** Um prompt cheio de markdown tende a gerar respostas cheias de markdown.
- **Peça ação explicitamente.** "Pode sugerir mudanças?" leva a sugestões; "Altere esta função para..." leva a alterações.
- **Menos ênfase agressiva.** Modelos recentes são muito responsivos ao prompt; "CRÍTICO: você DEVE..." tende a causar excesso. Instruções normais bastam.
- **Instruções gerais podem superar passos prescritos** quando o modelo raciocina ("pense com cuidado sobre isso" costuma render mais do que um plano passo a passo escrito à mão).

## 2. Anthropic: Claude Code

Fonte: https://code.claude.com/docs/en/best-practices

- O limite central é a **janela de contexto**: ela enche rápido e o desempenho cai à medida que enche. Prompts precisos evitam idas e vindas.
- **Dê ao Claude um jeito de verificar o próprio trabalho** (testes, build, screenshot, saída esperada). É apontado como a prática de maior alavanca. Exemplo de "depois": incluir casos de teste e pedir para rodá-los.
- **Explore → planeje → implemente → faça commit.** Separar pesquisa/plano da implementação evita resolver o problema errado. Se você descreveria o diff em uma frase, dispense o plano.
- **Contexto específico reduz correções:**
  - _Delimite a tarefa_: qual arquivo, qual cenário, preferências de teste.
  - _Aponte fontes_: direcione o Claude a onde a resposta está (ex.: histórico do git).
  - _Referencie padrões existentes_: aponte um arquivo do repositório como modelo.
  - _Descreva o sintoma_: sintoma + local provável + o que é "corrigido".
- **Conteúdo rico**: referencie arquivos com `@`, cole imagens, passe URLs de documentação, canalize dados (ex.: log).
- **Deixe o Claude entrevistar você** em features maiores, e depois escrever uma especificação. Boas specs são autocontidas: nomeiam arquivos e interfaces, dizem o que está fora de escopo e terminam com uma verificação de ponta a ponta.
- **Corrija cedo.** Se você corrigiu o Claude mais de duas vezes no mesmo problema, o contexto está poluído: use `/clear` e recomece com um prompt melhor que incorpore o que aprendeu.
- **Evite** a sessão "pia de cozinha" (várias tarefas sem relação numa só sessão) e a investigação sem escopo ("investigue isso" sem delimitar).
- **CLAUDE.md/skills**: manter curtos; instruções demais diluem as importantes.

## 3. OpenAI

Fonte: https://help.openai.com/en/articles/6654000-best-practices-for-prompt-engineering-with-openai-api

- **Instruções no início** do prompt e **delimitadores** (`###`, `"""`, tags) separando instrução de contexto/dados.
- **Seja específico e descritivo** sobre contexto, resultado, tamanho, formato e estilo.
- **Mostre o formato desejado com exemplos** ("mostre e explique").
- Prefira dizer o que fazer em vez do que não fazer; reduza descrições vagas ou "fofas".

Observação: as recomendações convergem com as da Anthropic (clareza, delimitação, exemplos, formato explícito), o que dá segurança de que são práticas gerais e não truques de um só modelo.

## 4. Como isso vira regra na skill

| Prática oficial                                                   | Onde aparece na skill                               |
| ----------------------------------------------------------------- | --------------------------------------------------- |
| Colega novo sem contexto                                          | Princípio 2 (clareza para a IA)                     |
| Contexto e motivo                                                 | Preservar o "porquê" do usuário                     |
| Positivo em vez de só negativo                                    | Princípio 2, com a ressalva de não perder sentido   |
| Tags XML / delimitadores / dados no topo                          | Seção "Tamanho e estrutura"                         |
| Sem ênfase agressiva                                              | Seção "Tamanho e estrutura"                         |
| Pedir ação explicitamente                                         | Destino: ação versus sugestão                       |
| Verificação, explore→planeje→implemente, escopo, padrões, sintoma | Seção "Destino do prompt" (Claude Code) e Sugestões |
| Uma tarefa por sessão                                             | Várias tarefas sem relação                          |
| Concisão                                                          | Tamanho proporcional                                |

Regras que **não** vêm dos provedores, mas do pedido do usuário desta skill: fidelidade total (nada omitido), preservar o tom, e nunca inventar conteúdo.
