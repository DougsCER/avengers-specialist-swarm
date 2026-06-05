# The Swarmvengers — Executable Agent Story

> **Dual-purpose document.** Humans read it as a story. AI agents read it as a runnable
> orchestration spec. The narrative lines are flavor; the fenced `yaml`/`json` blocks and
> the `## EXECUTION` section are the contract. An orchestrator should parse the structured
> blocks and ignore prose when executing.

---

## STORY (human layer)

The world received a **Request For Planet** from the Vorlani Collective: submit a flawless
proposal by nightfall or Earth goes dark. No single hero could answer it. So the
**Coordinator** assembled a swarm of specialists — **Pricing**, **Legal**, **Technical Fit**,
and **Competitive** — who worked *all at once*, in parallel. At the last second the **Critic**
caught the one fatal flaw, the Coordinator fixed it, and the bid was accepted.

Earth wasn't saved by one hero. It was saved by a swarm. 🐝

---

## SPEC (machine layer)

```yaml
swarm:
  name: The Swarmvengers
  version: 1.0
  goal: >
    Transform an inbound RFP ("Request For Planet") document into a single, flawless,
    branded proposal deliverable before the deadline.
  success_criteria:
    - All four specialist lanes completed and merged.
    - Critic gate passed (no blocking issues remain).
    - Final deliverable produced as a branded .docx.
  inputs:
    rfp_document:
      type: file
      required: true
      description: The RFP/tender document to respond to.
    deadline:
      type: timestamp
      required: false
  outputs:
    proposal:
      type: file
      format: docx
      description: Final branded proposal, ready to submit.
```

### Roles

```yaml
agents:
  coordinator:
    title: Coordinator (orchestrator)
    role: |
      Orchestrate the swarm. Ingest the RFP, dispatch all specialists IN PARALLEL,
      collect their outputs, resolve conflicts, synthesize one coherent proposal,
      send it through the Critic gate, apply required fixes, then produce the final deliverable.
    delegates_to: [pricing, legal, technical_fit, competitive]
    gate: critic

  pricing:
    title: Pricing Specialist
    role: Evaluate financial terms and produce an honest, competitive cost model.
    output_key: pricing_analysis

  legal:
    title: Legal Specialist
    role: Review compliance and contractual terms; flag hidden clauses, risks, and loopholes.
    output_key: legal_review

  technical_fit:
    title: Technical Fit Specialist
    role: Assess solution alignment; ensure promises in the proposal are technically deliverable.
    output_key: technical_assessment

  competitive:
    title: Competitive Specialist
    role: Analyze competitive positioning and articulate the differentiated win theme.
    output_key: competitive_positioning

  critic:
    title: Critic (review gate)
    role: Adversarially review the synthesized draft; return BLOCKING issues that must be fixed.
    output_key: critic_verdict
```

### Specialist task contract

Each specialist receives the same input envelope and must return the same output shape.

```json
{
  "input": {
    "rfp_document": "<file ref>",
    "context": "<coordinator notes, optional>"
  },
  "output": {
    "summary": "string — 2-3 sentence headline finding",
    "findings": ["string — key points, evidence-backed"],
    "risks": ["string — issues for other lanes or the coordinator to know"],
    "recommendation": "string — what this lane wants reflected in the final proposal",
    "confidence": "low | medium | high"
  }
}
```

### Critic gate contract

```json
{
  "input": { "draft_proposal": "<text>", "specialist_outputs": "<map>" },
  "output": {
    "verdict": "approve | revise",
    "blocking_issues": [
      { "location": "string", "problem": "string", "required_fix": "string" }
    ],
    "notes": "string — non-blocking suggestions"
  }
}
```

---

## EXECUTION (the runnable plan)

Deterministic steps for the orchestrator. Steps 2a–2d run **concurrently**.

```yaml
steps:
  - id: 1_ingest
    agent: coordinator
    action: Read rfp_document. Extract requirements, constraints, and the deadline.
    produces: rfp_brief

  - id: 2_dispatch_parallel
    agent: coordinator
    action: Dispatch all specialists at once with rfp_brief. Do NOT serialize.
    parallel:
      - { id: 2a, agent: pricing,       produces: pricing_analysis }
      - { id: 2b, agent: legal,         produces: legal_review }
      - { id: 2c, agent: technical_fit, produces: technical_assessment }
      - { id: 2d, agent: competitive,   produces: competitive_positioning }
    join: wait_for_all

  - id: 3_synthesize
    agent: coordinator
    action: >
      Merge all four specialist outputs into one coherent draft proposal.
      Resolve conflicts (e.g. a price that legal flags, or a promise technical_fit cannot back).
    produces: draft_proposal

  - id: 4_critic_gate
    agent: critic
    action: Review draft_proposal against specialist_outputs. Return verdict.
    produces: critic_verdict

  - id: 5_revise_loop
    agent: coordinator
    condition: critic_verdict.verdict == "revise"
    action: Apply every blocking_issue.required_fix, then return to step 4_critic_gate.
    max_iterations: 3

  - id: 6_deliver
    agent: coordinator
    condition: critic_verdict.verdict == "approve"
    action: Render the approved proposal as a branded .docx. This is the final deliverable.
    produces: proposal
```

### Invariants (must always hold)

```yaml
invariants:
  - Specialists never call each other directly; only the coordinator routes between lanes.
  - Step 2 specialists run in parallel, not in sequence.
  - The deliverable is produced ONLY after the critic returns verdict == "approve".
  - If max_iterations is reached without approval, escalate to a human; do not ship.
  - Every claim in the final proposal must trace to a specialist finding.
```

---

*Earth wasn't saved by one hero. It was saved by a swarm.* 🐝
*— The Swarmvengers will return (when the next RFP lands).*
