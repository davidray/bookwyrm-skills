---
name: campaign-packet
description: Design a D&D campaign with David in a campaign build's chat (story, places, characters, enemies, encounters, props) and assemble its packet - miniatures through Builder, props as their own builds, paper printables in the campaign's draft, and a custom campaign box sized to hold everything. Use for a campaign build (slug campaign--<name>, kind campaign); do not use to build a single prop, miniature or box, which have their own builds and skills.
---

# Campaign packet

Paths such as `shared/...` and `families/...` are from the root of the bookwyrm-skills repo (`~/code/bookwyrm-skills` on David's Mac).

A campaign build turns a pitch into a game David can run: the campaign itself, and a box he puts on the table holding everything it needs. It is a build like any other (`workshop`): a build record with a brief, a checkpoint, a stage, a budget and gates. What is different is that most of what it makes is made elsewhere. The campaign build designs, decides what goes in the packet, and keeps track; miniatures, props and the box are each made by the pipeline that already makes them.

## 1. The record

- Create the build record with `kind="campaign"` and the chat's slug (`campaign--<name>`). The brief is David's pitch in his words, then what is settled and what is still open.
- The **packet** lives on the record (`write_build(packet=[...])`, written whole every time). The Hoard shows it in the build's Packet pane, so keep it current: add an item as soon as it is agreed, and move its `status` from `idea` to `designing` (its build or Builder request is under way), `ready` (files to print exist) and `printed` (David says so).
- Each item: a stable `id`; `section` (`miniature`, `prop`, `paper` or `box`); a short `name`; `quantity`; `size_mm` [width, depth, height] of its outside, once known (the box is sized from these); and what it points at: `creature` for a miniature, `build` for a prop or the box, `files` for paper (paths in the campaign's draft). A one-line `note` is optional.
- Stages map as: `brief` (the pitch), `concept` (the campaign outline and the packet list), `design` (writing the campaign and getting its pieces made), `print-test` (printing), `done`.

## 2. Design the campaign with David

Work it out in the chat, a few questions at a time, and write it up as you go. Ask before inventing anything David would want a say in.

1. **The frame**: players, the party's level, sessions, tone, setting, and what the table enjoys (combat, mystery, roleplay, exploration).
2. **The outline**: the hook, the central conflict and villain, three to five acts or locations, and how it can end. One page.
3. **The cast**: allies and NPCs (a line of who they are, what they want and how they sound), and the enemies by encounter, with their stat-block source (an official book by name and page, or homebrew written in full).
4. **The encounters**: each with its place, its enemies and their numbers, the terrain worth building, and the treasure.
5. **The props**: physical things the table handles or that set a scene (the cursed crown, the puzzle box, the map table). A prop earns a place when the story turns on it or the players will touch it. Keep the number small: each one is a build.

Gate 1 (`concept`) is the outline, the cast, the encounter list and the packet list with rough quantities: everything David is about to spend money and printer time on. Put it to him as a build gate as usual, with the critic's report (`shared/independent-review/independent-review.md`): brief the critic to check the outline for holes (a hook with no reason to bite, an encounter the party's level cannot survive, an NPC who appears nowhere) and the packet against the encounters (every enemy on the table has a miniature or a stand-in).

Use published names, monsters and settings only as references for David's own table; never copy a published adventure's text, maps or art into a printable.

## 3. Miniatures: through Builder

Miniatures are made exactly as the Miniatures page makes them, by Builder (the `builder` MCP server); this chat only asks for them.

- Search first (`search_miniature_variants`): reuse a print-approved creature whenever one fits, including as a stand-in for a reskinned enemy (say so in the packet note).
- For a creature that does not exist, file a model request (`create_model_request`, after `model_request_estimate`) with the creature's description, size and the encounter it is for. Builder's own reviews go to Approvals; never decide one.
- Group every miniature the campaign uses in a Builder collection named after the campaign (`write_miniature_domain`, kind collection), with its quantities. That is the campaign tray on the Miniatures page, which exports print plates for the lot.
- A miniature's `size_mm` is its base and height (a medium creature on a 25 mm base, about 40 mm tall, is `[25, 25, 40]`).

## 4. Props: each its own build

A prop is a wondrous item: it gets its own build, run by the artificer under its family's skill, with its own concept, budget and gates.

- Create it with `write_build`: its own slug (`<campaign name>-<prop>`), `parent` set to the campaign's slug, and a brief that says what the prop is, the scene it is for, what the players do with it, a size limit (it has to fit in the box), and which family fits (`families/*/family.json`).
- Add it to the packet with `build` set to that slug, and tell David to open it on the Builds board: its own chat takes it from there. Do not model a prop in the campaign chat.
- When a prop's build reaches a draft, read its size from the draft and update the packet.

## 5. Paper printables: the campaign's own draft

Everything printed on paper goes in drafts of the campaign's own piece (the build's `piece`, kind `campaign`), saved as `workshop` section 4 says, so The Hoard keeps every revision and David prints from there.

- **The campaign book** (PDF): the outline, then each act with its scenes, NPCs, encounters (stat blocks or their sources), treasure and what happens next. Letter size, readable at the table.
- **Handouts**: letters, notices, riddles and clues the players are given, one per page, styled to look like what they are.
- **Maps**: a player map without secrets and a DM map with them, for each place that needs one. Generated map art is concept art: label it and keep it out of anything published as David's own.
- **Cards**: creature cards for every miniature from Builder (`print_creature_cards`, free), and item or NPC cards for anything the players keep.
- Write the printables with a script in this chat's working folder (HTML or Markdown rendered to PDF works), and save that script in the draft's `source/` with the PDFs, so a change to the campaign makes them again.
- Each paper item in the packet has its `files` and its `size_mm` (a stack of letter pages is about `[216, 279, 1]` per 10 sheets; card decks by their box).

## 6. The campaign box: a boxes build, sized to the packet

The box is a container build in the boxes family (`families/printable-container/SKILL.md`), with `parent` set to the campaign. Start it once the packet's sizes are mostly known; until then it is a packet item with status `idea`.

- Its brief carries the **contents list** from the packet: every item, its quantity and its `size_mm`, and how it should be held (miniatures in a foam or printed tray with one slot per figure, props in fitted wells, paper flat on top or in a lid pocket, cards in a deck well, dice in a tray).
- Give it the inside room the contents need, plus clearance (`families/printable-container/references/box-family-standards.md`), and say which items must not touch (painted miniatures). If the contents will not fit one box on David's printers (`shared/print-profile/print-profile.md`), propose trays that stack inside it or two boxes; never shrink a prop to fit without asking.
- Its art comes from the campaign: the box is the campaign's cover. Ask David what the lid shows, and give the box build the campaign's approved images to work from.
- Packet changes after the box is designed (a new prop, more miniatures) go to the box's build as a message, with the new contents list.

## 7. Spend

The campaign's budget covers the paid calls this chat makes (concept images for the campaign and its handouts). Each prop and the box ask for their own budgets in their own builds, and Builder's model requests are approved in Approvals. When you give David the campaign's packet at the concept gate, add up the likely cost of the whole packet as a rough range, so he sees it before anything starts.
