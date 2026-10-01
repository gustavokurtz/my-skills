# Exemplos de antes e depois

Servem para calibrar o nível de intervenção: reorganizar e clarear, sem inventar e sem inflar.

## Exemplo 1: bug (Claude Code)

**Original**

> o login ta quebrando dps q a sessao expira, acho q é no refresh do token mas n tenho certeza, olha em src/auth. faz um teste q reproduz antes de arrumar pfv. e nao mexe no resto q tá funcionando

**Resposta esperada**

Prompt refinado:

```
O login está quebrando depois que a sessão expira. Acho que o problema está no refresh do token, mas não tenho certeza.

1. Investigue o fluxo de autenticação em src/auth/, principalmente o refresh do token.
2. Antes de corrigir, escreva um teste que reproduza o problema.
3. Depois, corrija o problema.

Não mexa no resto do código, o restante está funcionando.
```

O que mudei:

- Separei sintoma (com a suspeita marcada como incerta), passos e restrição.
- Coloquei os passos na ordem em que ele os pediu (investigar, testar, corrigir).

Sugestões opcionais:

- Pedir que rode o teste (e a suíte existente) depois da correção, para confirmar.

_(Repare: "src/auth" e "não mexe no resto" foram mantidos; a verificação, que ele não pediu, ficou só como sugestão.)_

---

## Exemplo 2: landing page com referência e números

**Original**

> quero fazer uma landing page pro meu curso de violao online tipo essa https://exemplo.com/lp que eu gostei, cores mais quentes, tem q ter depoimentos e um botao de whatsapp fixo, o preço é 197 no pix ou 12x de 19,90, nao quero aquele visual generico de IA, o publico é adulto iniciante

**Resposta esperada**

Prompt refinado:

```
Quero criar uma landing page para o meu curso de violão online.

Referência: https://exemplo.com/lp (gostei dessa, quero algo nesse estilo).

Público: adultos iniciantes.

A página precisa ter:
- Depoimentos.
- Um botão de WhatsApp fixo na tela.
- O preço: R$ 197 no Pix ou 12x de R$ 19,90.

Visual: cores mais quentes. Não quero aquele visual genérico de IA.
```

O que mudei:

- Agrupei em referência, público, conteúdo obrigatório e visual.
- Marquei os valores como preço em reais (o contexto de Pix indica BRL).

Pontos em aberto:

- Não foi dito com que tecnologia construir (HTML puro, React, etc.); deixei em aberto.
- "Estilo dessa referência" vale só para o layout ou também para as cores? Assumi que as cores são "mais quentes" que a referência.

_(Repare: "tipo essa" virou "nesse estilo" porque é o sentido dele. Não foram inventadas seções como "FAQ" ou "garantia".)_

---

## Exemplo 3: prompt curto → refinado curto

**Original**

> resume esse artigo em 5 bullets e dps traduz pra ingles

**Resposta esperada**

Prompt refinado:

```
Resuma este artigo em 5 tópicos e, depois, traduza o resumo para o inglês.
```

O que mudei:

- Corrigi a escrita e deixei a ordem das duas etapas explícita.

Pontos em aberto:

- O artigo não veio junto com o texto; será preciso colá-lo ou anexá-lo ao enviar.
- Assumi que a tradução é do resumo, não do artigo inteiro.

_(Repare: sem seções, sem tags, sem sugestões desnecessárias. Prompt curto continua curto.)_

---

## Exemplo 4: material colado (erro literal)

**Original**

> tô tentando rodar o build e dá isso:
> Error: Cannot find module '@/lib/utils'
> at src/components/Button.tsx:3
> ja tentei reinstalar node_modules e n resolveu. usa vite. resolve isso aí

**Resposta esperada**

Prompt refinado:

````
Estou tentando rodar o build e recebo este erro:

```
Error: Cannot find module '@/lib/utils'
  at src/components/Button.tsx:3
```

Já tentei reinstalar o node_modules e não resolveu. O projeto usa Vite.

Resolva esse erro.
````

O que mudei:

- Isolei o erro em bloco de código, idêntico ao original.
- Juntei o que ele já tentou e a informação sobre o Vite como contexto.

Sugestões opcionais:

- Dizer como confirmar a correção (ex.: "o build deve terminar sem erros").
- Se souber, mencionar onde o alias `@` deveria estar configurado.

_(Repare: a skill NÃO tenta resolver o erro; só prepara o prompt.)_
