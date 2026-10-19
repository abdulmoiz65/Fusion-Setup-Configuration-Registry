# Router Skills

Router skills are the entry point for FSCR implementation workflows.

They classify the customer implementation objective, determine the appropriate next actions, and orchestrate shared, core, and pillar skills in the required sequence.

## Initial Router Skills

| Skill | Purpose |
| --- | --- |
| `implementation-router` | Accepts the overall implementation objective and starts the guided implementation workflow. |
| `project-objective-classifier` | Classifies the objective by pillar, offering, functional area, scope, geography, and implementation phase. |
| `next-action-planner` | Determines the next recommended skill or human action based on current state and dependencies. |

## Token Usage Tracking

Every router skill activity must track token usage according to the skill
manifest's `token_usage_tracking` policy. Router runs should include a
`token_usage` estimate in their skill-run record and append or update the
project token usage log whenever routing outputs are persisted:

```text
project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md
```

Use exact tokenizer/API accounting when available; otherwise use the repository
default `chars/4` estimate and note any exclusions.
