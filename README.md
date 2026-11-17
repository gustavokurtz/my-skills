# my-skills

Claude Code skills I use every day. One turns a sloppy draft into a clear prompt before it is sent, one runs a full plan-then-execute workflow with spec files, subagent reviews and handoffs between sessions, one writes a structured summary before `/compact`, and one turns a technical explanation into a chat message for someone who is not technical.

The skills are written in Portuguese, because that is the language I work in. They still apply to code in any language, and `refinar-prompt` answers in the language of the draft.

## Skills

| Skill | What it does | How to trigger |
| --- | --- | --- |
| `refinar-prompt` | Rewrites a loose prompt (typos, ideas out of order, vague references) into a clear one without dropping any idea, name, number or tone | Ctrl+G in the Claude Code prompt box (after setup), `/refinar-prompt <draft>`, or "refina esse prompt" / "refine my prompt" |
| `trilho` | Development workflow: research, questions, `spec.md`, `plano.md`, autonomous execution with TDD, a code review per phase, handoffs between sessions, and delivery | "vamos planejar", "executa", "continua <slug>", "handoff", or `/trilho` |
| `trilho-init` | Scans the repo once and writes `.trilho/projeto.md` (commands, conventions, fixed rules) for `trilho` to read | `/trilho-init` only (model invocation is disabled) |
| `compactar-contexto` | Writes a summary of the whole session to `.claude/contexto-sessao.md` before `/compact` | "compactar", "o contexto tá cheio", "resumir a sessão", or before running `/compact` |
| `descomplicar` | Writes the message you send to someone non-technical (PO, manager, client) from a loose technical explanation, in plain words and your own voice, and copies it to the clipboard | "explica de forma leiga", "me ajuda a responder a PO", "redige uma resposta pra...", or `/descomplicar` |

## Install

Clone the repo and copy the skills either to your user folder (all projects) or to one project:

```bash
git clone https://github.com/gustavokurtz/my-skills.git

# all projects
cp -r my-skills/.claude/skills/* ~/.claude/skills/

# or a single project
cp -r my-skills/.claude/skills/* /path/to/project/.claude/skills/
```

Requirements: `python3` for the `trilho` context hook. `descomplicar` copies through `clip.exe` and `iconv`, so the clipboard step only works under WSL. The Ctrl+G editor needs `bash`, the `claude` CLI and `timeout` on your PATH.

### Ctrl+G setup for refinar-prompt

In Claude Code, Ctrl+G opens the current prompt in the editor set by `$VISUAL`. `scripts/instalar.sh` points that variable at `scripts/refinar-editor`:

```bash
~/.claude/skills/refinar-prompt/scripts/instalar.sh
```

It writes `env.VISUAL` into `~/.claude/settings.json` (with `python3`, or `jq` as a fallback), keeps the rest of the file and can be run again without duplicating anything. The variable only applies inside Claude Code, in any shell or terminal. If you prefer to do it by hand, add:

```json
"env": { "VISUAL": "/absolute/path/to/refinar-prompt/scripts/refinar-editor" }
```

Open a new Claude Code session afterwards. `trilho-init` also offers to run this script when it finds the skill installed and the setting missing.

## refinar-prompt

The skill treats your text as material to edit, not as a task to run. It does not execute the prompt, answer questions inside it or open the files it mentions.

Rules it follows, in order of priority:

1. **Keep everything.** Every idea, reason, name, path, URL, number, version, code snippet and error message stays, the code and errors character for character. Your tone and first person stay too. Typos and chat abbreviations are fixed silently.
2. **Make it clear to an AI with no context.** Goal and expected result are explicit, vague references are resolved only when the text allows it, and "acho que" becomes a stated uncertainty instead of a fact.
3. **Reorder, never drop.** Goal, context, what to do, constraints, output, how to know it is done.
4. **Invent nothing.** Its own ideas (a verification step, plan mode for a big task) go in a separate suggestions list, not in the prompt.

Short drafts stay short. XML tags such as `<contexto>` or `<tarefa>` are used only for long prompts that mix instructions with pasted logs, code or documents. The answer has four parts: the refined prompt in a code block, what changed, open points (at most 3) and optional suggestions. The rules are based on the Anthropic and OpenAI prompting guides summarized in `referencias/boas-praticas.md`.

### What Ctrl+G does

1. You type a draft in the Claude Code prompt box and press Ctrl+G. Claude Code writes it to a temp file and calls `refinar-editor`.
2. The script sends the draft to a separate `claude -p` call (model `sonnet` by default, no tools, no MCP, no saved session, 180 s timeout). The system prompt is the whole skill: `SKILL.md`, `boas-praticas.md` and `exemplos.md`.
3. A terminal animation runs while it waits. Ctrl+C cancels and leaves the draft as it was.
4. Only the refined prompt goes back into the box, unsent, so you can review it and press Enter. Your main session never sees the draft.
5. The full answer, with what changed, open points and suggestions, is saved to `~/.cache/refinar/ultimo.md`.

Any other file Claude Code opens (a commit message, for example), an empty draft, or a second Ctrl+G on a prompt that was just refined opens your normal editor instead. Settings: `REFINAR_MODELO` (default `sonnet`) and `REFINAR_EDITOR` (default `$EDITOR`, then `nano`). `refinar-editor --demo` shows the animation without calling the model.

### Example

From `referencias/exemplos.md`, trimmed. The draft:

> o login ta quebrando dps q a sessao expira, acho q é no refresh do token mas n tenho certeza, olha em src/auth. faz um teste q reproduz antes de arrumar pfv. e nao mexe no resto q tá funcionando

The refined prompt:

```
O login está quebrando depois que a sessão expira. Acho que o problema está no refresh do token, mas não tenho certeza.

1. Investigue o fluxo de autenticação em src/auth/, principalmente o refresh do token.
2. Antes de corrigir, escreva um teste que reproduza o problema.
3. Depois, corrija o problema.

Não mexa no resto do código, o restante está funcionando.
```

The suggestion to run the test suite after the fix stays out of the prompt and goes in the suggestions list, because the draft did not ask for it.

## trilho

`trilho` ("track") keeps the state of a task in files instead of the conversation, so any fresh session can pick it up. One flow covers every size of task; only the depth of each step changes. A trivial change (one line, a text, formatting) is done directly without a spec.

```
branch → research → questions in chat → spec.md → plano.md → handoff + /clear
→ execute phase (code review → commits → handoff + /clear) → … → last phase → delivery (verification, push/PR)
```

Each task lives in `.trilho/tarefas/YYYY-MM-DD-<slug>/`:

- `spec.md`: what and why, written as plain prose for you to read and edit. Every requirement has an example, the reason and how it is checked. Anything beyond the request is flagged.
- `plano.md`: how. Decisions with their reasons, open empirical questions, and tasks, each with the requirement it covers and a `Teste:` (written first), a `Verificar por:` step, or a goal and budget for empirical work.
- `estado.md`: where things stand. Task status, user decisions, defects with their design cause, discarded hypotheses. A task is only `feito` (done) with evidence.

### Planning

It creates a branch, reads the code before asking anything, and asks only the questions whose answer would change the code or the scope, anchored in the code ("today shipping comes out 0 for an empty cart; keep it or show an error?"). Delivery mode is always asked: commits only, push, or push and PR. It does not ask you to approve the spec; you read it when you want and the next session checks whether you edited it.

Uncertainty is split in two. Decision uncertainty is resolved by asking. Empirical uncertainty (LLM behavior, performance, flaky integrations, bugs with no known cause) is only resolved by running, so it becomes an early probe in the plan with a goal, a budget and a plan B. Every paid LLM call or write to a remote database still asks for your go-ahead in the session.

### Execution

Tasks run one at a time, with no questions except in listed cases: the spec would change, a budget ran out, the fix at the root falls outside the scope, an action is destructive or remote. Before each task it states in one line why and how. Every fix is classified as root cause or symptom, and the skill lists the signs of a patch (a `catch` that swallows the error, an `if` for one value, a longer timeout, a test edited to pass).

### Subagent roles

| Role | Reference | When | Model |
| --- | --- | --- | --- |
| pesquisador (researcher) | `referencias/pesquisador.md` | Planning, when the area is broad or a bug has no known cause. 1 to 3 in parallel, read only, every claim with `file:line` | `Explore`, `sonnet` |
| revisor (reviewer) | `referencias/revisor.md` | End of every phase, on `<last review>..HEAD`. Checks spec coverage, bugs, patches, project rules; reports only findings with confidence ≥ 80 | `general-purpose`, `opus` |
| arquiteto (architect) | `referencias/arquiteto.md` | Second defect with the same design cause, or a fix that failed in a real run. Returns three options: local, failure path only, structural, each with how many normal cases it changes | `general-purpose`, `fable` |

Each subagent starts with a clean context so it does not inherit the session's hypothesis. The session checks their `file:line` claims before acting on them.

### Context and handoff

`trilho` registers a `UserPromptSubmit` and `PostToolUse` hook in its frontmatter (`scripts/contexto.py`). Once the skill is loaded, the hook reads the context size from the transcript and injects a warning at 300k tokens (finish the current task, then hand off) and at 400k (stop now and hand off). Thresholds come from `TRILHO_CONTEXTO_AVISO` and `TRILHO_CONTEXTO_LIMITE`. Handoff is also mandatory after planning and after every phase except the last: the session rewrites `estado.md` and asks you to run `/clear`, then `continua <slug>` resumes.

### trilho-init and OpenCode

Run `/trilho-init` once per project. It reads `package.json`, Makefiles, CI workflows, `git log` and docs to find test, lint, typecheck and build commands, the integration branch, commit convention and sensitive areas (migrations, scripts that touch a database). It runs the test suite once to time it, asking first if it points at anything non-local. Then it asks only what the repo cannot answer and writes `.trilho/projeto.md`. Durable lessons from finished tasks are added back to that file at delivery.

The skills also describe how to run under OpenCode (tool name mapping, `/new` instead of `/clear`). There the context warning comes from `scripts/opencode-contexto.ts`, linked into `~/.config/opencode/plugins/`, which `trilho-init` offers to set up.

When you are unhappy with how the workflow behaved, `trilho` appends an entry to `~/.claude/trilho/feedback.md`, outside any repo, so the skill can be fixed later.

## compactar-contexto

Automatic summaries keep the end of a conversation and lose the start and middle, where decisions and corrections usually are. This skill rereads the whole session and writes a fixed-format summary: goal, timeline (start, middle, end), key decisions with reasons, discarded alternatives, user corrections, current state, next steps and reference details. It saves it to `.claude/contexto-sessao.md`, newest on top, and suggests a `/compact` command that preserves it. If a `trilho` task is in progress, the `trilho` handoff is used instead.

## descomplicar

You paste whatever you have (jargon, out of order, the question the other person asked) and get back the message to send, written as you would write it in a work chat. The skill treats the text as material: it does not investigate the code or try to fix the problem.

- **Answer first.** The message starts with the answer to what the person asked, then only the context they need to accept it, then the next step (who does what).
- **The concrete fact, not an analogy.** The reason comes from the fact that convinces ("the test passes with or without the fix"). An analogy is used only when the fact cannot do it, in one sentence.
- **No backstage.** What changed in the code, how the issue was found, service names, environments and dev acronyms stay out. Their words stay in ("checklist", "PRD"); dev terms become what they mean in the other person's field.
- **Sounds like you.** Colloquial pt-BR, first person, 2 to 6 sentences, no headings, bold or emoji. If you paste earlier messages, it copies your style. A list of AI tells (staged metaphors, punchlines, "não é X, é Y", em dashes, dangling gerunds, corporate filler) is checked and rewritten before showing.
- **Invents nothing.** No deadlines, promises or names you did not give. If a missing fact would change the message, it says which one after the text.

The final message goes to the Windows clipboard through `scripts/copiar.sh` (UTF-16LE so accents survive, CRLF line endings) and is shown in the chat as plain text, followed by "Copiado.". "Mais curto" or "mais formal" adjusts the last version and copies it again.

## Layout

```
.claude/skills/
  refinar-prompt/
    SKILL.md
    referencias/        prompting guidelines and before/after examples
    scripts/            instalar.sh, refinar-editor (Ctrl+G)
  trilho/
    SKILL.md
    referencias/        one file per step and per subagent role
    modelos/            templates for spec.md, plano.md, estado.md
    scripts/            contexto.py (hook), opencode-contexto.ts (plugin)
  trilho-init/
    SKILL.md
    modelo-projeto.md   template for .trilho/projeto.md
  compactar-contexto/
    SKILL.md
  descomplicar/
    SKILL.md
    scripts/            copiar.sh (clipboard via clip.exe)
```
