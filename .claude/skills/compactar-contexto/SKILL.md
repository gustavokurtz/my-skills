---
name: compactar-contexto
description: Gera um resumo estruturado da conversa atual antes de compactar o contexto, preservando decisões-chave (com o porquê), alternativas descartadas, correções do usuário, estado atual e pendências, cobrindo início, meio e fim da sessão. Use sempre que o usuário for rodar /compact, mencionar "compactar", "resumir a sessão", "salvar contexto", "handoff", "o contexto tá cheio", "vou limpar a conversa", ou quiser continuar o trabalho depois sem perder o que foi decidido, mesmo que não peça explicitamente um resumo.
---

# Contexto para /compact

Resumos automáticos tendem a guardar bem o fim da conversa e esquecer o começo e o meio, que é justamente onde costumam estar as decisões de arquitetura, as restrições combinadas e as correções que o usuário fez. Esta skill existe para evitar isso: ela produz um resumo que outra instância do Claude consiga ler e continuar o trabalho como se tivesse estado presente o tempo todo.

## Como proceder

1. Releia a conversa inteira, do primeiro ao último turno. Não comece pelo fim. Divida mentalmente em três fases (início, meio, fim) e procure em cada uma o que mudou o rumo do trabalho.
2. Separe o que é **decisão** do que é **discussão**. Uma decisão é algo que foi combinado e que, se esquecido, faria o próximo Claude refazer ou desfazer trabalho. Discussão que não levou a nada pode sumir.
3. Para cada decisão, registre o motivo. Sem o porquê, a decisão vira regra arbitrária e acaba sendo revertida na primeira dúvida.
4. Registre alternativas descartadas e por que foram descartadas, para que ninguém as proponha de novo.
5. Dê peso especial a correções e preferências do usuário ("não use X", "prefiro Y", "isso está errado"). São as informações mais caras de perder.
6. Seja concreto: nomes de arquivos, funções, comandos, valores, versões, mensagens de erro. "Ajustamos a configuração" não serve; "mudamos `timeout` de 30 para 120 em `config/api.ts`" serve.
7. Escreva o resumo no formato abaixo e salve em `.claude/contexto-sessao.md` (crie a pasta se não existir; se já houver um arquivo de sessão anterior, acrescente no topo com a data e mantenha o anterior abaixo). Depois mostre o resumo ao usuário.
8. Termine sugerindo o comando para compactar, por exemplo:
   `/compact Preserve integralmente o conteúdo de .claude/contexto-sessao.md e as decisões listadas nele.`

## Formato do resumo

Use exatamente esta estrutura. Omita uma seção só se ela estiver realmente vazia (escreva "nenhum" em vez de inventar conteúdo).

```markdown
# Contexto da sessão — [data] — [tema em poucas palavras]

## Objetivo

O que o usuário quer alcançar, em 1 a 3 frases. Inclua o objetivo original e, se mudou, o atual.

## Linha do tempo

**Início:** como a sessão começou, pedido inicial, contexto e restrições dadas.
**Meio:** principais viradas: problemas encontrados, mudanças de abordagem, descobertas.
**Fim:** onde paramos, o que acabou de ser feito.

## Decisões-chave

- **[Decisão]** — motivo: [por quê]. (fase: início/meio/fim)

## Alternativas descartadas

- [Alternativa] — descartada porque [motivo].

## Preferências e correções do usuário

- [O que o usuário pediu, proibiu ou corrigiu, com as palavras dele quando forem importantes]

## Estado atual

- Arquivos criados/alterados: `caminho` — o que mudou
- O que está funcionando / testado
- O que está quebrado ou incompleto

## Pendências e próximos passos

1. [Próxima ação concreta]
2. ...

## Informações de referência

Comandos, valores, IDs, URLs, erros exatos e outros detalhes que seriam difíceis de reconstruir.
```

## Critérios de qualidade

Antes de entregar, confira:

- Existe pelo menos um item vindo do **início** da conversa? Se não, releia o começo; é quase certo que algo foi esquecido.
- Cada decisão tem motivo?
- Alguém que não viu a conversa conseguiria executar o primeiro próximo passo sem perguntar nada?
- O resumo está enxuto? Mire em algo que caiba em uma tela ou duas. Corte explicações longas, mantenha fatos.

## Exemplo curto

**Decisões-chave**

- **Usar SQLite em vez de Postgres no MVP** — motivo: app roda local, usuário não quer depender de servidor. (início)
- **Validar com Zod na borda da API, não no banco** — motivo: mensagens de erro mais claras para o front. (meio)

**Preferências e correções do usuário**

- Não usar `any` em TypeScript ("nem em teste").
- Commits em português, no formato `tipo: descrição`.
