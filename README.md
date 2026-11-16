# bookwyrm-skills

The skills for David's physical builds: lanterns, boxes, dioramas and anything else that ends up in The Hoard. Skills live here; what they build lives in the store (the library on David's Mac, backed up to R2), and The Hoard is how David sees it.

## The map

```
workshop/SKILL.md     how every build saves drafts to The Hoard and gets promoted (start here)
families/             one construction skill per kind of product
  lithophane-lanterns/      LED lithophane lanterns
  printable-container/      boxes, chests, cases and enclosures
  layered-diorama/          hand-modelled scene dioramas built in layers
  generated-scene-diorama/  multi-piece dioramas generated from one concept under a credit budget
shared/               method shared by more than one family
  print-profile/print-profile.md   printers, build volumes, materials, proven print and fit settings
  joints-and-assembly/glued-joints.md   the tab rule: printed alignment tabs, never dowels
  lithophanes/lithophanes.md   lit image panels: source images, relief, recipe, detail limits, tests
  lighting-and-electronics/lighting-and-electronics.md   WLED scenes, boards, light-path tests
  concept-and-faithfulness/   reference authority, faithfulness review, compromise register, art pipeline
  image-to-3d/image-to-3d.md   engines and prices, sculpt input images, four-view sheets, hidden mass
  evidence-and-claims/evidence-and-claims.md   the evidence ladder, statuses, export and slicer checks, physical tests
  design-playbook/design-playbook.md   lessons from the Shire and Mirkwood cases and a ten-gate default workflow
  blender-tooling/render-home/   home-library lantern renders
tools/check_piece_json.py        checks piece.json in version folders still locked in a family repo
```

Each family folder holds its `SKILL.md`, its `references/`, any scripts and tests, and a `family.json`: the family's name, what it builds, its kinds, its version numbering, and the repos that hold its projects. The Hoard's Ideas page reads families from these files.

## How a build project uses this repo

1. Attach this repo to the build project, beside the family repo (bookwyrm-lanterns, bookwyrm-boxes, ...).
2. Follow the family's construction skill for the build itself, and `workshop` for saving it: files go to The Hoard as draft change sets, and David promotes them.
3. Keep generator scripts, parameters, notes and the checkpoint in the family repo. Meshes, Blender files, renders and print files go to the store, not to git.

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

Until a family repo is switched over to this repo, its own copy of the skill is the one in use there. The plan is in bookwyrm-rpg `.hero/planning/initiatives/skills-and-store/spec.md`.

## Tests

```sh
uvx pytest families/printable-container/tests
```
