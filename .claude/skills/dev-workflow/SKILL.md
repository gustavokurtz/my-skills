---
name: dev-workflow
description: Workflow padrão de desenvolvimento deste projeto — planejar antes de codar, registrar o plano em docs/plans/ com checklist, executar marcando os itens, rodar os testes e commitar no padrão do repo. Use SEMPRE que a tarefa envolver escrever ou alterar código de produção: implementar feature, corrigir bug, refatorar, migrar, criar endpoint, mexer em schema. Use também quando o usuário disser "vamos planejar", "cria o plano", "pode implementar", "executa o plano", "termina isso" ou pedir para continuar um plano existente. Na dúvida entre usar e não usar, use.
---

# Workflow de desenvolvimento

Este projeto trabalha em três etapas: **planejar → executar → entregar**. O plano vive num arquivo versionado, não na conversa, para que qualquer sessão futura (sua ou de outra pessoa) consiga retomar de onde parou.

## Configuração do projeto

Preencha esta seção uma vez e trate os valores como a fonte da verdade:

```
Comando de teste:     <ex: npm test>
Comando de build:     <ex: npm run build>
Pasta dos planos:     docs/plans/
Branch de integração: develop
```

Se algum desses comandos não existir no projeto, pule a etapa correspondente em vez de inventar um comando.

## Etapa 1 — Planejar

Antes de editar qualquer arquivo, entenda o terreno: leia os arquivos que a tarefa toca, procure código parecido que já exista no repo e siga o padrão local em vez de introduzir um novo. Se a tarefa for ambígua num ponto que muda o desenho da solução, pergunte agora — uma pergunta bem colocada antes de planejar economiza um replanejamento inteiro.

Depois escreva o plano em `docs/plans/AAAA-MM-DD-<slug>.md` usando `template.md` (ao lado deste arquivo) como estrutura. Use a data real do sistema e um slug curto em kebab-case derivado da tarefa.

Regras para o checklist:

- Cada item é uma ação verificável, não um tema. "Adicionar índice em `users.email`" serve; "melhorar performance" não.
- Cada item cabe em um passo de trabalho. Se um item vai encostar em oito arquivos, quebre.
- Ordene por dependência: o que precisa existir primeiro vem primeiro.
- Inclua os itens de verificação (testes, lint, typecheck) como itens do checklist, não como um rodapé implícito.
- Entre 3 e 12 itens. Menos que isso normalmente não precisava de plano; mais que isso normalmente são dois planos.

Apresente o plano e **espere aprovação antes de executar**. O valor do plano está em o usuário poder discordar barato, antes de o código existir.

## Etapa 2 — Executar

Trabalhe um item de cada vez, na ordem. Ao terminar um item, marque `[x]` no arquivo do plano antes de começar o próximo — o arquivo é o estado real do trabalho, e uma sessão interrompida no meio precisa conseguir ser retomada só lendo ele.

Quando a realidade divergir do plano — e ela vai —, atualize o plano em vez de seguir em frente calado: edite o item, ou adicione um novo com uma linha explicando o porquê na seção "Desvios". Um plano que não bate com o que foi feito é pior do que nenhum plano, porque mente para quem ler depois.

Se um item revelar que a abordagem inteira está errada, pare e fale com o usuário. Não replaneje sozinho no meio da execução.

## Etapa 3 — Entregar

Só considere a tarefa pronta depois de, nesta ordem:

1. **Rodar os testes.** Falhou, conserte — e conserte a causa, não o teste. Se o teste estiver genuinamente errado, diga isso explicitamente ao usuário em vez de ajustá-lo em silêncio.
2. **Rodar lint e typecheck**, se o projeto tiver.
3. **Revisar o próprio diff** com `git diff`. Procure `console.log` esquecido, código comentado, arquivo temporário, segredo hardcoded, import não usado.
4. **Commitar** no padrão abaixo.
5. **Marcar todos os itens do checklist** e preencher o "Resultado" no arquivo do plano.

Nunca commite com teste quebrado. Se o usuário pedir explicitamente para commitar assim, tudo bem, mas registre no corpo do commit o que está falhando.

### Padrão de commit

Conventional Commits, assunto no imperativo, em português, até 72 caracteres, sem ponto final:

```
<tipo>(<escopo>): <o que muda>

<por que muda, se não for óbvio pelo assunto>
```

Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `perf`.

**Exemplos:**

Mudança: adicionado login com token JWT
→ `feat(auth): adiciona autenticação via JWT`

Mudança: corrigido crash quando o carrinho está vazio
→ `fix(checkout): trata carrinho vazio no cálculo do frete`

Prefira vários commits pequenos e coerentes a um commit gigante. Um item do checklist costuma ser um bom tamanho de commit.

Não adicione coautoria, assinatura de ferramenta ou emoji nas mensagens, a menos que o projeto já use.

### Fechamento

Ao entregar, responda com: o que foi feito em uma ou duas frases, os commits criados, o resultado dos testes e o caminho do arquivo do plano. Nada de relatório longo — o plano já é o registro.

## Retomando um plano existente

Se o usuário pedir para continuar, ou se existir um plano em `docs/plans/` com itens desmarcados relacionados à tarefa: leia o arquivo, confira com `git log` e `git status` o que de fato já foi feito (o checklist pode estar desatualizado se alguém trabalhou fora do fluxo), reconcilie as marcações e siga do primeiro item realmente pendente.

## Quando pular o plano

Nem tudo merece um arquivo. Vá direto ao código, ainda respeitando a Etapa 3, quando a mudança for de uma linha, correção de texto, ajuste de formatação, ou quando o usuário disser explicitamente que não quer plano. Na dúvida, pergunte em uma linha se vale planejar.
