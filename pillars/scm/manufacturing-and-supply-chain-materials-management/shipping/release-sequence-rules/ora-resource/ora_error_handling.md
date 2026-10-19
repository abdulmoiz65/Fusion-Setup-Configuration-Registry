# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A priority or sort friendly value cannot be resolved because its resolver contract is TBD | Stop before preview and request a complete approved read-only resolver contract; do not guess a REST path or backend code. |
| A priority or sort lookup returns no exact match or multiple exact matches | Stop before preview and ask for a corrected or more specific value; do not choose the first result. |
| sequenceDFF values are supplied without a verified UCM template context and segment schema | Stop before preview and request the live Data Loader DFF template evidence; do not infer segments from the dynamic Redwood layout. |
| Data Loader rejects StartDateActive or EndDateActive format | Stop, rebuild the ZIP, and verify both literal active-date values against the selected-environment `releaseSequenceRules` Data Loader sample and attribute details. This applies even when the requested update changes only Description. |
| FSM import rejects an active date | Stop, rebuild the FSM ZIP from its current same-environment export template, and verify the CSV field matches that export’s representation. |
| An FSM package member, CSV header, or metadata XML differs from the export template | Stop before upload and rebuild the archive from the fresh export without renaming, removing, or reordering members or columns. |
| A populated FSM DFF or attribute field has no fresh template evidence | Stop before preview and obtain a task-specific export that identifies the supported context and segment columns. Blank DFF/attribute columns do not block the import. |
| Data Loader or Fusion rejects a prepared Release Sequence Rules record | Preserve the reported validation result, stop before retry, and correct the source through the governed Data Loader workflow. |
| Source data or the immutable preview changes after approval | Invalidate approval and require a newly validated immutable preview before any load. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Dependency blocker | A required lookup contract is TBD | Obtain the complete approved resolver contract. |
| Lookup resolution | An exact lookup has no match or is ambiguous | Request a corrected or more specific display value. |
| DFF schema readiness | sequenceDFF values are supplied without verified template context or segment metadata | Obtain live UCM template evidence before preparing the source. |
| Active-date contract | StartDateActive or EndDateActive does not match the selected route’s current Data Loader sample or FSM export template | Correct the source to the evidenced representation, rebuild the immutable preview, and obtain fresh approval. |
| FSM artifact contract | An FSM member, header, metadata XML, active-date format, or populated DFF/attribute value differs from the export contract | Rebuild the archive from the export template and obtain fresh approval. |
| Data Loader validation | The downstream business object rejects the source | Correct the source and rebuild the immutable preview. |
| Approval blocker | The source or preview changes after approval | Create and approve a new immutable preview. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup-contract blocker | The affected priority or sort field and the missing complete resolver contract |
| Lookup failure | The supplied display value and whether the result was no match or ambiguous |
| DFF schema blocker | That DFF context and segment metadata has not been verified from the Data Loader UCM template |
| Active-date contract failure | The supplied StartDateActive or EndDateActive value, selected route, and the missing or mismatched current template evidence |
| FSM artifact failure | The affected package member, CSV field, header, or unsupported populated DFF/attribute value |
| Data Loader validation failure | The governed validation result without credentials, tokens, or internal payload details |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A priority or sort resolver is incomplete | Do not construct a direct REST URL, guess a code, or select a similar lookup value. |
| DFF schema is not verified | Do not infer DFF segment names, context values, or child payload shape from the Redwood dynamic layout. |
| StartDateActive or EndDateActive is malformed | Do not retry the existing immutable archive. |
| An FSM archive changes after validation | Do not reuse prior validation or approval; rebuild and validate the changed archive. |
| A downstream validation or lookup fails | Do not retry a load or direct write automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| RSR.HANDLE_ISSUE | step | 70 | error_handler | disclosed->RETURN_ISSUES | none | stop | A prior node is invalid, blocked, unresolved, ambiguous, or failed |
| RSR.DONE | terminal | 80 | terminal | none | RSR.CHECK_DFF_READINESS | stop | All documented task-local rules have passed |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Error disclosure is complete |
