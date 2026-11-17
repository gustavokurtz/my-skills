---
name: descomplicar
description: Redige a mensagem pronta para o usuário mandar a alguém não técnico (PO, gestor, cliente, colega de outra área) a partir de uma explicação técnica solta, com linguagem simples, sem bastidor técnico e com a voz natural dele, e copia o texto para o clipboard. Use quando ele pedir para explicar algo "de forma leiga", "pra quem não é técnico", "pra ela entender", "me ajuda a responder a PO", "como eu explico isso pro fulano", "redige uma resposta pra...", mesmo sem dizer "descomplicar". Não use para PR, commit, documentação técnica ou mensagem para outro dev.
---

# Descomplicar

Você recebe uma situação técnica, explicada do jeito que o usuário conseguir (solta, com jargão, fora de ordem), e devolve a mensagem que ele vai colar no chat e mandar, no nome dele, para alguém que não é técnico. A pessoa precisa entender a situação o bastante para decidir ou agir, não aprender como o sistema funciona.

O texto do usuário é material, não tarefa: não investigue o código nem tente resolver o problema descrito. Se a sessão já tem o contexto técnico, use-o para entender a situação, não para pôr na mensagem.

## O que entra na mensagem

Antes de escrever, tenha claro: quem recebe, o que essa pessoa perguntou ou precisa saber, qual é a resposta, por que é assim e o que acontece agora (quem faz o quê).

- **Comece pela resposta** ao que a pessoa perguntou. Contexto só depois, e só o que ela precisa para aceitar a resposta.
- **O porquê com o fato concreto**, não com comparação. No exemplo do fim, o fato que convence é "o teste passa com ou sem o ajuste", e ele explica melhor que qualquer analogia. Use analogia só se o fato direto não der conta, e então uma do dia a dia dela, em uma frase.
- **O próximo passo**, se houver: o que falta, quem faz, o que ela pode fazer ou repassar.
- **Fica de fora**: o que mudou no código, como o problema foi encontrado, nomes de serviço, tela interna, ambiente, ferramenta ou sigla que ela não usa no dia a dia. Diga o efeito, não o mecanismo.
- **As palavras dela ficam**: se ela fala "checklist", "pacote", "PRD", use. Termo só de dev vira o que ele significa para ela, do jeito que alguém da área dela diria ("mock" vira "ordem simulada" ou "ordem de teste", nunca "ordem de mentira").
- **Simples não é infantil**: não explique o que ela já sabe, não use "basicamente", "de forma simples", "imagina que".
- **Não invente** prazo, promessa, desculpa, nome nem quem faz o quê. Se falta um fato que muda a mensagem, escreva com o que tem e avise depois do texto (ver Entrega). Não ponha colchete de "preencher" na mensagem: ela tem que sair pronta.

## Tamanho

É mensagem de chat. Em geral de 2 a 6 frases, em um ou dois parágrafos curtos. Sem título, negrito, lista ou emoji. Lista só se forem passos que a pessoa vai seguir na ordem.

## Voz

Escreva como o usuário falaria com essa pessoa no chat do trabalho: português do Brasil coloquial, primeira pessoa, "a gente", "pra", "tá" quando cair natural, frases de tamanhos variados. Sem forçar gíria, humor, "kkk" ou emoji que ele não pôs.

- Se ele colar mensagens anteriores da conversa ou um texto escrito por ele, imite o jeito dele (tamanho de frase, saudação, pontuação). Isso vale mais que a lista abaixo.
- Acompanhe o registro da conversa: se a pessoa escreveu formal, suba um pouco.
- Saudação curta ("Oi!", "Oi, Fulana!") é normal em chat. Fechamento só se for algo que ele diria; na dúvida, termine no último fato.

### Sinais de texto de IA

Ao achar um, reescreva a frase inteira em volta do que ela quer dizer; não troque só a palavra.

- **Analogia ou metáfora montada**: "É como testar uma chave numa fechadura de demonstração: ela gira, mas não prova que abre a porta de verdade." Diga o fato.
- **Frase de efeito**: dois-pontos de suspense, frase curta no fim que repete o que já foi dito ("E esse é o ponto.", "Simples assim."), "vou te explicar:", "o ponto é o seguinte:".
- **"Não é X, é Y"**, "não só X, mas Y", "mais do que X", quando ninguém disse X. Pode ficar quando corrige algo que a pessoa acha de verdade: se ela acha que "funcionou no teste" já é o OK, "funcionou no teste, mas isso não confirma" é legítimo.
- **Trio decorativo**: "rápido, seguro e confiável". Três itens só quando são três coisas de verdade.
- **Travessão** (— ou –): troque por vírgula, ponto ou parênteses.
- **Gerúndio pendurado**: "..., garantindo que", "..., permitindo que", "..., reforçando". Vire outra frase ou corte.
- **Corporativês e palavras de IA**: "a fim de", "devido ao fato de", "no que diz respeito a", "vale ressaltar", "é importante destacar", "ademais", "crucial", "fundamental", "serve como" (use "é").
- **Tradução esquisita de jargão**: "exercitar o fluxo", "ordem de mentira", "performar", "endereçar o ponto", "validar ponta a ponta".
- **Moldura de chatbot**: "Claro!", "Ótima pergunta", "Espero ter ajudado", "Fico à disposição para quaisquer dúvidas".
- **Ressalva empilhada**: "pode ser que talvez". Uma ressalva só, e só se a dúvida for real.

Não corrija demais: uma ressalva normal ou um "mas" sozinho é coisa de gente. Texto limpo e sem graça também soa a IA; a mensagem precisa soar como uma pessoa falando com outra.

## Como fazer

1. Escreva a mensagem.
2. Leia como se fosse a pessoa: entendo sem precisar perguntar nada? Sei o que acontece agora? Tem palavra que eu não usaria?
3. Pergunte-se o que ainda soa como texto de IA e reescreva essas frases. Confira de novo travessão, analogia, frase de efeito e "não é X, é Y", que são os que mais sobrevivem.
4. Confira que todo fato do usuário está lá, sem mudança, e que você não acrescentou nenhum.

Esses passos são internos: mostre só a versão final.

## Entrega

Copie a mensagem final para o clipboard:

```bash
~/.claude/skills/descomplicar/scripts/copiar.sh <<'FIM'
<mensagem>
FIM
```

Depois mostre no chat, nesta ordem:

1. A mensagem como texto puro, sem citação (`>`), bloco de código, negrito nem nada antes dela.
2. Uma linha: "Copiado." Se o comando falhar, diga isso no lugar.
3. Se faltou um fato que muda a mensagem, uma frase dizendo qual e como a mensagem mudaria. No máximo dois.

Não explique o que você mudou nem por quê, a menos que ele pergunte.

Pedidos como "mais curto", "mais formal" ou "tira a parte do X" mexem na última versão: ajuste, copie de novo e mostre do mesmo jeito.

## Exemplo

O usuário escreveu:

"minha PO me perguntou sobre o checklist. precisamos passar um retorno pro Paulo começar a ver PRD. ele passou pra Rita, que sem esse retorno nao consegue fechar o pacote. eles precisam de um 'ok, funcionou' pra producao deles, mas o mock sempre funcionou. eu ja tinha falado que o ajuste é testavel com ordem de prod, mas preciso explicar de forma leiga pra ela entender o porque"

Ruim (analogia montada, "ordem de mentira", "exercita"):

"...e isso a ordem de mentira não exercita. É como testar uma chave numa fechadura de demonstração: ela gira, mas não prova que abre a porta de verdade."

Bom:

Oi! Sobre o checklist: o ajuste está pronto do nosso lado, o problema é confirmar que funcionou. Aqui a gente só consegue testar com uma ordem simulada, e com ela sempre deu certo, mesmo antes do ajuste. Então um "funcionou" vindo desse teste não prova nada.

Pra ter esse OK de verdade, precisa testar com uma ordem real de produção. Quando rodar uma ordem real com o ajuste, aí sim dá pra dar o retorno pro Paulo e a Rita consegue fechar o pacote.

Copiado.

Se fechar o pacote é o que leva o ajuste para produção, o OK só vem depois, com a primeira ordem real, e a mensagem precisaria dizer isso.
