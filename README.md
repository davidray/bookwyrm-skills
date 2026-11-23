# bookwyrm-skills

The skills for David's physical builds: lanterns, boxes, dioramas and anything else that ends up in The Hoard. Skills live here; what they build lives in the store (the library on David's Mac, backed up to R2), and The Hoard is how David sees it.

## The map

```
agents/               the artificer and the critic (roles only; linked into ~/.claude/agents/)
workshop/SKILL.md     how every build keeps its build record and saves drafts to The Hoard (start here)
families/             one construction skill per kind of product
  lithophane-lanterns/      LED lithophane lanterns
  printable-container/      boxes, chests, cases and enclosures
  layered-diorama/          hand-modelled scene dioramas built in layers
  generated-scene-diorama/  multi-piece dioramas generated from one concept under a credit budget
  campaign-packet/          D&D campaigns designed in a chat, and the packet for a campaign box
  miniature-roster/         sets of miniatures designed in a chat and made by Builder as one batch
shared/               method shared by more than one family
  print-profile/print-profile.md   printers, build volumes, materials, proven print and fit settings
  joints-and-assembly/glued-joints.md   the tab rule: printed alignment tabs, never dowels
  lithophanes/lithophanes.md   lit image panels: source images, relief, recipe, detail limits, tests
  lighting-and-electronics/lighting-and-electronics.md   WLED scenes, boards, light-path tests
  concept-and-faithfulness/   reference authority, faithfulness review, compromise register, art pipeline
  image-to-3d/image-to-3d.md   engines and prices, sculpt input images, four-view sheets, hidden mass, cutting function into generated art
  evidence-and-claims/evidence-and-claims.md   the evidence ladder, statuses, export and slicer checks, physical tests
  independent-review/independent-review.md   the critic reviews before every gate: how it is briefed, what it checks and reports, and how its verdict is used
  design-playbook/design-playbook.md   twenty design rules from the Shire and Mirkwood travel cases
  blender-tooling/render-home/   home-library lantern renders
tools/check_piece_json.py        checks piece.json in version folders still locked in a family repo
```

Each family folder holds its `SKILL.md`, its `references/`, any scripts and tests, and a `family.json`: the family's name, what it builds, its kinds, its version numbering, and the repos that hold its projects. The Hoard's Ideas page reads families from these files.

## How a build project uses this repo

1. Attach this repo to the build project, beside the family repo (bookwyrm-lanterns, bookwyrm-boxes, ...).
2. Follow the family's construction skill for the build itself, and `workshop` for saving it: files go to The Hoard as draft change sets, and David promotes them.
3. Keep the brief, the checkpoint and the build's stage and gates in its build record in the store (`workshop` section 1); The Hoard's Builds board shows them. Generator scripts and parameters go in the family repo and in each draft's `source/`. Meshes, Blender files, renders and print files go to the store, not to git.

On David's Mac the clone is `~/code/bookwyrm-skills`, `~/.claude/skills/` links to `workshop` and each family folder, and `~/.claude/agents/` links to each file in `agents/`:

```sh
S="$HOME/code/bookwyrm-skills"; mkdir -p ~/.claude/agents; for a in artificer critic; do ln -sfn "$S/agents/$a.md" ~/.claude/agents/$a.md; done
```

The agents hold roles only; the vocabulary and how a session runs a build are in bookwyrm-artificery's `CLAUDE.md`. A link to `shared/` or another family is written relative to the repo, and every such link also names its path from the repo root (for example `shared/image-to-3d/image-to-3d.md`), so open it from the clone rather than through `~/.claude/skills/`. Fetch before a build: a clone behind `origin/main` gives stale rules.

Paths in a skill such as `lanterns/<slug>/...` or `projects/<slug>/...` mean that folder in the family's repo (see its `family.json`).

## Where these came from

The family skills were copied in with their git history (blame still works):

| Here | From |
|---|---|
| `families/lithophane-lanterns/` | bookwyrm-lanterns `SKILL.md`, `agents/`, `references/` |
| `shared/design-playbook/` | bookwyrm-boxes `shared/3D-DESIGN-PLAYBOOK.md` |
| `shared/blender-tooling/render-home/` | bookwyrm-lanterns `tools/render-home/` |
| `families/printable-container/` | bookwyrm-boxes `skills/printable-container/` |
| `families/layered-diorama/` | bookwyrm-dioramas `skills/layered-diorama/` |
| `families/generated-scene-diorama/` | David's account skill of that name |
| `workshop/` | bookwyrm-rpg `services/library/skills/publish-to-the-hoard/`, rewritten for drafts and change sets |
| `tools/check_piece_json.py` | bookwyrm-rpg `services/library/tools/` |
| `agents/` | bookwyrm-artificery `agents/` |

Every family repo has switched over: its old skill folder holds only a pointer here. The design is in bookwyrm-rpg `.hero/planning/initiatives/skills-and-store/spec.md`.

## Tests

```sh
uvx pytest families/printable-container/tests
```
