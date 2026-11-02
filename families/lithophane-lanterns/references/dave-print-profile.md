# Dave's lantern print profile

Use this profile for Dave's lithophane-lantern projects unless a project explicitly overrides it. Treat it as a persistent equipment/material preference, not as proof that a particular part fits, slices, prints, or performs optically.

## User-supplied fleet

| Printer | Intended nozzle | Official build volume | Design note |
| --- | ---: | ---: | --- |
| Bambu Lab A2L | 0.6 mm | 330 × 320 × 325 mm | Largest bed; the 0.6 mm nozzle governs conservative shared exterior feature sizing. |
| Bambu Lab A1 | 0.4 mm | 256 × 256 × 256 mm | Smallest ordinary single-nozzle build envelope in the fleet. |
| Bambu Lab X2D | 0.4 mm | 256 × 256 × 260 mm using the main/left nozzle | When both nozzles or the auxiliary/right nozzle are required, use the smaller applicable official print area instead of the main-nozzle envelope. |

The X2D official areas recorded on 2026-11-02 are:

- main/left nozzle: 256 × 256 × 260 mm;
- auxiliary/right nozzle: 235.5 × 256 × 256 mm;
- two-nozzle intersection: 235.5 × 256 × 256 mm.

## Material and finish preference

- Default opaque exterior material: Bambu Matte PLA, White.
- Default exterior finish intent: single-color white print prepared for hand painting unless the project says otherwise.
- Do not automatically use Matte PLA for lithophane panels. Panel material, color, thickness range, nozzle, layer height, orientation, and light spacing remain optical decisions requiring explicit project selection and a lit test strip.

## Cross-fleet engineering rules

- When a part must print unchanged on all three machines with one nozzle, use the A1's 256 × 256 × 256 mm volume as the maximum common nominal envelope and leave practical slicer/bed margin rather than designing exactly to the limit.
- When an X2D job requires both nozzles, constrain the applicable part/plate to 235.5 × 256 × 256 mm unless current official documentation or a verified slicer profile shows otherwise.
- For exterior parts shared across the fleet, size freestanding details, relief, slots, joints, wall transitions, and support-removal access conservatively for the 0.6 mm A2L nozzle. Do not assume that geometry proven only with a 0.4 mm nozzle will survive the 0.6 mm profile.
- A 0.4 mm detail or lithophane variant may be supplied separately for the A1 or X2D, but keep it distinct from the 0.6 mm-compatible shared exterior set and validate it independently.
- Unknown layer height, line width, shrink/fit compensation, seam behavior, overhang performance, paint allowance, and slicer settings remain project inputs. Retire them with representative coupons instead of inventing universal tolerances.
- A whole lantern may exceed the common build envelope only through an explicit segmentation and assembly plan; never uniformly scale protected panel, lighting, or service geometry merely to fit a bed.

## Scope boundary

This profile stores printers, nozzles, material preference, and cross-fleet implications only. Project-specific visual approvals, dimensions, proportions, hardware, light sources, panel art, mechanisms, and compromises stay in each project's checkpoint and must not become defaults for other lanterns.

## Official sources checked 2026-11-02

- Bambu Lab A2L announcement/specification: https://blog.bambulab.com/bambu-lab-a2l-creative-playground-extra-large/
- Bambu Lab A1 Quick Start Guide: https://cdn1.bambulab.com/documentation/quick-start-a75adcb1d5d5e/Quick%20Start%20Guide%20for%20A1.pdf
- Bambu Lab X2D announcement/specification: https://blog.bambulab.com/xcellence-made-simple-bambu-lab-presents-the-x2d/

Recheck current official specifications before relying on them for a new release, especially X2D multi-nozzle print areas and supported slicer behavior.
