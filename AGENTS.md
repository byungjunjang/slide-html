# AGENTS.md — slide-html (Codex / Claude Code dual-host)

This repo builds **editable PPTX** via a per-slide-HTML → html2pptx pipeline.
`CLAUDE.md` and `.codex/skills/slide/SKILL.md` are the SSOT for *how*. This file
is the **execution contract** for Codex (Claude Code gets the same discipline
for free through its Skill runtime).

`.codex/skills` is a GENERATED mirror of `.claude/skills` — never hand-edit it.
Edit `.claude/skills/...`, then run
`python3 .claude/skills/slide/scripts/dev/sync_codex_mirror.py`.

## When the user asks for slides / PPT / 프레젠테이션 / pptx / 발표 자료

1. **Execute, do not paraphrase.** Run `.codex/skills/slide/SKILL.md`
   step-by-step. Do NOT summarize the procedure and improvise. **No fallback
   reimplementation** — never hand-roll python-pptx, image-flatten a deck, or
   build slides outside `node build.mjs`.

2. **Plan auto-entry.** If the deck is **≥10 slides**, OR a reference file is
   attached/in `inputs/`, OR the brief carries an attitude keyword
   (계획·철저·상세·꼼꼼·체계·제대로·thorough·detailed·comprehensive·polished),
   first run `.codex/skills/slide-plan/SKILL.md` to produce
   `output/<project>-pptx/slide_plan.json`. Only the bypass keywords
   (`간단히`, `빠르게`, `quick`, `simple로`, `plan 없이`) skip this — and when
   bypassing a ≥10-slide deck, write `output/<project>-pptx/.deck-mode` = `simple`.

3. **Single build path.** `init-project.sh` → author per-slide HTML (4 hard
   constraint, compose-don't-copy) → [§2.5 images / §2.6 diagrams] →
   `node build.mjs`. Nothing else produces the `.pptx`.

4. **Image discipline.** Run the §2.5 preflight (`codex --version`,
   `codex login status`). If images are required but real generation is not
   possible, use SKILL §2.5's `<div class="img-placeholder">` fallback. NEVER
   fabricate image files, generate local PIL/solid-color placeholders, or fall
   back silently.

5. **Verify before "done".** Before declaring completion, `node build.mjs` must
   succeed AND
   `python3 .codex/skills/slide/scripts/verify_deck.py output/<project>-pptx`
   must pass. On gate failure, fix the deck — do not declare done.

6. **Preflight (optional, recommended first).**
   `python3 .codex/skills/slide/scripts/preflight.py [--images]`.
