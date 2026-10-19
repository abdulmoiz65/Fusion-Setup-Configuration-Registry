# Manage Account Combinations Design Enforcement

Design gates prevent the first live import from being used to discover basic package, identity, or defaulting defects.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Import-mode boundary | Use FBDI only; do not route this task through FSM import or export. |
| 2 | Candidate closure | Validate every row and the one-member ZIP contract before a preview or handoff. |
| 3 | COA identity | Require consistent COA code and structure-instance evidence. |
| 4 | Execution boundary | Hand off only the verified package through the approved data-loader workflow after current explicit approval. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Always | Blocker |  | FSM import or export is selected for Manage Account Combinations | Use the FBDI candidate and packaging contract only | Yes |
| A CSV or ZIP is supplied | Blocker |  | The package is not named GlBulkComboInterface.zip, has a header, not exactly 62 columns, a different root member, or any invalid row | Correct the candidate and revalidate before package handoff | Yes |
| Candidate includes a COA identity | Blocker | resolve_chart_of_accounts_from_candidate | The exact enabled COA does not resolve through the candidate's code-first and natural-language name-fallback sequence, or the CSV code disagrees with StructureInstanceCode | Correct the candidate identity and regenerate the candidate | Yes |
| Before import approval | Blocker |  | The package is unverified, or the approval is stale or for a different package/environment | Create an exact preview, then obtain approval for that preview | Yes |
| When dates, posting, attributes, or alternate account are supplied | Warning |  | Values do not reflect the intended enablement, posting, attribute inheritance, or disabled-combination behavior | Review Enabled, From Date, To Date, Allow Posting, Preserve Attributes, and Alternative Account before preview | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_chart_of_accounts_from_candidate | Candidate includes a COA identity | StructureInstanceCode, StructureInstanceNumber, StructureInstanceId, enabled evidence | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAC-050-ENFORCE-DESIGN | decision | 50 | design_enforcement | compliant->MAC-060-EXECUTION-GATE;blocked->MAC-070-HANDLE-ERROR | MAC-040-APPLY-DEFAULTS | stop | Always |
