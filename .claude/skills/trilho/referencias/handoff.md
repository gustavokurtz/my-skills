# Handoff

Prepara a tarefa para continuar numa sessão nova, depois de um `/clear`.

**Quando:** sempre no fim do planejamento e no fim de cada fase, menos a última (a entrega segue na mesma sessão); quando o usuário pede ("handoff", "vou dar clear", "salva onde paramos"); antes de qualquer pausa; e quando chega o aviso de contexto. Você não roda o `/clear`: peça ao usuário.

## Aviso de contexto

A skill registra um hook (`scripts/contexto.py`, no frontmatter do `SKILL.md`) que fica ativo na sessão depois que o trilho é invocado. Ele lê o tamanho do contexto no transcript e injeta um aviso que começa com `[trilho] contexto em …`:

- **Aviso (200k):** termine a tarefa em andamento, sem abrir outra, e faça o handoff. Numa rodada empírica ou esperando o dev, faça assim que a rodada fechar.
- **Limite (250k):** pare agora, sem começar nada novo. Deixe o código num ponto commitável, ou registre no `estado.md` o que ficou pela metade, e faça o handoff.

O aviso não se discute: você não mede o próprio contexto, e a partir de uns 300k a qualidade cai. Os limites mudam com `TRILHO_CONTEXTO_AVISO` e `TRILHO_CONTEXTO_LIMITE`, que vão no `env` do `settings.json`.

## Como

1. **Releia a conversa inteira, não só o fim.** Resumos tendem a guardar o fim e esquecer o começo e o meio, onde costumam estar as correções do usuário e as decisões que mudaram o rumo.
2. **Procure o que o roteiro não tem:**
   - correções, preferências e decisões do usuário, escritas com as suas palavras ("decidido: X"), sem transcrever a fala dele, salvo se ele pedir;
   - defeitos encontrados, com o mecanismo de desenho de cada um (é o que mostra a família na próxima sessão);
   - decisões tomadas no caminho, cada uma com o porquê (sem o porquê, a decisão é revertida na primeira dúvida);
   - causas encontradas, com `arquivo:linha`;
   - hipóteses testadas e descartadas, com a evidência;
   - descobertas sobre o código que a próxima sessão precisaria redescobrir.
3. **Reescreva o `estado.md`** a partir de `modelos/estado.md`. Reescreva, não acrescente: ele descreve o agora. Hipóteses descartadas e decisões continuam enquanto forem relevantes; o que virou história sai (o histórico fica no git).
4. **Seja concreto:** arquivos, funções, comandos, ids, mensagens de erro. "Ajustamos o prompt" não serve; "trocamos o retorno da `acionar_manobra` em `tools/registry.py`" serve.
5. **Teste antes de entregar:** uma sessão nova executaria o próximo passo lendo só `projeto.md`, `roteiro.md` e `estado.md`, sem perguntar nada? Se não, falta algo. Máximo de duas telas; corte o que já está no roteiro.

## Fechar

Responda em uma ou duas linhas onde paramos e termine com o comando para retomar:

```
/clear
continua <slug>
```
