---
name: miniature-roster
description: Design a roster of 1 to 20 tabletop miniatures with David in a roster build's chat (a warband, an encounter's enemies, a chess set), get it approved at a gate, and record it as one Builder model batch that The Hoard tracks under the build. Use for a roster build (slug roster--<name>, kind roster) or when a campaign needs new miniatures. A single new miniature is a roster of one. Do not use for a change to an existing miniature (its Request a change or chat on the Miniatures page) or for any wondrous item.
---

# Miniature roster

A roster build designs a set of miniatures in its chat and hands them to Builder, which makes each one: concept art, a 3D model, a printable miniature. This chat writes the roster; Builder and The Hoard do everything after. It is a build like any other (`workshop`): a record with a brief, a checkpoint, a stage and gates. Builder's paid calls are approved in The Hoard, not from this chat, so the build needs no budget of its own.

## 1. The record

- Create the build record with `kind="roster"` and the chat's slug (`roster--<name>`). The brief is David's request in his words, then what is settled and what is open.
- Once the batch is recorded, set the build's `batch` to the batch's slug. The Hoard then shows the roster's progress, and every member's step that waits on David, in the build's right pane.
- Stages map as: `brief`, `concept` (the roster written and at its gate), `modelling` (the batch under way), `done` (every member finished or closed).

## 2. Write the roster with David

1. **What it is for**: the setting or campaign, what the figures are (a warband, one encounter's enemies, a chess set), how many, and the scale (print height, 25 to 60 mm; a chess set gives the king's height). Unless David gives a number, propose 6. Never fewer than 2 or more than 20.
2. **Check what exists** (`search_miniature_variants`, `list_model_requests`): say which members the library already has, and leave them out of the batch unless David wants a new variant.
3. **Each member**: a short, distinct name; a creature id (lowercase letters, digits and hyphens, usually the name); the library family it belongs to (an id from Builder's families, or none; never invent one); and its concept-art prompt.
4. **Chess sets**: one member per distinct figure: each side's king and queen, each different rook, bishop and knight, and one pawn per side that stands for all its pawns. Two identical pieces are one member. Every piece shares one art direction. The side David names first is white.

### Writing prompts that print

Every prompt is generated on its own, so repeat the shared setting and art direction in each one.

- One full-figure character, three-quarter view, crisp readable silhouette, painterly fantasy illustration, no text, no watermark, no border.
- An action pose caught mid-motion, not posing for a portrait: describe the moment (bracing for a charge, drawing back to strike, turning to face a threat), weight on one leg, torso twisted, head turned. Give each member a different action.
- Grounded and compact so it prints: every foot and paw flat on the floor in a wide, stable stance; nothing leaping, rearing or airborne; weapons and props at shoulder height or lower, held close; no thin poles held far out, floating effects, or capes, hair and tails flying free; wings folded flat against the back.
- No base: the figure stands on the bare floor ("feet flat on the floor"). Never describe a base, plinth, rock or patch of ground, not even for a chess piece: the print base is added with the print files.
- Tell members apart by shape (build, silhouette, gear, weapon, headwear, pose). The design sheet is monochrome, so colour is never the only difference.
- Concept art is input to modelling at full detail: paint finishes may show, but never softened or thickened detail.
- Under 1200 characters each.

## 3. The roster gate

Put the roster to David as a build gate (`gate_kind` `concept`), with every member's name, creature, family and prompt in the gate details, and:

- the print height and how many concept candidates each member gets (1 unless he asks for a choice; more candidates cost more);
- the cost from Builder's `model_batch_estimate`, and the ceiling you propose (at least the kick-off high end; the batch can never spend past it);
- the rights and licence the batch will carry. Start from David's studio defaults (`~/.config/bookwyrm-studio/config.yml`: `licence` and `rights`; the date is today) and show them as a decision: the rights assertion is his, so never fill it in for him.

Run the critic first, briefed with the roster as written (not your reasons): it checks each prompt against the printing rules above, that members differ by shape, and that the family ids exist.

## 4. Record the batch

After David approves the roster (and only the members, rights, licence and ceiling he approved):

- Call Builder's `create_model_batch` with the build's name as the batch slug (without `roster--`), the title, the ceiling, the rights and licence exactly as approved, and the members (`slug`, `prompt`, `creature`, `category`, `print_height_mm`, `candidates`, `title`, `families`, `chess`). It spends nothing.
- Set the build's `batch` and stage `modelling`, and tell David the roster is ready to start from the build's right pane. Starting approves the kick-offs (the concept art calls), and only he does it. Never call an approval tool for the batch.
- From there each member's concept pick, card art, reference sheet, variant and print check waits on David in The Hoard; the build's right pane lists them. When he asks how it is going, read the batch (`read_model_batch`) and answer in a few lines.

## 5. For a campaign

A campaign build that needs several new miniatures starts a roster build for them, as it starts a build for each prop: `write_build` with a `roster--<campaign name>-<group>` slug, `kind="roster"`, `parent` set to the campaign, and a brief listing the creatures, their encounters and sizes. Its members go in the campaign's packet with `creature` set.
