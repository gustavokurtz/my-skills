# Feedback sobre o trilho

Registra a insatisfação do usuário com o jeito como o trilho trabalha, para que a skill seja corrigida depois. Na correria, ele não tem tempo de relatar; o registro faz isso por ele.

## Quando registrar

- **Pedido explícito:** "feedback: …", "anota isso pro trilho", "isso tem que mudar na skill".
- **Sinal de insatisfação**, mesmo sem pedido:
  - corrigiu a mesma coisa duas vezes;
  - "não era isso", "de novo?", "já falei", ou irritação;
  - recusou uma ação ou interrompeu no meio;
  - precisou lembrar você de uma regra que a skill já tem.

Registre o que é sobre o processo: como o trilho pesquisa, pergunta, planeja, executa, revisa, faz handoff e entrega. Um erro pontual de código que se corrige na própria tarefa não é feedback, a menos que mostre um padrão (ex.: remendo em vez de causa). Na dúvida, registre: uma entrada a mais custa pouco, e a que falta se perde.

Registre na hora, avise em uma linha ("anotei no feedback do trilho: <resumo>") e siga com a tarefa. Não pergunte se pode.

## Onde

`~/.claude/trilho/feedback.md`, fora do repositório: o arquivo junta o feedback de todos os projetos e não vai para o git de nenhum. Se não existir, crie com o título `# Feedback do trilho`. Acrescente no fim e nunca reescreva entradas antigas.

## Formato

```markdown
## AAAA-MM-DD HH:MM — <resumo em uma linha>

- **Status:** aberto
- **Projeto:** <nome do repo> · **Etapa:** planejamento | execucao (Tn) | entrega | handoff
- **Gatilho:** explícito | detectado (<qual sinal>)
- **O que aconteceu:** <o que você fez e o que o usuário esperava, em uma ou duas frases>
- **Palavras do usuário:** "<literais>"
- **Na skill:** <a regra que falhou ou faltou, com o arquivo; ex.: `referencias/planejamento.md`, passo 4>
- **Sugestão:** <o que mudar na skill para não acontecer de novo>
```

Sem código, segredo, credencial, dado de cliente ou nome de pessoa (troque por papel: "o PO", "um colega"), porque o arquivo sai do projeto. Descreva o comportamento, não o conteúdo.

## Processar

Acontece fora das tarefas, no repositório das skills, quando o usuário pedir ("processa o feedback do trilho"): leia as entradas `aberto`, agrupe pela causa na skill, apresente o diagnóstico e o plano de mudança e espere a aprovação antes de editar. Depois da correção, mude o status de cada entrada para `resolvido em <commit>`.
