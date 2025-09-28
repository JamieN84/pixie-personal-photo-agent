# Folder Organisation System Design

This document outlines the planned components that will allow Pixie to inspect libraries, plan folder structures, and execute moves safely.

## Architectural Overview
Pixie is composed of three primary subsystems:

1. **Filesystem scanner** – Reads the source inbox and target library, collecting metadata such as folder hierarchy, file counts, timestamps, and EXIF attributes. It should support dry runs and run-time filters to limit scope.
2. **Decision engine** – Combines user preferences, historical approvals, and current batch context to decide where each file belongs. The engine produces a ranked list of proposed destinations plus rationales.
3. **Move executor** – Applies the approved plan, handling folder creation, renames, moves, and rollback logging. It must gracefully handle partial failures and provide undo information.

## Key Data Flows
- **Input**: Paths to the "To sort" inbox and the destination library, optional natural-language prompts, stored preference files, and audit history.
- **Processing**: The scanner maps the current state, the decision engine builds a plan, and the executor performs operations once the user approves.
- **Output**: Updated folder structure, audit CSVs, and a summary report for the user.

## Operating Assumptions
- Pixie runs as a standalone CLI application with permissions to read and write within the configured directories.
- The user provides clear natural-language context when necessary but Pixie should default to safe holding areas when unsure.
- Audit logs are stored in the repository root (or configurable path) and can be replayed to undo actions.

## Error Handling
- **Pre-flight checks**: Validate source and target paths, ensure sufficient disk space, and confirm write permissions before planning moves.
- **Transactional moves**: Use temporary staging and renaming strategies to minimise the chance of partially moved files.
- **Recovery**: Provide a command (`--undo <audit_file>`) that replays the audit log to revert changes when possible.

## Extensibility Considerations
- **Plugin architecture**: Allow new metadata extractors (e.g., face recognition, object detection) to feed the decision engine without rewriting the core.
- **Cloud and hybrid storage**: Design abstractions so future integrations with cloud providers can reuse the same planning logic.
- **Automation hooks**: Expose APIs or scheduled tasks so Pixie can process new photos automatically once trust is established.

## Next Steps
- Define the schema for preference storage and auditing.
- Prototype the decision engine using a rules-based approach before layering ML-driven suggestions.
- Create sample libraries and automated tests to validate moves without touching personal data.
