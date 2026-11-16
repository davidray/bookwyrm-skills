# Lighting and electronics

Read this before designing LED scenes, a controller, a circuit board, or a lit space in any family. Each family keeps its own standard hardware: the lanterns' [standard lighting architectures](../../families/lithophane-lanterns/references/standard-lighting-architectures.md) (split lighting with the XIAO ESP32-S3 controller, the WS2812B strip and the hardware plate; lit shell; tea light), and the boxes' energy-safety rules in [engineering and validation](../../families/printable-container/references/engineering-and-validation.md). Lessons here come from the Shire case controller Ashmaw, the case controller B board (bookwyrm-boxes `shared/electronics/case-controller-b/`), the lanterns, and the Dale diorama's LED tests.

## Test lighting as hardware, access and optics

- Establish the selected hardware and its measured dimensions before cutting production pockets. Keep unverified controller and connector envelopes labelled as reserves, and tell uncut route guides apart from real openings.
- Design installation and removal for the wired part: board orientation, solder pads, leads, connectors, bend space, slack, retention and the service cover. A nominal bare-board path or wire centreline does not prove the soldered assembly can be installed. Keep cavities and routes reachable in the intended assembly order.
- Fit purchased lights, batteries and switches with generous clearance, so a slightly different part from another pack still fits.
- Check source visibility and light delivery separately. Hiding an LED behind a bend can conceal it while starving the target. A rendered glow, a clear bore or a blocked sightline does not prove brightness or diffusion.
- Before repeating a holder or committing a large lit part, test short and long or bent light paths with the actual LED, the intended interior colour and removable diffuser samples. Hold drive settings and ambient light constant and change one variable at a time. If delivery is poor, move the emitter or add a light guide rather than turning up the brightness.
- Keep new fit and optics results pending until they are measured or reported.

## LED scenes (WLED)

- The box must run on its own, so final scenes are WLED presets saved on the device, not streamed (DDP) from a computer.
- Map the LEDs onto the lithophane art before designing scenes. Film the box stepping through each LED and calibrate positions from the video. On the Shire, the old "window" LEDs were not behind the windows.
- Keep presets to about 17 segments. A 21-segment named version ran the controller out of memory.
- A long transition from a 1-segment preset into a multi-segment one makes the new segments fade up from black, which looks like everything turned off. Use a short fade (2 s) there.
- An always-connected client such as Home Assistant's WLED integration can drain the controller's memory and make it reboot every few minutes. Keep it disabled.
- Saving a playlist needs `"o":true`; for scenes, apply the state, check the segments, then save the current state.
- Put the presets file, hardware and button settings (without network credentials), the LED map and the scene generator in the release, with restore steps.
- Set a current limit in WLED (the lanterns' reference is 850 mA) and let the limit, not the pixel count, bound the load. Re-check current, voltage drop, wiring, connector capacity, battery runtime and heat before raising it.

## Circuit boards

- Read the main chips' datasheets for pinout and features before release, and record what you checked. The IP5306-I2C has no battery voltage readout, so the board needs a divider to measure the battery.
- Check every BOM part is in stock at the assembler before ordering, offer substitutes for any that aren't, and record the as-ordered substitutions in the release (J6 became C53055319).
- A board release is frozen like any product release. The next change is r2 in its own release folder; quote r2, not r1, for a larger order.
- Route user forces (buttons, USB plugs) into the printed structure, not the board.
