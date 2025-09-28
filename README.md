# Pixie Personal Photo Agent

## Overview
Pixie is a standalone assistant that helps people organise their personal photo libraries. It analyses the existing folder structure, understands a user's stated preferences, and plans safe file moves so every photo ends up where it belongs. The long-term goal is to give users confidence that Pixie can take a pile of unsorted memories and transform it into a curated collection.

## Core Use Cases
- **Inbox triage** – interpret natural-language context supplied with photos placed in a "To sort" folder and recommend the best destination folders.
- **Preference-aware organisation** – respect the user's conventions for naming, hierarchy depth, and people or event tags when planning folder creation and file moves.
- **Guided operation** – offer dry-run previews, undo logs, and conversational prompts so users stay in control while Pixie performs the heavy lifting.

## Planned Capabilities
- Inspect existing libraries to understand current folder patterns and important metadata.
- Create new folders or rename existing ones to match expressed preferences.
- Move, copy, or skip photos with full audit logging and the ability to undo changes.
- Accept natural-language instructions that clarify what the latest batch of photos represents (e.g., people, places, dates).
- Learn from prior decisions to refine future recommendations.

## Roadmap & Further Reading
Pixie's product vision and detailed workflows are documented in the `docs/` directory.

- [Vision](docs/vision.md)
- ["To sort" workflow and preference handling](docs/to-sort-workflow.md)
- [Folder organisation system design](docs/system-design.md)

Contributors should review these documents before proposing new features so that design and implementation decisions stay aligned with Pixie's mission.
