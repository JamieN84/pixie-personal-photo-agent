# Starlight Picker – Initial Concept

Starlight Picker is a light, arcade-style prototype where players scoop up fallen starlight while drifting through a calm night sky. The goal is to quickly showcase the feel of the loop without needing art assets or complex UI.

## Core Loop
- Move your ship to collect drifting starlight shards.
- Avoid space debris that knocks energy off your hull.
- Survive the short session and rack up the highest score before your energy runs out.

## Controls & Rules
- **Movement:** Arrow keys to glide across the screen; movement is limited to the visible playfield.
- **Scoring:** Each shard adds points; consecutive pickups can be tuned later for streak bonuses.
- **Damage:** Colliding with debris removes energy/hearts. When energy is gone, the run ends.
- **Replayability:** A restart key should immediately reset the round without reloading the page.

## MVP Requirements
- Phaser-based single scene with a playable ship, collectible shards, and simple debris obstacles.
- Minimal HUD showing score, remaining energy/hearts, and a short description of controls.
- Procedural spawning for shards and debris to keep runs varied.
- Friendly difficulty curve suitable for a proof of concept; winning or losing should be clear.

## Visual Language
- Use solid-color primitives (triangles, circles, stars) so the build stays asset-free.
- Soft space palette (midnight background, warm highlights for shards, cool tones for debris).
- Subtle particle or glint effects can be added later; start with clean silhouettes.

This concept is intentionally lean so you can validate gameplay flow and integration with future AI-generated content.
