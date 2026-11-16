---
name: publish-to-the-hoard
description: Lock a finished version of a 3D-printable build (lantern, box, chest, diorama or any physical product) so it reaches The Hoard, David's catalogue. Use at the lock or release step of a construction skill, when David approves a version for printing, or at the end of a build session that changed meshes without locking.
---

# Publish to The Hoard

The Hoard is David's catalogue of everything he builds. It runs on his Mac over the library in bookwyrm-rpg. A build reaches it in two halves:

1. **This skill, in the build project:** lock the version folder with a `piece.json`, check it, and open the lock pull request.
2. **The Hoard, on the Mac:** after the merge it sees the new locked version, marks the item out of date, and imports it when David clicks Import.

The Hoard watches the bookwyrm-boxes, bookwyrm-dioramas and bookwyrm-lanterns repos. It does not watch bookwyrm-rpg, so a version locked there (the palace balcony, the Lothlorien staircase) never shows up in Catalogue → Sources on its own; tell David when you lock one there.

Never import into the library from a build project, and never ask David to run `import_piece` by hand. Call the library's `import_from_source` only when David asked, in your thread, for that exact import.

The construction skill (lithophane-lanterns, printable-container, layered-diorama, ...) still owns what goes in the version folder and when a version is ready. This skill adds the steps that make the folder publishable.

## When to use

- The construction skill reaches its lock or release step, or David approves a version for printing or as a preview.
- At the end of any session that changed a project's meshes, sizes or interfaces without locking. Say so in one line, such as "Dragon Mountain has unlocked changes since v2. Lock them as v2.1?", and lock only if David says yes.

## 1. Pick the version

Use the repo's own numbering. Read the existing version folders of this project and of sibling projects first.

- bookwyrm-lanterns: `lanterns/<slug>/v<N>/` or `v<N>.<M>/`, with `version` `v<N>`.
- bookwyrm-boxes: `projects/<slug>/release-v<N.M>/`, with `version` `v<N.M>`. Unprinted digital previews are `v0.x`.
- Another repo: follow its README, its `hoard.json` `new_projects` folder, and its existing folders.

A change to any mesh, size, clearance, pocket or assembly position is a new version. A documentation fix is not, and neither is adding a `piece.json` to a folder locked before the convention. A locked folder is never edited after that.

Versions compare as numbers (`v1.10` is newer than `v1.9`), never as folder names.

## 2. Write piece.json

Put it at the root of the version folder, beside the README. The full rules are in bookwyrm-rpg `services/library/docs/piece-json.md`. In short:

```json
{
  "piece_json": 1,
  "slug": "dragon-mountain",
  "version": "v2",
  "title": "Dragon Mountain lantern",
  "kind": "lamp",
  "status": "digitally-validated",
  "rights": {"design": "ai-assisted", "ip": "none", "licence": "all-rights-reserved"},
  "description": "One or two sentences a buyer would read.",
  "themes": ["dragons"],
  "tags": ["lantern", "led"],
  "size_mm": {"x": 172, "y": 145, "z": 238},
  "components": [{"name": "Plinth", "file": "print/dragon-mountain-v2_plinth.3mf"}]
}
```

- **slug:** one per product across every repo, kebab case, never reused. Earlier versions of the same product keep the same slug. For a new product, check that the slug is unused in this repo and in The Hoard (ask David if you can't check The Hoard).
- **kind:** diorama, figurine, lamp, ornament, terrain, prop or container.
- **status:** the highest claim the evidence supports: `concept`, `digitally-validated`, `prototype` (printed), `interface-fit-tested`, `qualified`. A render or a slice is never more than `digitally-validated`.
- **rights:** `design` is `original` or `ai-assisted`. `ip` is the third-party world in kebab case (`middle-earth`, `zelda`) or `none`. Any `ip` other than `none` must have `licence` `personal-use-only`. Original designs default to `all-rights-reserved`.
- **components:** every print file in the folder (`.stl`, `.3mf`, `.step`, slicer files) must be named by one component, with only the fields `name`, `file`, `part_id`, `quantity` (how many to print; never `count`), `printer` and `material`. A version that holds only its changed parts names each unchanged part in its earlier folder as `../<version>/<path>`.
- **uses:** shared pieces (a hardware plate, a controller) pinned as `{piece, revision}`, only when the library already has that revision.

## 3. Make sure the repo has hoard.json

The Hoard reads `hoard.json` at the repo root to find projects and to offer the repo to new ideas. If it is missing, add it in the same pull request:

```json
{
  "hoard_json": 1,
  "family": {
    "name": "Lithophane lanterns",
    "builds": "LED lithophane lanterns with lit image panels",
    "skill": {"path": "SKILL.md"},
    "kinds": ["lamp"]
  },
  "projects": ["lanterns/*"],
  "new_projects": "lanterns/<slug>/"
}
```

`projects` are folder globs, one folder per product. `ignore` lists folders that are not products (shared parts, guides). A family with no products yet lists `"projects": []` with `new_projects`. `new_projects` is where a new product goes; leave it out for a single-product repo. `family.skill` is the construction skill's path, with `repo` (`owner/name`) when it lives in another repo. `releases: true` marks a repo that ships its files as GitHub release zips.

## 4. Check

Run the repo's checker from the repo root and fix every line it prints:

```sh
python tools/check_piece_json.py <projects folder>/
```

It checks `piece.json` and `hoard.json` together. Use `--metadata-only` only in a repo whose print files are not in git. If the repo's `tools/check_piece_json.py` doesn't know `hoard.json`, copy the current one from bookwyrm-rpg `services/library/tools/`.

## 5. Open the lock pull request

Commit on a branch and open a pull request. Never push to main. Large meshes go in Git LFS, except in a repo that keeps meshes out of git (bookwyrm-dioramas). There, commit `print/SHA256SUMS` (`shasum -a 256 print/*.stl > print/SHA256SUMS`, run in the version folder) and copy the locked set on the Mac to `~/bookwyrm/dungeons-and-dragons/sources/files/<owner>/<name>/<version folder>/` at the same paths; The Hoard imports the files from there and checks each hash. A cloud container can't reach lfs.github.com, so when meshes need uploading, give David the exact command block to run from his Mac clone. The construction skill says which files belong in the folder.

## 6. After the merge

Tell David in one line that the version is merged and The Hoard will show it as ready to import, for example "Dragon Mountain v2.1 is merged. Import it from Catalogue → Sources in The Hoard." Stop there. The import, the R2 backup and the item's images happen in The Hoard. The item's card shows "v2.1 locked" until it is imported.
