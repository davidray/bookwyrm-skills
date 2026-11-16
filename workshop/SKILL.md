---
name: workshop
description: Save a 3D-printable build (lantern, box, chest, diorama or any physical product) to The Hoard as a draft, and promote it only when David asks. Use before starting work on an item, whenever a build has files David should see, at a construction skill's lock or release step, and at the end of a session that changed meshes without saving them.
---

# Workshop

The Hoard is David's catalogue of everything he builds. It runs on his Mac over one store, the library at `~/bookwyrm/dungeons-and-dragons/library`, which is backed up to R2 every night. Every product is an item there with numbered revisions. Two pointers say where it stands:

- **current**: the promoted revision that the catalogue, downloads and listings show;
- **head**: the newest revision. While it is a draft, it sits after current and changes nothing anyone sees.

A build saves files as drafts. David promotes a draft, and promotion gives it its version label and status. No file is copied when a draft is promoted.

The construction skill (in `families/`) owns what a version must contain and when it is ready. This skill owns how the files get into the store, and it is the same for every family.

## Where things live

- **Family repo** (bookwyrm-lanterns, bookwyrm-boxes, bookwyrm-dioramas, ...): generator scripts, parameter files, design notes, the checkpoint, review notes, and small SVG or DXF art. As a rule, text and anything under 1 MB that a person might diff goes in git.
- **The store**: meshes, Blender files, renders, images and print files. Don't commit these to the family repo for new work. Locked version folders already in git stay where they are, and history is never rewritten.

## 1. Before you build

Read the item first with `read_piece` from the library tools. It tells you:

- `current_revision` and `head_revision`;
- the current version, status and rights;
- the files you will be building on.

`list_drafts` with the slug shows any open drafts and what each one changed. If there is an open draft you didn't make, say so and build on it, or ask which one to build on. For a new product, check that the slug is unused (`list_pieces`), one per product across every repo, kebab case, never reused.

## 2. Build anywhere

Work wherever suits the job: Blender on the Mac, a cloud container, project files. Commit generator scripts and notes to the family repo as you go, so that every saved draft can name the commit that made it.

## 3. Save a draft (a change set)

Save a draft whenever David should see the state of a build: a blockout for review, a candidate version, a checkpoint before a risky change, or when a construction skill says to lock or release.

A change set is one folder in the inbox, holding the item's **complete** file set and a `piece.json`:

```
~/bookwyrm/dungeons-and-dragons/inbox/<slug>/<change set>/
  piece.json
  print/...            every print file, at the paths the components name
  renders/...          images; the first displayable render is the cover
  source/...           Blender files and other sources worth keeping
```

Change sets are for pieces. A collection (piece set) changes only when David asks; save it with `import_piece_set` and `draft=True`.

Name the change set something short and unique for the item, such as `cs-2026-11-16-body-thinner`. Include unchanged files too: the store recognises them by hash and keeps one copy.

Then call `submit_change_set(slug, change_set, expected_revision, note)` with:

- `expected_revision`: the `head_revision` you read, or 0 for a new item;
- `note`: one sentence on what this draft is.

Call it with `dry_run=True` first if you're unsure: it lists every problem and writes nothing. On success, the store holds a new draft revision and the inbox folder is gone. A refusal writes nothing and leaves the folder for you to fix. On `Revision conflict`, someone saved a newer draft: read the item again and decide with David before you build over it.

Then tell David in one line what the draft is, for example "Dragon Mountain draft r12 is in The Hoard: body 4 mm thinner. Promote it from Catalogue → Drafts when you're happy."

### From a cloud container

The store's tools run on the Mac. In a cloud thread linked to it, the library tools and the inbox folder come through the device link:

1. Build the change set in the project files.
2. Copy it into `inbox/<slug>/<change set>/` with the device file tools (up to 400 MB a file).
3. Call `submit_change_set`.

If the Mac is asleep or not linked, keep the change set in the project files, say so in one line, and submit it next time. Nothing is lost.

## 4. piece.json

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
- **rights:** `design` is `original` or `ai-assisted`. `ip` is the third-party world in kebab case (`middle-earth`, `zelda`) or `none`. Any `ip` other than `none` must have `licence` `personal-use-only`. Original designs default to `all-rights-reserved`.
- **source:** the family repo, the product's folder, and the commit of the generator code that made these files. Push that commit first.
- **components:** every print file (`.stl`, `.3mf`, `.step`, slicer files) is named by one component, with only `name`, `file`, `part_id`, `quantity` (how many to print; never `count`), `printer` and `material`.
- **uses:** shared pieces (a hardware plate, a controller) pinned as `{piece, revision}`, only when the store already has that revision.

`submit_change_set` with `dry_run=True` is the check for a change set. `tools/check_piece_json.py` in this repo checks the version folders already locked in a family repo, which need `version` and `status`.

## 5. Promotion is David's

A draft becomes the current revision only when David promotes it: with **Promote** on Catalogue → Drafts in The Hoard, or by asking in your thread for that exact draft. Only then call `promote_draft(record, slug, revision, expected_revision, version, status)`, where `expected_revision` is the current revision you read. Never promote on your own judgement, and never promote a different draft from the one he named.

At promotion:

- **version** follows the family's numbering (see its `family.json`). Versions compare as numbers, so `v1.10` is newer than `v1.9`.
- **status** is the highest claim the evidence supports (see [evidence and claims](../shared/evidence-and-claims/evidence-and-claims.md#status-in-the-hoard)): `concept`, `digitally-validated`, `prototype` (printed), `interface-fit-tested`, `qualified`. A render or a slice is never more than `digitally-validated`.

A change to any mesh, size, clearance, pocket or assembly position is a new draft. Images, listings and the final cut are edited on the current revision in The Hoard and need no draft.

## 6. End of session

If a session changed an item's meshes, sizes or interfaces without saving a draft, say so in one line, such as "Dragon Mountain has unsaved changes since r12. Save them as a draft?", and save only if David says yes.
