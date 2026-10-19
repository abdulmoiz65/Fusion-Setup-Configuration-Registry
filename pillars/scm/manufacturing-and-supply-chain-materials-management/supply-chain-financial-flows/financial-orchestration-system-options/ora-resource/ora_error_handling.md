# Error Handling

Source: Oracle Implement Supply Chain Financial Orchestration documentation and Oracle Financial Orchestration System Options documentation.

## Error Situations

| Situation | What Should Happen |
|---|---|
| The implementation project does not include Manufacturing and Supply Chain Materials Management or the System Options task | Stop and correct the project scope before configuring System Options. |
| More than one Financial Orchestration System Options record is returned | Stop and investigate the unexpected state; do not create a second record or update an ambiguous record. |
| The Item Validation Organization or required Service Item cannot be resolved | Stop and request an unambiguous reference; do not substitute a similarly named organization or item. |
| A non-null Service Item is supplied while the effective Configure service items for global purchase processing value is not true | Stop and require the option to be true before accepting a Service Item; do not enable it implicitly. |
| The Service Item LOV returns no rows for the resolved Item Validation Organization or no single item is selected | Stop and request a valid selection from that organization's LOV, unless `clearServiceItem = true` was explicitly requested. |
| A Service Item clear is requested | Allow it only when the clear is explicit, whether global service-item processing is enabled or disabled. An omitted Service Item is not an explicit clear request. |
| A lookup request path or match rule is not source-backed | Stop and request approved Oracle endpoint details; do not infer a Fusion REST endpoint or matching behavior. |
| The configured Fusion pod does not match the requested target, or a legacy `rest/rv` path is used | Stop before the request. Align the configured target pod and use the documented `resources/latest` resource path; do not fall back to another pod. |
| The Data Loader cannot prepare an archive because this REST business object has no UCM DAT `METADATA` section | Stop the request. Do not fabricate an archive, submit an incomplete file, or substitute a direct write route. |
| A proposed payload includes a field the user did not explicitly approve | Stop and remove the field from the preview; preserve unmentioned fields. |
| OAuth credentials, access tokens, or authorization headers would be recorded or displayed | Stop and redact them. Use only temporary untracked credential material and never place credentials in task resources or project artifacts. |
| A user requests a Fusion change | Do not mutate through this resource; use the separately routed workflow after its validation and approval gates are satisfied. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Project-scope gap | The required offering or setup task is not present in the implementation project | Correct the project scope, then restart validation. |
| System Options cardinality gap | More than one System Options record is returned | Investigate and correct the data state before another create or update attempt. |
| Reference-resolution gap | The selected validation organization or required service item is missing or ambiguous | Provide one valid, unambiguous reference. |
| Lookup-contract gap | Oracle documentation does not provide an executable endpoint or match rule | Supply an approved lookup contract; do not infer one. |
| REST-contract gap | The target pod, resource path, or REST-only execution route is not confirmed | Correct the endpoint or route before another request; do not fall back across pods or to an unsupported archive. |
| Update-concurrency gap | The current record version is absent, stale, or rejected | Re-read the one record, rebuild the update row, and obtain fresh approval before another load. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Validation blocker | The affected System Options field or prerequisite, the validation result, and a safe next action; never credentials or sensitive environment data. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A lookup contract contains TBD values | Do not infer Oracle lookup behavior, endpoints, payloads, or writes. |
| A Fusion mutation is requested | Do not treat this resource as authorization to perform a mutation. |
| An update load has an uncertain outcome | Do not repeat the load automatically or reuse the previous record version. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| FOS.SO.HANDLE_ISSUE | step | 30 | error_handler | handled->FOS.SO.RETURN_ISSUES | FOS.SO.VALIDATE_INPUT | stop | A project-scope, reference-resolution, lookup-contract, or input-validation issue occurs |
| FOS.SO.RETURN_ISSUES | terminal | 40 | terminal | none | FOS.SO.HANDLE_ISSUE | stop | A blocking issue was disclosed |
| FOS.SO.DONE | terminal | 50 | terminal | none | FOS.SO.RESOLVE_RECORD | stop | System Options values and record state are validated for the separate create-or-update workflow |
