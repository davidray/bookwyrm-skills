# Standard lighting architectures

Use these names consistently in Dave's lantern projects. Record the selected architecture in the project checkpoint before functional blockout.

## Split lighting

Selecting **split lighting** imports the following system together. Do not substitute a generic PCB, battery, divider, or LED layout while continuing to call the result split lighting. Record any explicit exception as a project-specific departure.

### Controller and power baseline

- Controller PCB proposal: 88 × 50 × 1.6 mm with 3 mm corner radius.
- Minimum board cavity: 94 × 56 × 25 mm.
- Wired controller envelope: 94 × 85 × 25 mm, excluding the separate antenna.
- Preserve a 20 mm straight USB plug approach at the service edge and 15 mm beyond the harness edge for connector bodies and wire bends.
- Four 3.2 mm mounting holes, top view from the PCB lower-left origin: `(44,4)`, `(84,4)`, `(4,46)`, `(84,46)` mm. The pattern is asymmetric; do not mirror it. Use nonconductive 3 mm standoffs.
- Controller: Seeed Studio XIAO ESP32-S3.
- LED data path: XIAO D1 / GPIO2 through an SN74AHCT125N 5 V level shifter to the `+5 V / DATA / GND` light connector.
- Retained charger/5 V boost daughterboard M1: 34.39 × 25.53 × 5 mm actual, with a 36.4 × 27.5 mm plan reservation.
- Battery: protected 3.7 V single cell, 40 × 65 × 12 mm actual. Reserve a provisional 42 × 67 × 14 mm removable, non-compressive pocket with strain relief and an extraction path.
- XIAO battery pads remain unused. Add the required Schottky isolation diode between external `+5V_SYS` and the XIAO 5V/VBUS input before fabrication.
- The retained M1 architecture has physically operated the lights while USB-C charging in another lantern. Repeat staged powered and thermal testing in each final enclosure.
- External adhesive antenna: 38 × 19 × 3 mm; reserve at least 40 × 21 × 4 mm on a flat nonmetallic surface. Use a gentle, serviceable U.FL lead route and keep the antenna away from the battery, M1, large metal parts, and ground planes where practical.

### Divider and light baseline

- Use an opaque, removable divider built as a hollow central post with four radial light-blocking blades. Together, the post and blades create four face-oriented optical chambers, one per lithophane.
- Orient the divider so each of the central post's four flat faces points toward the center of one lithophane. Each lithophane sits between two adjacent radial blades; the blades form the chamber sidewalls and prevent light intended for one lithophane from spilling directly behind its neighbors.
- Run each blade outward toward the opaque corner/frame line between adjacent lithophanes. Its outer edge must meet or overlap the lantern's light-blocking frame region rather than terminate in the illuminated image field.
- Run the divider continuously between keyed base and roof seats. Preserve the hollow center as a protected vertical wiring/service passage, including usable entry and exit openings.
- The divider must not block panel installation, panel removal, roof removal, or controller service.
- Provide one vertical recessed or positively located LED-strip channel on each of the four central post faces.
- Mount one vertical 12-pixel addressable-LED strip in each channel, aimed outward toward the corresponding lithophane: four strips and 48 pixels total. Keep the LEDs and channel edges clear of the two adjacent divider blades so the full lithophane field receives light.
- Daisy-chain `DIN→DOUT` around the post across the four strips as one 48-pixel serial data chain connected to the controller's single light output. In this definition, “wired in serial” refers to the addressable data order; preserve a correctly sized, serviceable 5 V/GND distribution path rather than placing the strip power rails electrically in series.
- Reference firmware/load configuration: WLED with an 850 mA current limit. Re-check current, voltage drop, wiring, connector capacity, battery runtime, and heat before increasing the count or limit.

### Physical divider reference

These user-supplied photos define the intended spatial relationship. Treat them as form and assembly evidence, not dimensioned drawings.

![Divider installed among four lithophanes](images/split-lighting-divider-installed.jpg)

The installed view shows one lithophane facing each central post face. Adjacent radial blades extend toward the opaque corner/frame regions and separate the four optical chambers.

![Isolated split-lighting divider](images/split-lighting-divider-isolated.jpg)

The isolated view shows the hollow central wire passage, four vertical strip channels on the post, and the radial baffle blades. Preserve this topology when adapting the divider height and span to a new lantern.

### Variables that remain lantern-specific

The name locks the system topology and established hardware envelopes, but not every geometric or optical dimension. Determine and verify for each lantern:

- divider height, blade span and thickness, central-post section, strip-channel fit, interlock, and base/roof key geometry;
- perimeter light sealing, reflectivity, diffuser use, and seam leakage;
- LED pitch and strip length if the purchased strip differs from the established 12-pixel segment;
- LED-to-lithophane spacing, panel thickness range, color balance, and hotspot control;
- final harness lengths, power injection, connector selections, wire gauge, and service routing;
- enclosure fit, antenna performance, powered temperature, and runtime.

Use a divider/key/light-seal coupon, one representative chamber optical coupon, and a controller-carrier fit check before release claims.

## Puck light

**Puck light** is a separate standard architecture name. Use the actual selected low-voltage puck's measured envelope, switch, charging or battery access, removal path, and optical spacing. Do not import the split-lighting PCB, battery, X divider, or strip topology unless the user explicitly requests a hybrid. Add a locked puck baseline here only after the user approves a specific reusable setup.

## Tea light

**Tea light** is a separate standard architecture name for an LED tea light only; open flame remains excluded. Use the actual light's measured diameter, height, flame/lens envelope, switch access, battery door, and removal path. Do not import the split-lighting PCB, battery, X divider, or strip topology unless the user explicitly requests a hybrid. Add a locked tea-light baseline here only after the user approves a specific reusable setup.
