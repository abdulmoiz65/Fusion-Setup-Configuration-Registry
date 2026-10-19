# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required UOM input is missing or invalid | Stop and identify the missing field or the failed length validation. A Title Case issue is a warning and does not block lookup. |
| Units of measure class lookup fails | Stop before retry, classify the failure as transport, authorization, or Fusion API, and disclose the sanitized diagnostic. |
| Existing UOM class violates the conversion design rule | Block preview and show the base-unit or conversion condition that must be corrected. |
| Bypass approval is absent | Stop; obtain explicit user approval tied to the UOM class and the identified blocker before continuing. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Required input is missing or UOMCode or UOM exceeds its documented maximum length | Correct the input and rerun validation. |
| Transport or authorization or Fusion API | The read-only UomFinder request cannot complete | Stop before retry and resolve the reported environment, access, or API issue. |
| Approval blocker | A conversion-design bypass is requested without explicit user approval | Request explicit approval for the precise UOM class and blocker. |
| Design blocker | Existing UOM conversion design does not meet the documented rule and no approved bypass exists | Correct the base unit or conversion values, or request an explicit bypass. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | Environment, read-only request purpose, failure class, sanitized message, and safe next action. |
| Design blocker or bypass | UOMClass, evaluated base-unit and conversion facts, blocker condition, and the approval requirement. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup or validation failure | Do not retry automatically or infer a class result. |
| Design blocker | Do not proceed to preview or a live write without either correction or explicit user approval to bypass. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| UOM.GATE-BYPASS-APPROVAL | decision | 40 | execution_gate | approved->UOM.DONE-APPROVED-BYPASS;approval_missing->UOM.HANDLE-APPROVAL-BLOCKER | UOM.ENFORCE-CONVERSION-DESIGN | stop | A bypass of the conversion design blocker is requested |
| UOM.HANDLE-INPUT-ERROR | step | 50 | error_handler | handled->UOM.RETURN_ISSUES | UOM.VALIDATE-INPUT | stop | Input validation is invalid |
| UOM.HANDLE-LOOKUP-ERROR | step | 60 | error_handler | handled->UOM.RETURN_ISSUES | UOM.LOOKUP-CLASS | stop | The UomFinder lookup fails |
| UOM.HANDLE-DESIGN-BLOCKER | step | 70 | error_handler | handled->UOM.RETURN_ISSUES | UOM.ENFORCE-CONVERSION-DESIGN | stop | The conversion design rule blocks the request without a bypass request |
| UOM.HANDLE-APPROVAL-BLOCKER | step | 80 | error_handler | handled->UOM.RETURN_ISSUES | UOM.GATE-BYPASS-APPROVAL | stop | Bypass approval is missing |
| UOM.DONE-NEW-CLASS | terminal | 90 | terminal | none | UOM.LOOKUP-CLASS | stop | The UOM class does not exist |
| UOM.DONE-CLASS-COMPLIANT | terminal | 100 | terminal | none | UOM.ENFORCE-CONVERSION-DESIGN | stop | The existing UOM class complies with the conversion design rule |
| UOM.DONE-APPROVED-BYPASS | terminal | 110 | terminal | none | UOM.GATE-BYPASS-APPROVAL | stop | Explicit user approval bypasses the conversion design blocker |
| UOM.RETURN_ISSUES | terminal | 120 | terminal | none | none | stop | A validation, lookup, design, or approval issue is handled |
