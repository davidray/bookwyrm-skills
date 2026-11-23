---
name: workshop
description: Keep a 3D-printable build (lantern, box, chest, diorama or any physical product) in The Hoard: its build record (stage, gate, brief, checkpoint) while it is made, and its files as drafts that David promotes. Use before starting or resuming work on an item, at every gate, whenever a build has files David should see, at a construction skill's lock or release step, and at the end of a session.
---

# Workshop

Paths such as `shared/...` and `families/...` are from the root of the bookwyrm-skills repo (`~/code/bookwyrm-skills` on David's Mac). Open them from there: a `../` link resolves wrongly when this skill is opened through a link in `~/.claude/skills/`.

The Hoard is David's catalogue of everything he builds. It runs over one store, the library at `~/bookwyrm/dungeons-and-dragons/library`, which is backed up to R2 every night. Every product is an item there with numbered revisions. Two pointers say where it stands:

- **current**: the promoted revision that the catalogue, downloads and listings show;
- **head**: the newest revision. While it is a draft, it sits after current and changes nothing anyone sees.

A build saves files as drafts. David promotes a draft, and promotion gives it its version label and status. No file is copied when a draft is promoted.

The construction skill (in `families/`) owns what a version must contain and when it is ready. This skill owns how the files get into the store, and it is the same for every family.

## Where things live

- **The build record** (in the store): the piece's brief, its checkpoint, its stage, the gate waiting on David and a few images. Design notes, decisions and review notes go in the checkpoint. This is the project's text: it is not committed to git, and The Hoard's Builds board shows it. See section 1.
- **Family repo** (bookwyrm-lanterns, bookwyrm-boxes, bookwyrm-dioramas, ...): generator scripts, parameter files and small SVG or DXF art. Every draft also carries the scripts that made it in its `source/` folder.
- **The store**: meshes, Blender files, renders, images and print files. Don't commit these to the family repo for new work. Locked version folders already in git stay where they are, and history is never rewritten.

An older project may still have `BRIEF.md` and `CHECKPOINT.md` in its family repo. If it has no build record yet, create one from them (title, family, brief and checkpoint). From then on the record is the one to keep current; leave the old files as they are.

## 1. The build record

A build is the piece while it is being made. The library tools keep it: `read_build`, `write_build`, `list_builds`, and `build_schema` for the stages and gate kinds. The slug is the piece's slug.

- **Starting or resuming:** `read_build(slug)` gives the record, the brief and the checkpoint. Read them before anything else; they replace the project's `BRIEF.md` and `CHECKPOINT.md`. For a new piece, create the record with `write_build(slug, 0, title=..., family=..., brief=..., summary=...)` once the brief is settled.
- **Every write** passes `expected_revision`, the `revision` you last read (0 creates it). On `Revision conflict`, someone else changed it: read it again and merge your change into what is there.
- **Keep it current:** set `stage` as the build moves (brief, concept, design, modelling, print-test), `summary` to one line on where it stands, and `checkpoint` to the whole checkpoint text whenever the construction skill says to update the checkpoint. Set `piece` once the piece exists in the store.
- **At every gate**, before you ask David: set `gate_kind` (concept, paid-call, physical-check or other), `gate_question` (one line summing up the gate) and `gate_details`: the numbered `decisions` as you will ask them, each with your `recommendation`; the `assumed` list ("Still assumed:"); the critic's open FAILs as `critic_fails`; the `images` he should see, by name; for a budget gate the `budget_usd` you ask for; and for any gate that asks him to print (a physical check, a test coupon), `print_files`. Put those images on the record in the same write, with `images` listing them as absolute paths on the machine where the library tools run (`images` replaces the whole list).
  - **In The Hoard** (your runtime note says which surface you are on), David decides in Approvals, not in the chat. After writing the gate, call `review_subject(kind="build_gate", id=<slug>)` and `submit_for_review` with that kind and id and the revision and sha256 it gives, tell him in a line that the gate is in Approvals, and end your turn. His decision arrives as a message from him starting "Gate decided:", with one answer per numbered decision and his note: read it as his answer. The Hoard clears the gate, and approving a budget gate sets `budget_usd`; record his answer, in his words, in the checkpoint.
  - **Print files:** David does not know or care where files are on disk, and he prints from The Hoard. Before a gate that asks him to print anything, save a draft (section 4) holding every file he is to print, under `print/`, with the build's `piece` set to that item. Then list exactly those files in `gate_details.print_files`, by their paths in that draft (for example `print/charger-coupon/01-charger-face-r2.stl`); the write refuses a path the draft lacks. The Hoard shows them first in the build's Files pane, under "Print files", each ready to open in Bambu Studio. In the gate and the chat, name the files and say they are in the Files pane; never give him a filesystem path, and never leave a print file only in a build folder.
  - **In a terminal**, ask him in the chat. When he answers, write again with `clear_gate=True` and record his answer, in his words, in the checkpoint.
- **Costs:** the record keeps the build's budget and every outlay, and The Hoard shows spend against the budget and where it went.
  - **Budget:** recommend one with the brief and ask David to approve it, before the first paid call. Build it from the plan, one line per kind of paid call the construction skill expects: concept rounds, part or panel art, a 3D generator call per part, and anything else priced in the [image to 3D](../shared/image-to-3d/image-to-3d.md#engines-and-prices) (`shared/image-to-3d/image-to-3d.md`) prices, each as count × price. Add a reserve that covers at least one part retry (new art plus new 3D) and is never less than 10% of the calls, and filament for the expected test prints. The [art pipeline](../shared/concept-and-faithfulness/art-pipeline.md#spending) (`shared/concept-and-faithfulness/art-pipeline.md`) has a typical split to check the lines against. Give the total in dollars, rounded up to the next whole dollar, as its own numbered decision, with the lines beneath it, and say that approving it lets you make those calls without asking again. Record it as a gate (`gate_kind` `paid-call`, the total as `gate_details.budget_usd`). In a terminal, set `budget_usd` only when he approves; in The Hoard, approving the gate sets it. Either way, put his answer in his words in the checkpoint. If he names a different figure, that is the budget; if it can't cover the plan, say which parts it leaves out.
  - A build already under way with no budget gets a recommendation the next time it resumes: what it has spent plus the plan for what is left.
  - **An approved budget is the approval to spend.** Inside it, make the paid calls the work needs, retries included, without asking, and log each one. Before a call that would take spend past the budget, or as soon as the reserve can no longer cover one part retry, stop spending, re-plan, and recommend a raised budget as its own decision: what has been spent and on what, what is left to do, and the new total. Spend again only when he approves it. Set a helper's caps to the approved budget, and raise them only when he raises it.
  - **Every paid call** is logged with `costs`, in the same write that records it in the checkpoint. A build that calls the 3D generator or the image model through `tripo_helper.py` passes `tp.build_costs()` whole after each call and after each `tp.poll()`: each entry has a stable id, so the same entries sent again replace rather than add, and an estimate becomes the actual once the credits are known. Log any other paid call (a Builder tool, a call made another way) as one entry yourself: `{id, category, what, usd, estimate, retry}`, with `id` the task or job id if there is one, `category` one of `image`, `3d-model`, `filament`, `other`, `estimate: true` until the real price is known, and `retry: true` when it redoes an earlier call.
  - **Filament:** after a print test, log what the slicer reports as one `filament` entry per plate (its cost if the slicer shows one, otherwise grams with the price per kilo David gave), `estimate: true`.
  - **At every gate**, give the build's spend so far against its budget.
- **Pausing:** stage `paused`, with the steps a fresh session needs to resume in the checkpoint. **Finished:** stage `done`, only when David says the piece is finished.

## 2. Before you build

Read the item first with `read_piece` from the library tools. It tells you:

- `current_revision` and `head_revision`;
- the current version, status and rights;
- the files you will be building on.

`list_drafts` with the slug shows any open drafts and what each one changed. If there is an open draft you didn't make, say so and build on it, or ask which one to build on. For a new product, check that the slug is unused (`list_pieces`), one per product across every repo, kebab case, never reused.

## 3. Build anywhere

Work wherever suits the job: Blender on the Mac, a cloud container, project files. Commit generator scripts to the family repo as you go, so that every saved draft can name the commit that made it, and keep the build record current (section 1).

## 4. Save a draft (a change set)

Save a draft whenever David should see the state of a build: a blockout for review, a candidate version, a checkpoint before a risky change, or when a construction skill says to lock or release.

A change set is one folder in the inbox, holding the item's **complete** file set and a `piece.json`:

```
~/bookwyrm/dungeons-and-dragons/inbox/<slug>/<change set>/
  piece.json
  print/...            every print file, at the paths the components name
  renders/...          images; the first displayable render is the cover
  source/...           the generator scripts and parameters that made these files, Blender files and other sources worth keeping
```

Change sets are for pieces. A collection (piece set) changes only when David asks; save it with `import_piece_set` and `draft=True`.

Name the change set something short and unique for the item, such as `cs-2026-11-16-body-thinner`. Include unchanged files too: the store recognises them by hash and keeps one copy.

Then call `submit_change_set(slug, change_set, expected_revision, note)` with:

- `expected_revision`: the `head_revision` you read, or 0 for a new item;
- `note`: one sentence on what this draft is.

Call it with `dry_run=True` first if you're unsure: it lists every problem and writes nothing. On success, the store holds a new draft revision and the inbox folder is gone. A refusal writes nothing and leaves the folder for you to fix. On `Revision conflict`, someone saved a newer draft: read the item again and decide with David before you build over it.

Then tell David in one line what the draft is, for example "Dragon Mountain draft r12 is in The Hoard: body 4 mm thinner. Promote it from Catalogue → Drafts when you're happy." Its print files are in the build's Files pane, so point him there, not to a path.

### From a cloud container

The store's tools run on the machine that holds the store. In a cloud thread linked to it, the library tools and the inbox folder come through the device link:

1. Build the change set in the project files.
2. Copy it into `inbox/<slug>/<change set>/` with the device file tools (up to 400 MB a file).
3. Call `submit_change_set`.

If that machine is asleep or not linked, keep the change set in the project files, say so in one line, and submit it next time. Nothing is lost.

## 5. piece.json

The full rules are in bookwyrm-rpg `services/library/docs/piece-json.md`. In a change set, `version` and `status` may be left out: they are set at promotion.

```json
{
  "piece_json": 1,
  "slug": "dragon-mountain",
  "title": "Dragon Mountain lantern",
  "kind": "lamp",
  "rights": {"design": "ai-assisted", "ip": "none", "licence": "all-rights-reserved"},
  "description": "One or two sentences a buyer would read.",
  "themes": ["dragons"],
  "tags": ["lantern", "led"],
  "size_mm": {"x": 172, "y": 145, "z": 238},
  "source": {"repo": "davidray/bookwyrm-lanterns", "path": "lanterns/dragon-mountain", "commit": "<40-character commit>"},
  "components": [{"name": "Plinth", "file": "print/dragon-mountain_plinth.3mf"}]
}
```

- **kind:** diorama, figurine, lamp, ornament, terrain, prop or container.
- **rights:** `design` is `original` or `ai-assisted`. `ip` is the third-party world in kebab case (`middle-earth`, `zelda`) or `none`. Any `ip` other than `none` must have `licence` `personal-use-only`. Original designs default to `all-rights-reserved`. A public-domain artist (Doré, Van Gogh, Monet) is a theme, not an ip: `ip` `none` with the artist in `themes`, since The Hoard refuses `all-rights-reserved` with an ip.
- **Selling** (David, 2026-11-17): only original designs (`all-rights-reserved`) are offered for sale. Middle-earth and Zelda pieces are personal and non-commercial; when one is shown publicly it uses no Tolkien or Nintendo names (Lonely Mountain appears only as "Dwarven lantern", a detail demo, not for sale). The Gift lanterns are `personal-use-only` because the song's rights aren't cleared, so sales copy calls the stable a nativity lantern and avoids the song's name and lyrics. Photos of unpainted prints say they are unpainted, and copy says "3D printed", not "made by hand".
- **source:** the family repo, the product's folder, and the commit of the generator code that made these files. Push that commit first.
- **components:** every print file (`.stl`, `.3mf`, `.step`, slicer files) is named by one component, with only `name`, `file`, `part_id`, `quantity` (how many to print; never `count`), `printer` and `material`.
- **uses:** shared pieces (a hardware plate, a controller) pinned as `{piece, revision}`, only when the store already has that revision.

`submit_change_set` with `dry_run=True` is the check for a change set. `tools/check_piece_json.py` in this repo checks the version folders already locked in a family repo, which need `version` and `status`.

## 6. Promotion is David's

A draft becomes the current revision only when David promotes it: with **Promote** on Catalogue → Drafts in The Hoard, or by asking in your thread for that exact draft. Only then call `promote_draft(record, slug, revision, expected_revision, version, status)`, where `expected_revision` is the current revision you read. Never promote on your own judgement, and never promote a different draft from the one he named.

At promotion:

- **version** follows the family's numbering (see its `family.json`). Versions compare as numbers, so `v1.10` is newer than `v1.9`.
- **status** is the highest claim the evidence supports (see [evidence and claims](../shared/evidence-and-claims/evidence-and-claims.md#status-in-the-hoard) (`shared/evidence-and-claims/evidence-and-claims.md`)): `concept`, `digitally-validated`, `prototype` (printed, not yet production), `interface-fit-tested`, `qualified`. Files that have not been printed are never more than `digitally-validated`. Use the same word in the README as in the status. A render or a slice is never more than `digitally-validated`.

A change to any mesh, size, clearance, pocket or assembly position is a new draft. Images, listings and the final cut are edited on the current revision in The Hoard and need no draft.

A change to the records only (README, PRINT-AND-TEST, piece.json) needs a draft when David should see it there: before he prints from The Hoard, or when a build is parked, so the item's README matches the decisions he made. Otherwise let the next draft carry it. A change set still holds the complete file set: read the head revision with `read_piece`, copy every unchanged file from the project's build folders (or fetch it with `piece_file`), add the changed records, and check it with `dry_run=True`. Afterwards, `list_drafts` should show only the records as changed.

## 7. End of session

If a session changed an item's meshes, sizes or interfaces without saving a draft, say so in one line, such as "Dragon Mountain has unsaved changes since r12. Save them as a draft?", and save only if David says yes. Bring the build record up to date before you stop: stage, summary and checkpoint.
