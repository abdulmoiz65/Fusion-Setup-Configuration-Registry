# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Target isolation | Confirm all lookup responses, mapping IDs, and writes belong to the selected target environment. |
| 2 | REST-only reference resolution | Resolve lookup codes and target identifiers through the maintained REST declarations; database access is diagnostic-only. |
| 3 | Complete Plan Copy mappings | Require every named source mapping to contain its REST-resolved target identifier before the combined generateMappings/import request. |
| 4 | Immutable approval | Require a current preview and exact later approval before the governed runbook performs its first mutation. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Any workbook value requires a target lookup code or identifier | Blocker | resolve_eligibility_profile_references | The value was populated from a database, another pod, a guessed ID, an undocumented API, or an unresolved or ambiguous result | Resolve the exact value from the maintained REST catalog on the selected target environment; ask for the corresponding REST API if the catalog has no supported resolver | Yes, before package generation |
| The generated package contains Plan Copy mapping rows | Blocker | inspect_plan_copy_mappings | A populated SrcName has null or blank TrgId before submission or after generateMappings | Correct the target-pod REST resolution and regenerate the package; do not require later manual mapping | Yes, before generateMappings |
| A live Plan Copy execution is requested | Blocker | | Target, workbook-derived effective date, package digest, OpenAPI digest, metadata, or intended action differs from the approved preview | Create and review a new immutable preview, then obtain a later standalone approve message | Yes, with a new preview and approval |
| ESS reports successful completion | Blocker | inspect_plan_copy_result | Plan Copy parent ImportPlDesign is not 12, is 10, or RequestStatus is terminally unsuccessful | Continue the documented read-only verification or report the application failure and processing-log messages | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_eligibility_profile_references | Before generating XML for every populated lookup-backed workbook field | Target-pod lookup codes, labels, source identifiers, target identifiers, and context identifiers | ora_reference_lookups.md |
| inspect_plan_copy_mappings | Before generateMappings and after its combined mapping/import ESS request | Every mapping row, resolved count, unresolved rows, and TrgId completeness | ora_reference_lookups.md |
| inspect_plan_copy_result | After the combined ESS request completes or when resuming an existing import | ImportPlDesign, RequestStatus, processing-log count, and sanitized messages | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PLAN_COPY.ENFORCE_DESIGN | decision | 4 | design_enforcement | passed->BEN_PLAN_COPY.EXECUTION_GATE;blocked->BEN_PLAN_COPY.FAILED | BEN_PLAN_COPY.RESOLVE_REFERENCES | stop | Before presenting or accepting approval for the governed Benefits Plan Copy REST runbook. |
