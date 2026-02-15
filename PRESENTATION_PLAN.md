# Hackathon III: Presentation & Video Plan 🎥

This plan provides scripts and demo flows for the four **90-second videos** required for your submission.

---

## Video 1: LearnFlow Application (The Face) 🎨
**Goal**: Demonstrate the functional value of the AI Tutoring Dashboard.

1.  **Opening (0-15s)**: Start with the browser on `http://localhost:3000`. Show the "System Online" indicator.
2.  **The Demo (15-60s)**:
    -   Type: "I need to learn about Kafka Producers."
    -   Show the **Triage-Agent** routing the request to the **Concepts-Agent**.
    -   Highlight the real-time response generation.
3.  **The Tech (60-90s)**: Mention the **Dapr sidecars** and **Kafka/Postgres** backbone running in Kubernetes.
4.  **Closing**: "LearnFlow: Intelligent, Cloud-Native Education."

---

## Video 2: Skills Library (The Brain) 🧠
**Goal**: Show how AI intelligence is packaged into reusable units.

1.  **Opening (0-15s)**: Open the `.claude/skills/` directory in your IDE.
2.  **The Demo (15-60s)**:
    -   Focus on `mcp-code-execution`.
    -   Show how the `SKILL.md` is tiny (intent) while the `scripts/` handle the heavy lifting.
    -   Explain: "We save tokens and increase reliability."
3.  **The Validation (60-90s)**: Run `python verify.py` in one of the skills folder to show automated verification.
4.  **Closing**: "9 Skills. Zero Token Waste. Pure Execution."

---

## Video 3: CAPS Library (The Law) ⚖️
**Goal**: Demonstate Spec-Driven Development (SDD) governance.

1.  **Opening (0-15s)**: Open `specs/governance/system.spec.md`.
2.  **The Demo (15-60s)**:
    -   Explain the **CAPS** methodology (Constitution, Agents, Product, Specs).
    -   Show the "Supreme Rules" like "No direct MCP loading."
3.  **The "Wow" (60-90s)**: Run the governance check script (`validate_repo.py`).
    -   Show the final score (e.g., 95/100).
4.  **Closing**: "Governance that isn't just a document—it's an executable rule."

---

## Video 4: Spec-Kit Plus (The Engine) 🚀
**Goal**: Show the developer experience (DX) and automation.

1.  **Opening (0-15s)**: Open the `.specify/` directory.
2.  **The Demo (15-60s)**:
    -   Run `./.specify/scripts/powershell/update-agent-context.ps1`.
    -   Show how it automatically updates memory files across different agents.
3.  **The Workflow (60-90s)**: Show a **Prompt History Record (PHR)** template.
    -   Explain how it captures every decision and interaction for "Reusable Intelligence."
4.  **Closing**: "Spec-Kit Plus: Building AI systems with architectural integrity."

---
**Status**: Ready for Recording  
**Tip**: Use a screen recorder with high resolution. Keep the pacing fast! 🚀🏁
