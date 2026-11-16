# Lighting and electronics

Read this before designing LED scenes, a controller, or a circuit board for a box. Safety rules for energy sources stay in [engineering and validation](engineering-and-validation.md). Lessons come from the Shire case controller Ashmaw and the case controller B board (`shared/electronics/case-controller-b/`).

## LED scenes (WLED)

- The box must run on its own, so final scenes are WLED presets saved on the device, not streamed (DDP) from a computer.
- Map the LEDs onto the lithophane art before designing scenes. Film the box stepping through each LED and calibrate positions from the video. On the Shire, the old "window" LEDs were not behind the windows.
- Keep presets to about 17 segments. A 21-segment named version ran the controller out of memory.
- A long transition from a 1-segment preset into a multi-segment one makes the new segments fade up from black, which looks like everything turned off. Use a short fade (2 s) there.
- An always-connected client such as Home Assistant's WLED integration can drain the controller's memory and make it reboot every few minutes. Keep it disabled.
- Saving a playlist needs `"o":true`; for scenes, apply the state, check the segments, then save the current state.
- Put the presets file, hardware and button settings (without network credentials), the LED map and the scene generator in the release, with restore steps.

## Circuit boards

- Read the main chips' datasheets for pinout and features before release, and record what you checked. The IP5306-I2C has no battery voltage readout, so the board needs a divider to measure the battery.
- Check every BOM part is in stock at the assembler before ordering, offer substitutes for any that aren't, and record the as-ordered substitutions in the release (J6 became C53055319).
- A board release is frozen like a box release. The next change is r2 in its own release folder; quote r2, not r1, for a larger order.
- Route user forces (buttons, USB plugs) into the printed structure, not the board.
