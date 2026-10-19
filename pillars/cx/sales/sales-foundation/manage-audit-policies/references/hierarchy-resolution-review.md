# Hierarchy Resolution Review Evidence

These synthetic fixtures exercise the reasoning specified by the Child Object Inventory and Resolution workflow. They contain no tenant metadata. The expected outcomes were worked through against the scoped rows during the audit fix. They are declarative workflow review evidence, not results from an executable resolver or live Fusion. Existing text-contract tests remain structural checks.

Source: [hierarchy-scenarios.json](../tests/golden/hierarchy-scenarios.json).

| Scenario | Expected outcome | Review |
| --- | --- | --- |
| direct-sales-account | RESOLVED | Root exclusions do not exclude a live-bound child named Sales Account. |
| nested-child | RESOLVED | Each parent edge is present; the payload uses the immediate Address parent, not Account. |
| shared-contact-child | RESOLVED | The selected Contact root retains only its reachable path; Account is not inferred from the name. |
| ambiguous-paths | SELECTION_REQUIRED | Two immediate parents remain. Stop before status or preview; require path selection. |
| cycle | RESOLVED | Per-path visited identities prevent re-entering Address; the valid simple root path remains. |
| module-isolation | RESOLVED | Scope by sales and the mapped module before graph construction or attribute merging. |
| disconnected-child | REJECTED | Other children exist but this target has no validated path from Account. |
| missing-root | INCOMPLETE_INVENTORY | Mentioning Account in a parent list is not root existence proof; the mapped root row is absent. |
| empty-children | INCOMPLETE_INVENTORY | An empty hierarchy is incomplete inventory, not proof of unsupported children. |
| duplicate-display-name | REJECTED | An exact display-name request still requires a unique business-object identity. |

For resolved cases, compare business object, immediate parent and every edge in the expected path with the input rows. For module isolation, only AllowedField survives scope filtering. For ambiguous paths, both candidate paths exist and neither may be selected silently. For failed cases, no status request, preview or mutation is permitted. Review all cases again when root mappings, module scope or traversal rules change.
