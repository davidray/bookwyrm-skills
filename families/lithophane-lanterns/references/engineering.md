# Lantern engineering

## Hardware and service

Model the measured light source as an envelope plus access requirements, not as a guessed primitive. Include the controlling diameter or width, height, flame-tip or lens height, switch location and travel, battery door, charging connector, cable bend, finger access, and removal direction as applicable.

Use low-voltage LEDs only. Keep open flame outside this workflow. Treat heat, battery safety, electrical compliance, and material temperature limits as separate requirements when consequential; ordinary visual and mesh checks do not qualify them.

Prefer a service route that does not require disturbing fragile lithophanes. The light should be positively located and remain removable. Verify access in the assembled state, including inversion and handling if those are expected.

## Panel architecture

Specify for each face:

- visible image field;
- finished panel outer dimensions;
- minimum and maximum thickness targets;
- frame overlap and light-blocking border;
- channel or pocket dimensions and clearance;
- bottom support and positive retention;
- insertion/removal path and required external clearance;
- face identity and correct image orientation.

Use a representative channel coupon before locking all faces. Long panels need allowance for printer variation, elephant foot, edge roughness, and warping. Do not choose a clearance solely from a generic tolerance table when a quick physical coupon is possible.

Common service patterns include roof-captured vertical panels, removable frames, side-loading channels, or separately fastened panels. Choose by actual assembly and replacement needs.

**Series default for Dave's square lanterns:** flat 3.2 mm panel plates drop into 3.8 mm slots from the top, rest on the slot floor, and are captured by the roof (0.2 mm above the panel). The relief faces the LEDs and the flat back faces out, so the image is mirrored in the relief. Service order: lift the roof, lift the panel. All three split-lit lanterns use this.

A removable roof needs positive location by default: locating pegs into the body (Bag End: four 6 × 5 mm pegs in 6.6 × 6.5 mm holes) or a keyed lip. Gravity-only seating needs the user's explicit acceptance. A decorative roof may sit over the body like a lid, with a pocket the body top nests into, as long as it still lifts straight off. The pegs locate the roof; the lid tie-down below holds the stack together.

The body needs the same on the base: every stacked joint is positively located, never gravity-only. When the body has an open bay at the bottom, use locator tabs on the base deck that stand just inside the bay's walls, one at the middle of each side. Keep them clear of the divider blades and below the panel grooves. Give them the proven 0.3 mm per-side clearance and a 1 mm lead-in chamfer on the outer top edge. (Lonely Mountain: the first print had nothing locating the body on the base, and David flagged it. Print v2 adds four tabs, each 30 × 3.5 × 4 mm with the outer face 0.3 mm inside the 132 mm bay; the fit is not yet printed. The same tab also prints loose, to glue onto a base that is already printed.) Check every base-to-body and body-to-roof joint for location at blockout, together with the roof.

## Lid tie-down (series standard)

Every one of Dave's lanterns has a central tie-down (David, 2026-11-06). An M4 eye bolt in the lid and a wire to the base clamp lid, body and base together, so the lantern can be carried as one piece and still comes apart for service. This standard does not replace the roof pegs or keyed lip. It is not a hanging point, and the eye stays inside.

The tie runs straight down the lantern's vertical axis:

```text
  lid ── M4 heat-set insert in a boss, eye bolt screwed up into it (eye down)
   │      wire loop crimped through the eye
   │   wire down the hollow divider / LED post bore (beside the LED harness)
   │   through the deck wire hole, straight across the base bay
  plate ─ anchor cup: lower eye bolt sits in a keyed funnel,
          its shank passes a 4.5 mm hole; washer + M4 lock nut underneath
```

**Lid (top) fitting.**
- Put an M4 brass heat-set insert in a boss on the lid underside, on the axis. For split lighting that is the ceiling of the roof's post socket; for a lit shell it is above the LED post.
- Starting dimensions are for a standard M4 × 8.1 mm insert: a 5.6 mm hole, 9.5 mm deep, in a boss of at least 12 mm OD. Leave at least 3 mm of solid above the hole so the exterior isn't marked. Tie the boss into the lid structure with ribs or a fillet, not just a thin skin. Measure the purchased insert and use its maker's hole size.
- Press the insert in from below after printing. The load pulls the insert toward its entry face, so give it full depth and a solid boss.
- Keep the boss inside the post bore's footprint (12 mm OD in a 14 mm bore) so it may hang down into the bore.
- When the boss is out of the soldering iron's reach (deep inside a one-piece shell), a side-loaded hex pocket trapping an M4 nut is an accepted equivalent.

**Tie assembly.**
- Use two identical M4 eye bolts with an eye OD of 10 mm or less and a 16–20 mm shank, joined by 1.0–1.5 mm 7×7 stainless wire rope, nylon-coated where it can be had so it doesn't chafe the LED wires. Crimp a loop through each eye with an aluminium ferrule.
- The lower eye bolt, its loop and its ferrule must drop through the post bore and the deck hole beside the LED harness. Keep a free 10 mm passage there.
- Set the wire length between eyes from the stack. With the lid seated and the lower eye sitting in its funnel, the nut should engage at about the middle of the take-up range. Record the length and the take-up in the lantern's facts.

**Wire path.** The wire stays inside the post bore and on the axis through the bay. It never enters an optical chamber, never crosses a strip, panel or slot, and never runs outside the divider. In lantern blockouts, model it as a named reserve (`R_tie_axis`): a 24 mm diameter column from the plate to the deck hole, plus the bore. Hardware layouts must keep this column clear.

**Base (bottom) fitting.**
- The anchor is a standard feature of every hardware plate, the blank included, because the plate is the base floor. It is an inverted cup rising into the bay on the axis.
- Inside the cup, a 14 mm bore leaves room for a 7 mm nut driver. The cup is deep enough that the bolt shank never passes the plate's bottom face at full take-up, so the lantern still sits flat. The cup wall is 2.4 mm, with radial ribs to the plate.
- At the top of the cup is a 4 mm cap with a 4.5 mm M4 clearance hole. Above it, a lead-in funnel (about 20 mm down to 4.5 mm) guides the hanging bolt into the hole, and a 5 mm cross slot keys the eye so it can't turn while the nut is tightened.
- The washer (an M4 × 12 mm fender washer spreads the load on PLA) and an M4 nylon-insert lock nut go on from underneath.
- Fix the plate with M3 heat-set inserts rather than self-tapped pilots once it carries the tie.
- If a lantern's floor is base structure rather than the plate, put the same cup in that structure instead.
- Record the anchor in `hardware-interface.json`:

```json
"tie": {"xy": [0, 0], "hole_d": 4.5, "cup_id": 14, "cup_depth": 0, "keepout_d": 24}
```

**Load path.** The lid must bear on the body's seat and the body on the base. Tension must not reach the panels (keep the 0.2 mm over the panel) or the divider. Leave at least 0.5 mm of vertical clearance at one divider seat so the post can't become the column. Check that the lid around the boss is stiff enough for a central pull.

**Tension.** Make it snug by hand with a 7 mm nut driver, plus a quarter turn. That is enough to keep the stack from separating when the lantern is lifted by its base. Don't crank it: PLA creeps, so recheck the nut after a few days.

**Assembly and service.**
- To assemble:
  1. Screw the upper eye bolt into the lid insert.
  2. Hold the lid above the body and lower the free eye bolt and wire down the post bore. The bolt hangs shank-down and drops through the deck hole into the funnel.
  3. Seat the lid.
  4. From underneath, fit the washer and nut, then tighten.
- To take it apart: remove the nut from underneath and lift the lid off. The tie comes out with it.
- Remove the nut before you unscrew the plate.

**Evidence.** This is a new interface type, so it needs one small coupon before release claims: a lid-boss block with the insert, pulled by hand with the eye bolt, and a plate cup with the funnel and the slot, checked for nut-driver access and for the hanging bolt finding its hole.

## Service face, door, and switch

Put the hardware plate's port window behind a service face. A decorative door can cover it (Bag End: a 38 mm green door held by four 6 × 3 mm magnets, with a full-window clearance pocket in its back). When the user wants a power switch, an SS12D00-type slide switch on the battery positive line before the charger/boost board, operated through a slot behind the door, is the recorded pattern. Without a switch request, keep a switch reserve at the service face.

## Light path

Reserve the full optical volume early. Consider source-to-panel distance, source height, central obstructions, interior reflectance, diffuser placement, venting, and light leakage at seams. A tall central tower can create dark bands; a close point-like tea light can create hotspots. A diffuser can help but also costs brightness and space.

Evaluate all faces, not only the hero view. A four-panel lantern needs reasonably balanced illumination around the full perimeter. Use physical coupons for critical optical decisions because slicer walls, pigment, layer direction, and the actual LED dominate the result.

## Structure and segmentation

Decide which parts are intended to be single connected solids and which are deliberate assemblies. Check load paths and joints after Boolean operations and export. Visual overlap is not union; one object can still contain disconnected components.

Choose segmentation from build volume, support burden, panel installation, service, painting, and repair. Ensure the assembly order is possible without trapping panels, hardware, or fasteners. Keep fragile optical panels separate from high-support structural prints where practical.

## Scaling

Scale the architecture selectively. Keep real hardware, required clearances, printable wall/relief features, and usable access at viable absolute dimensions. Recompose the exterior around them. When a larger light replaces a smaller one, expect footprint, base, and proportion changes; do not hide the change behind a uniform scale or stale visual approval.

Faithful decor parts often grow the lantern (wider plinth to carry the body, taller roof, canopy wider than the walls). That is acceptable when the art needs it. Re-check the build envelope for every part and say how the overall size changed.

Supports: decks that bridge a base bay print upright with tree supports inside the bay only, removed through the open bottom. Keep supports out of hollow lit interiors.

## Finish

For single-color hand-painted frames, design crisp paint boundaries and brush access. Avoid using material color in renders to claim detail that is absent from the exported surface. Lithophane panels remain an optical/material system even when the frame is hand-painted.
