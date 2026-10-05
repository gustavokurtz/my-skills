# Handoff

Prepara a tarefa para continuar numa sessão nova, depois de um `/clear`.

**Quando:** o usuário pede ("handoff", "vou dar clear", "salva onde paramos"); no fim do planejamento ou de uma fase com o contexto pesado; antes de qualquer pausa.

## Como

1. **Releia a conversa inteira, não só o fim.** Resumos tendem a guardar o fim e esquecer o começo e o meio, onde costumam estar as correções do usuário e as decisões que mudaram o rumo.
2. **Procure o que o roteiro não tem:**
   - correções e preferências do usuário, com as palavras dele quando importarem;
   - decisões tomadas no caminho, cada uma com o porquê (sem o porquê, a decisão é revertida na primeira dúvida);
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
