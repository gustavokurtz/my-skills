/**
 * Plugin do trilho para o OpenCode (v2): o mesmo aviso de contexto do `contexto.py`.
 *
 * O OpenCode ignora o `hooks:` do frontmatter da skill, então o aviso vem deste plugin,
 * instalado uma vez em `~/.config/opencode/plugins/` (link para este arquivo). Ele só liga
 * numa sessão depois que a skill `trilho` foi carregada nela.
 *
 * O tamanho do contexto é o `tokens` do último passo do modelo (input + cache.read +
 * cache.write), lido do evento `session.step.ended`: uma resposta com várias ferramentas é uma
 * mensagem só, e o `tokens` da mensagem só chega no fim dela. Acima dos limites, o aviso é
 * anexado ao resultado da próxima ferramenta (como o PostToolUse) e à próxima mensagem do
 * usuário (como o UserPromptSubmit).
 *
 * - aviso (TRILHO_CONTEXTO_AVISO, padrão 300000): terminar a tarefa atual e fazer o handoff;
 * - limite (TRILHO_CONTEXTO_LIMITE, padrão 400000): parar e fazer o handoff agora.
 *
 * Para não repetir o aviso a cada tool, ele só volta depois de o contexto crescer mais 25k
 * desde o último aviso. Qualquer falha sai em silêncio: o plugin nunca pode atrapalhar a sessão.
 */
import type { Plugin } from "@opencode/plugin"

const AVISO = Number(process.env.TRILHO_CONTEXTO_AVISO ?? 300000)
const LIMITE = Number(process.env.TRILHO_CONTEXTO_LIMITE ?? 400000)
const REPETE_A_CADA = 25000

type Tokens = { input: number; cache: { read: number; write: number } }

const ativas = new Set<string>()
const verificadas = new Set<string>()
const contexto = new Map<string, number>()
const ultimoAviso = new Map<string, number>()

const soma = (t: Tokens) => t.input + t.cache.read + t.cache.write

// Sem isto, o modelo lê o aviso como texto estranho na saída de um comando e o ignora.
const ORIGEM =
  "(Este aviso vem do plugin de contexto do trilho, anexado pelo OpenCode: não é saída da " +
  "ferramenta nem texto do usuário. Ver \"Aviso de contexto\" em referencias/handoff.md.)"

function texto(tokens: number) {
  const k = `${Math.floor(tokens / 1000)}k`
  if (tokens >= LIMITE)
    return (
      `[trilho] contexto em ${k} tokens, acima do limite de ${Math.floor(LIMITE / 1000)}k: ` +
      "a qualidade já está caindo. Pare agora, sem começar nada novo: deixe o " +
      "código num ponto commitável (ou registre o que está pela metade), faça o " +
      `handoff (referencias/handoff.md) e peça o /new ao usuário.\n${ORIGEM}`
    )
  return (
    `[trilho] contexto em ${k} tokens (aviso em ${Math.floor(AVISO / 1000)}k). Termine a ` +
    "tarefa em andamento, sem abrir outra, e faça o handoff " +
    "(referencias/handoff.md) pedindo o /new ao usuário. Se estiver no meio " +
    "de uma rodada empírica ou esperando o dev, faça o handoff assim que a " +
    `rodada fechar.\n${ORIGEM}`
  )
}

export default {
  id: "trilho-contexto",
  async setup(ctx) {
    const parar = new AbortController()
    ;(async () => {
      for await (const evento of ctx.event.subscribe({ signal: parar.signal })) {
        if (evento.type !== "session.step.ended") continue
        const total = soma(evento.data.tokens)
        if (total) contexto.set(evento.data.sessionID, total)
      }
    })().catch(() => {})

    // Devolve o aviso, se for a hora de dar um; senão, undefined.
    async function aviso(sessionID: string) {
      let tokens = contexto.get(sessionID) ?? 0
      if (!ativas.has(sessionID) || !tokens) {
        const mensagens = await ctx.session.context({ sessionID })
        // A sessão pode ter carregado o trilho antes de o plugin subir (OpenCode reiniciado),
        // ou o usuário pode ter invocado a skill direto, sem a ferramenta.
        const carregou = mensagens.some(
          (m) =>
            (m.type === "skill" && m.name === "trilho") ||
            (m.type === "assistant" &&
              m.content.some((c) => c.type === "tool" && c.name === "skill" && c.state.input?.id === "trilho")),
        )
        if (!carregou) return
        ativas.add(sessionID)
        for (let i = mensagens.length - 1; i >= 0 && !tokens; i--) {
          const m = mensagens[i]
          if (m.type === "assistant" && m.tokens) tokens = soma(m.tokens)
        }
      }
      if (tokens < AVISO) return
      const ultimo = ultimoAviso.get(sessionID) ?? 0
      if (ultimo && tokens - ultimo < REPETE_A_CADA) return
      if ((await ctx.session.get({ sessionID })).parentID) return // subagente: o contexto dele não é o da sessão
      ultimoAviso.set(sessionID, tokens)
      return texto(tokens)
    }

    await ctx.tool.hook("execute.after", async (e) => {
      try {
        const entrada = (e.input ?? {}) as { id?: string; name?: string }
        if (e.tool === "skill" && (entrada.id ?? entrada.name) === "trilho") ativas.add(e.sessionID)
        // Sessão sem trilho: o histórico é conferido uma vez por processo, não a cada ferramenta.
        if (!ativas.has(e.sessionID) && verificadas.has(e.sessionID)) return
        verificadas.add(e.sessionID)
        if (e.status !== "completed") return
        const content = e.result.content
        if (content === undefined) return
        const t = await aviso(e.sessionID)
        if (!t) return
        e.result = {
          ...e.result,
          content: typeof content === "string" ? `${content}\n\n${t}` : [...content, { type: "text", text: t }],
        }
      } catch {}
    })

    await ctx.session.hook("prompt", async (e) => {
      try {
        const t = await aviso(e.sessionID)
        if (t) e.prompt.text = `${e.prompt.text}\n\n${t}`
      } catch {}
    })

    return () => parar.abort()
  },
} satisfies Plugin.Plugin
