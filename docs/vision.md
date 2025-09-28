# Pixie Vision

Pixie is a standalone agent that gives people a trustworthy companion for organising their personal photo collections. The project aspires to combine deep awareness of a user's existing folder structure with conversational guidance so that tidying up photos feels collaborative rather than tedious.

## Mission
- Deliver an assistant that can sort large backlogs of photos without compromising the user's preferred organisation style.
- Provide clear previews and undo paths so every automated action feels reversible and safe.
- Keep the experience self-contained, running locally when possible so users can work with private collections without relying on external services.

## Guiding Principles
1. **Context first** – Pixie always inspects the current library before acting so it can mimic the user's conventions.
2. **Explainability** – Every planned move comes with a reason and appears in an audit log for review.
3. **User-in-the-loop** – Pixie accepts natural-language direction and confirmations, blending automation with conversational control.
4. **Resilience** – Operations should be idempotent, guard against partial moves, and offer straightforward recovery steps.

## Success Indicators
- Users routinely rely on the "To sort" inbox as a staging area and trust Pixie to make the right choices.
- Library structures remain coherent after repeated runs, demonstrating that Pixie adapts to evolving preferences.
- Contributors can extend Pixie's capabilities without re-learning the system because the design documents and roadmap stay current.

## Related Documents
- ["To sort" workflow and preference handling](to-sort-workflow.md)
- [Folder organisation system design](system-design.md)
