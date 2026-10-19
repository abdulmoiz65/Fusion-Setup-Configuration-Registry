# Execution Gate and Recovery

Inherit the parent immutable preview, standalone approval, error classification, log verification, and no-write-retry rules. The Markdown import workflow verifies the Opportunity Marketplace task identity in the parent preview. The gate is not applicable during preview; live import requires current approval. Evaluation has its own later approval. Monitoring uses only GET requests and retained run context.

Parent contract: [Execution Gate and Recovery](../../../../benefits-configuration/benefits-eligibility/eligibility-profiles/ora-resource/ora_error_handling.md). Load it for this node; the child overrides above take precedence.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| OM_ELIG.GATE | decision | 5 | execution_gate | approved->OM_ELIG.READY;approval_missing->OM_ELIG.AWAITING | OM_ELIG.DESIGN | stop | Immediately before approved native Plan Copy execution. |
| OM_ELIG.READY | terminal | 6 | terminal | none | OM_ELIG.GATE | stop | All preparation and approval gates have passed. |
| OM_ELIG.AWAITING | terminal | 7 | terminal | none | OM_ELIG.GATE | stop | Preview is ready; wait for standalone approval. |
| OM_ELIG.FAILED | terminal | 8 | terminal | none | none | stop | A validation, dependency, lookup, design, or execution blocker is present. |
