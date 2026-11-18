# Design rules from the travel cases

Twenty rules learned on the Shire Travel Case and its interior (2026-10) and the decorated Shire and Mirkwood cases (2026-11). They came from boxes but hold for any build. The central lesson: progress was fastest when every uncertainty was named and answered with the smallest useful physical test, not with full-size geometry.

The numbers those cases settled (magnets, Gridfinity, pane, case, connectors, fonts) are in [box family standards](../../families/printable-container/references/box-family-standards.md) (`families/printable-container/references/box-family-standards.md`). Reuse the method, not blindly the numbers.

## Before modeling

1. **Measure the real thing before finalising a precision interface.** Photos give a roomy blockout; calipers set the fit. The dice foam measured 107 × 74 × 20 mm, which the photo estimate had missed.
2. **Classify every visible object** as required content, optional content, packaging, scale reference or excluded. A gauge was once designed for a cardboard box that was only packaging.
3. **Draw every use state:** closed, open, removed, inverted, loaded, serviced, carried, stored, with which face is up and where hands go. An early lid misread which face became the dice tray.
4. **Name both endpoints of every critical dimension** and its coordinate system. The 11.84 mm connector spacing was between mounting faces, not outer faces; two 3 mm plates turned that into a 6 mm error.
5. **Check concept proportions against the real envelope.** Mirkwood concept r2 showed the box at half its height; render a neutral guide of the real envelope and draw the concept on it.
6. **Choose a method that can reach the target look** before iterating. Six scripted Mirkwood blockouts never looked carved (an AI audit scored one 85/100); one generated relief wrapped on the shell matched the concept. Judge by a render beside the concept, not by audit scores.

## Structure

7. **Reserve swept volumes for wires, connectors, tools and hands**, including bend radius, insertion path and strain relief. A collision-free seam still pinched a real three-wire lead.
8. **Carry loads through broad bearing surfaces** and route user forces (plugging, lifting, carrying) into replaceable structural parts, never into boards, lenses or stored objects. Magnet pockets retain; they are not feet. A panel-mount USB-C extension kept plugging force off the board.
9. **Separate stable structure from wear parts, inserts, electronics and decoration**, so later changes stay local, and reserve expansion space on purpose.

## Testing

10. **Answer expensive questions with small coupons**, one variable at a time, with pass/fail criteria set before printing. Magnet-pocket arrays and connector-holder sets locked high-value interfaces cheaply.
11. **Record print conditions with every physical result:** printer, nozzle, material, layer height, walls, infill, supports, orientation. Wrong infill once invalidated a lithophane thickness result.
12. **Store a passed interface with its application and limits.** A 5 × 2 mm magnet pocket behind a 0.8 mm roof holding a miniature's washer does not qualify a lid magnet in a side wall.

## Decoration

13. **Frames, bands and beads wrap corners; relief never fills an edge round.** Check corners and rounds as their own pass along every side.
14. **Protruding ornament is chunky and fused, or a separate glued part.** Generate the organic form, then enforce strength rules on it; hand-built replacements read as dough.
15. **Mating features are exact solids added after any smoothing.** A remesh rounded the Shire foot pegs and they failed the fit test.
16. **Lithophanes come from flat, bright, proportion-checked images**, tested as a crop first (see [lithophanes](../lithophanes/lithophanes.md), `shared/lithophanes/lithophanes.md`).

## Inherited parts and release

17. **Check every inherited file's orientation in an assembled render, and write the stack-up for every interface that spans two parts.** The V2.1 outer lid STL is stored face down and put magnet pockets on top; the V2.1 tray sat the connector holder 2.92 mm low.
18. **Make the assembly picture before the full print:** layer plan, exploded view, section, numbered steps, up and front markers, magnet polarity. If it can't be explained on one page, the design or the guide isn't finished.
19. **Ship one numbered print folder with every part**, orientation and quantity in each file name, never just the changed parts.
20. **Freeze an approved version; geometry changes start a new draft**, and claim only what the evidence shows (see [evidence and claims](../evidence-and-claims/evidence-and-claims.md), `shared/evidence-and-claims/evidence-and-claims.md`).
