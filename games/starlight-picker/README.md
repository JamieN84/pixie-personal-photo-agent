# Starlight Picker Prototype

A minimal Phaser-based proof of concept inspired by `docs/specifications/initial-concept.md`. Fly a small ship, pick up golden starlight shards, and dodge drifting debris. Restart instantly with **R**.

## How to run locally
1. From the repository root, start a simple web server:
   - Python: `python -m http.server 8000`
   - Or `npx http-server` if you prefer Node-based tooling.
2. Open `http://localhost:8000/games/starlight-picker/` in your browser.
3. Use the arrow keys to move, collect starlight for points, dodge debris, and press **R** after a run to restart.

No build step is required because Phaser is loaded from a CDN and all visuals use generated shapes.
