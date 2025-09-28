# "To Sort" Workflow and Preference Handling

This document defines how Pixie should process photos staged in the user's "To sort" folder and how preference data influences the proposed organisation plan.

## Workflow Overview
1. **User staging** – The user drops new or backlog photos into the "To sort" folder and optionally writes a short natural-language note describing the batch (e.g., "Emma's birthday, March 2024, park picnic").
2. **Context gathering** – Pixie scans the target library to understand existing folder patterns, people or event naming conventions, and date formats. It also checks stored preference files or prior user confirmations.
3. **Interpretation** – Pixie parses the natural-language note plus embedded metadata (EXIF timestamps, geolocation, faces) to produce a structured intent: who is involved, what event occurred, when and where it happened, and any special handling instructions.
4. **Planning** – Based on the intent and the observed library structure, Pixie proposes folder operations: create new folders, reuse existing ones, or adjust naming to stay consistent. It prepares an audit table that describes each planned move.
5. **Review loop** – Pixie presents the plan for confirmation. The user can accept, decline, or refine the instructions conversationally.
6. **Execution** – When approved, Pixie performs moves (or copies) and records the outcome in an audit CSV for undo purposes.

## Preference Sources
- **Configuration file** – A structured file (e.g., `preferences.json`) stores explicit choices such as default date formats, preferred folder depth, and whether to group by people or events.
- **Learned behaviour** – Pixie updates heuristics based on previous user approvals or corrections, gradually learning custom folder names and ordering.
- **Inline instructions** – Natural-language commands supplied with a batch take precedence for that run (e.g., "Use yyyy-mm event naming" or "Keep duplicates").

## Edge Cases and Safeguards
- **Conflicting instructions** – When inline instructions clash with stored preferences, Pixie should request clarification before executing moves.
- **Missing metadata** – If crucial data such as dates or locations is absent, Pixie should either prompt for details or default to a safe holding folder that flags the issue.
- **Permission issues** – The agent must verify write access before planning moves and surface actionable errors when access is denied.
- **Large batches** – For thousands of photos, Pixie should chunk operations and ensure the audit log remains readable.

## Outputs
- **Audit CSV** – Captures proposed and completed actions, including source path, destination path, decision reason, and status.
- **Summary report** – Highlights newly created folders, skipped items, and follow-up questions for the user.

## Future Considerations
- Automate preference onboarding by interviewing the user the first time they run Pixie.
- Support collaborative households by letting multiple profiles share a library with personalised preferences.
- Integrate confidence scores so the user can quickly review uncertain decisions before approval.
