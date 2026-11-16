# Dave's print profile

Use this profile for every one of Dave's builds (lanterns, boxes, dioramas) unless a family standard or a project explicitly overrides it. Family standards, such as the box family's in `families/printable-container/references/box-family-standards.md`, add defaults for their own kind of product on top of it. Treat it as a persistent equipment/material preference, not as proof that a particular part fits, slices, prints, or performs optically.

## User-supplied fleet

| Printer | Intended nozzle | Official build volume | Design note |
| --- | ---: | ---: | --- |
| Bambu Lab A2L | 0.6 mm | 330 × 320 × 325 mm | Largest bed; the 0.6 mm nozzle governs conservative shared exterior feature sizing. Usable footprint in Bambu Studio is about 290 × 290 mm (see below). |
| Bambu Lab A1 | 0.4 mm | 256 × 256 × 256 mm | Smallest ordinary single-nozzle build envelope in the fleet. |
| Bambu Lab X2D | 0.4 mm | 256 × 256 × 260 mm using the main/left nozzle | When both nozzles or the auxiliary/right nozzle are required, use the smaller applicable official print area instead of the main-nozzle envelope. |

**Taller builds.** David's printer handles builds taller than 256 mm (H2D-class; the Christmas village church is 263 mm). Don't cap a part's height at 256 mm; ask which printer it is for when a part needs the extra height.

**Usable A2L footprint.** On 2026-11-06, Bambu Studio 02.09.01.70 accepted a 290 × 290 mm box on the A2L but refused 300 × 300 mm and a 317 × 159 mm half, with or without a brim. Design A2L parts to fit 290 × 290 mm until a larger size is shown to slice. Plan any split at blockout.

The X2D official areas recorded on 2026-11-02 are:

- main/left nozzle: 256 × 256 × 260 mm;
- auxiliary/right nozzle: 235.5 × 256 × 256 mm;
- two-nozzle intersection: 235.5 × 256 × 256 mm.

Laser cutting: flat structural lantern parts are cut from acrylic by default (see the lanterns family's [engineering](../../families/lithophane-lanterns/references/engineering.md#laser-cut-acrylic-parts-series-standard)). Cutter not yet named; assume a 12 × 12 in (305 × 305 mm) bed.

## Material and finish preference

- Default opaque exterior material: Bambu Matte PLA, White.
- Default exterior finish intent: single-color white print prepared for hand painting unless the project says otherwise.
- Do not automatically use Matte PLA for lithophane panels. Panel material, color, thickness range, nozzle, layer height, orientation, and light spacing remain optical decisions requiring explicit project selection and a lit test strip.

## Proven lithophane and fit settings

These were printed and verified on earlier projects (davidray/shire-travel-case and davidray/the-gift-story-lanterns). Reuse them as defaults; do not propose new coupons for these interfaces. Only a new interface type, a new material, or a different light distance needs a fresh test.

| Setting | Proven value | Source |
| --- | --- | --- |
| Lithophane relief | 0.8 mm bright to 2.0 mm dark; 2.4 mm and thicker read too dark | Shire travel case |
| Lithophane print | White PLA (not Matte), 100% infill, 0.10 mm layers, flat with the back down; 0.4 mm nozzle on the A1 or X2D | Shire travel case, gift lanterns |
| Flat border or rails | 3.2 mm thick | Gift lanterns |
| Lithophane facing | Textured (relief) side outside toward the viewer, flat side toward the light | Christmas village mini print, David, 2026-11-14 |
| Pane seat | 0.3 mm clearance per side, 0.2 mm above the pane (3.8 mm slot for a 3.2 mm panel) | Shire cassette, in service |
| Free sliding fit | 0.5 mm per side | Shire cassette |
| Tongue and groove | 0.30 mm lateral per side, 0.20 mm vertical relief | Shire seam test r3 |
| Three-wire exit | 10 × 3.6 mm | Shire tray |
| LED-to-lithophane distance | 15–25 mm proven; about 54–61 mm used in the user's working lanterns | Shire; user, 2026-11-05 |

## Exterior process preset (provisional, not yet proven)

The profile has no proven exterior settings yet. Until the user supplies theirs, slice structure parts with Bambu's stock "0.30mm Standard @BBL A2L 0.6" process, Bambu Matte PLA, and tree supports, and say in the release that slice times, supports, and filament use come from this stock preset. For A1 or X2D parts, use the matching stock 0.4 mm process: A2L presets don't load on them. Where tree supports leave overhangs uncovered (window heads, bay ceilings), switch that part to normal supports and check the projection again. Replace this section with the user's own settings (layer height, walls, infill, support style) when known.

Two-colour prints (an opaque body with integrated white lithophane) use the X2D with both nozzles and its 235.5 × 256 × 256 mm two-nozzle area. The opaque colour is ordinary PLA, not Matte.

## Cross-fleet engineering rules

- When a part must print unchanged on all three machines with one nozzle, use the A1's 256 × 256 × 256 mm volume as the maximum common nominal envelope and leave practical slicer/bed margin rather than designing exactly to the limit.
- When an X2D job requires both nozzles, constrain the applicable part/plate to 235.5 × 256 × 256 mm unless current official documentation or a verified slicer profile shows otherwise.
- For exterior parts shared across the fleet, size freestanding details, relief, slots, joints, wall transitions, and support-removal access conservatively for the 0.6 mm A2L nozzle. Do not assume that geometry proven only with a 0.4 mm nozzle will survive the 0.6 mm profile.
- A 0.4 mm detail or lithophane variant may be supplied separately for the A1 or X2D, but keep it distinct from the 0.6 mm-compatible shared exterior set and validate it independently.
- Beyond the proven settings above, unknown layer height, line width, shrink/fit compensation, seam behavior, overhang performance, paint allowance, and slicer settings remain project inputs. Retire them with representative coupons instead of inventing universal tolerances.
- Freestanding decorative detail such as open dragon wings has printed without difficulty for the user. Do not thicken, fold, or anchor it on assumption; change it only if a slice or print fails.
- A whole product (lantern, case, diorama) may exceed the common build envelope only through an explicit segmentation and assembly plan; never uniformly scale protected panel, lighting, or service geometry merely to fit a bed.

## Scope boundary

This profile stores printers, nozzles, material preference, proven print and fit settings, and cross-fleet implications only. Project-specific visual approvals, dimensions, proportions, hardware, light sources, panel art, mechanisms, and compromises stay in each project's checkpoint and must not become defaults for other projects. Family-wide defaults belong in that family's standards.

## Official sources checked 2026-11-02

- Bambu Lab A2L announcement/specification: https://blog.bambulab.com/bambu-lab-a2l-creative-playground-extra-large/
- Bambu Lab A1 Quick Start Guide: https://cdn1.bambulab.com/documentation/quick-start-a75adcb1d5d5e/Quick%20Start%20Guide%20for%20A1.pdf
- Bambu Lab X2D announcement/specification: https://blog.bambulab.com/xcellence-made-simple-bambu-lab-presents-the-x2d/

Recheck current official specifications before relying on them for a new release, especially X2D multi-nozzle print areas and supported slicer behavior.
