# Consolidation Groups Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Explicit integration-key columns | Omit SourceSystemOwner, SourceSystemId, and other explicit integration-key columns | Create uses the verified working MERGE shape | No; the record uses ConsolidationSetCode and LegislativeDataGroupName as its supported user key | |
| Comments | Omit the Comments field and ClobFiles entry | Create or Update and no description is supplied | No; a supplied description must be packaged as a referenced UTF-8 file | |
| SearchTerms and FilterAttributes | Omit both finder inputs | LDG-scoped list or Read One precheck has no keyword | Yes; include both only when a keyword search is explicitly requested | |

Do not default ConsolidationSetCode from ConsolidationSetName. The documented HDL shape requires both values, Oracle documents Code as immutable after creation, and the current UI uppercase behavior is not a universal HDL rule.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CG.APPLY_DEFAULTS | decision | 4 | apply_default | applied->CG.ENFORCE_DESIGN;skipped->CG.ENFORCE_DESIGN | CG.RESOLVE_REFERENCES | stop | Validated request with ready dependencies and references |

## Sources

- Developer-provided ConsolidationGroups.md, updated and reviewed 2026-08-13.
- Oracle Fusion Cloud HCM, Consolidation Groups: https://docs.oracle.com/en/cloud/saas/human-resources/faagp/consolidation-groups.html
- Oracle Fusion Cloud HCM, Example of Loading Payroll Consolidation Group: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/example-of-loading-payroll-consolidation-group.html
