# Towerverse
A buildless canvas tower defence game. Open `dist/index.html` through any static web server.

## Play
Choose an unlocked planet, then Deploy. Start with $300 on Planet 1, increasing by $25 per planet ($475 on Planet 8; $525 on Planet 10), and 20 base health. Select a tower and click a highlighted dedicated build pad; kills award space dollars, shown as brief +$ rewards where enemies disappear. Click any part of a placed tower to upgrade (three marks shown in its bar) or sell for 70% of its investment. The first wave starts after 20 seconds, with 8 seconds to build after later waves clear. Once a wave has finished spawning, send the next one early even while enemies remain. Pause and 1×/2×/3× speed controls are available. Build controls and upgrades remain visible without scrolling. Escape optionally cancels placement; Space or Enter sends the next wave; P pauses. Keys 1–9 select towers 1–9, and 0 selects tower 10.

The campaign has ten themed maps with ten waves each, branching and alternating routes, leaf-only building areas, paid rubble clearance, 21 progressively introduced enemy types (seven ground units, seven vehicles and seven aircraft), with a final boss per planet. Ten functional tower types: Gun, Grenade, Mud, Laser, Flak, Flame, Arrow Brigade, Electricity Zapper, Poison and Rocket Launcher. Aircraft fly straight from their assigned entrance to the base. Electricity chains across up to three targets; poison keeps dealing damage over time; rockets hit ground or air targets with splash damage. Sound is intentionally omitted.

Earn 3 stars at full health, 2 with 10–19 health, 1 with 1–9 health. Winning unlocks the next planet. Best stars persist in this browser's local storage, with no account or cloud save. Mid-mission state is not persisted.

## Verification
`node verify.cjs` checks map routes, blocked placement, purchases, kill rewards, upgrades and selling, star thresholds, defeat, and complete wave traversal of all ten maps with ample test defences. The game renders the approved illustrated map panels and transparent tower, alien and planet sprite atlases. Enemy waypoints follow the artwork; terrain color sampling and path clearance constrain construction. Three upgrade appearances use the original level 1, 3 and 5 design progression. Human difficulty balancing remains future work.

Navigation is generated from hand-guided routes and the illustrated road surface using `python scripts/refine-navigation.py` (Pillow, NumPy, SciPy). The basic alien uses eight walk frames, normalized to a fixed foot anchor; other units use trimmed sprite frames.

First-time enemy encounters show a small dismissible introduction card. More info pauses the mission to show speed, current-wave health, reward and effective counter towers. Encountered types persist in browser storage and are introduced once.

All ten weapons use distinct muzzle and impact effects: bullets, arcing grenades, mud blobs, laser beams, flak shells and black smoke, flame jets, arrows, chain lightning, poison globules and propelled rockets. Travelling ammunition applies damage on arrival. Ground enemies are occluded by the Figure Eight bridge; aircraft and ammunition render above it. Planet 7 permits more clear paving and overgrown ground while preserving path and rubble exclusions.

Each planet opens with three basic-Alien-only waves. Waves 4–5 add fast and armoured units, 6–7 add eligible aircraft and vehicles, 8–9 introduce heavier threats, and wave 10 ends with a boss. Enemy numbers, health and the advanced-enemy share rise through the level; planet unlocks still control which types can appear.

Enemy bounties have been increased by 20% across all 21 types to improve funding for late-wave towers and upgrades (basic Alien $12; Armoured Alien $30; Cyclops $180).

Late-wave pressure is limited: advanced units rise to 60% by wave 10. Each wave contains at most two heavy units (including the boss); only one heavy is active at once, with a three-second gap after it is defeated or escapes. Light units have 0.8-second spacing; a heavy gets a 2.5-second lead-in before the next spawn.

The campaign menu fits the viewport with all ten planets and Deploy visible. Build pads are densely packed near roads and inner bends, with direct pad clicks taking priority during construction.

Broodmothers give birth to two small Spiderlings after 6 seconds, then every 8 seconds, for at most three broods. No more than six Spiderlings can be alive at once. The young stay on their mother’s route, have low health, pay $6 each and cannot reproduce.

APCs deploy two basic Aliens after 6 seconds, followed by another pair 8 seconds later. Each APC carries four Aliens, and at most six deployed passengers can be alive at once. Passengers follow the APC’s own path, inherit its wave health scaling and pay the normal $12 bounty.

Shifting Sands uses wider stone gates with foreground occlusion for ground enemies. The former coloured route dots have been removed; the active north/south gate is identified in the wave status text.
