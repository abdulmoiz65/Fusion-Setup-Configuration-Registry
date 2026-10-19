# Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required rule-set, rule, serialized definition, or translation identity field is missing | Classify the failure as input validation, identify the row and field, stop before ZIP assembly or upload, and require a corrected value or transformation. |
| A field exceeds an Oracle data-dictionary length or precision limit | Classify the failure as input validation, report the normalized field name, sanitized value, actual size, and documented maximum, then stop before upload. |
| Composite, Draft, or another documented enum has an unsupported value | Classify the failure as input validation, report the accepted values, and stop before upload. |
| A generated rule or translation row does not match its parent identity | Classify the failure as input validation, identify both sanitized identities, and rebuild the archive with consistent parent and child keys. |
| Fusion returns JBO-27040 for RuleName | Treat JBO-27040 as the primary cause. The surrounding JBO-25026, JBO-25027, and JBO-25025 messages are row and rowset load failures caused by the invalid RuleName. |
| A logical input value is longer than its technical database representation | Apply the documented transformation first and validate the generated technical value; for example, validate ITEM_DESC rather than rejecting ITEM_DESCRIPTION against the RETURN_TYPE limit. |
| A validated input or generated archive changes after approval | Treat the archive as changed, rebuild it, rerun validation, calculate a new hash, and require a new upload approval. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | A required value is missing; a type, length, precision, enum, XML, or parent-child identity check fails | Correct the input or transformation and restart archive preparation and validation. |
| Reference-data validation | A structurally valid association type, association code, or other reference value cannot be confirmed in the target Fusion environment | Preserve the unresolved value and stop until the declared reference-data workflow resolves it. |
| Fusion API | Fusion rejects an archive that passed the documented local schema checks | Preserve the primary Fusion message and stop before retry for diagnosis. |
| Approval blocker | The corrected or regenerated archive does not have approval bound to its new hash | Present the corrected validation result and request new upload approval. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Input or generated archive validation fails | Affected row, normalized field name, sanitized supplied or generated value, actual type or size, accepted values or maximum, and a compliant correction example when one is known. |
| Parent-child identity validation fails | Sanitized parent and child identities and which matching relationship failed. |
| Fusion import fails | Primary actionable Fusion message and the safe next action; do not present cascading rowset messages as separate causes. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Any required input, shape, type, length, precision, enum, XML, or identity validation fails | Do not approve, upload, import, or retry the archive. |
| A corrected or regenerated archive has not been revalidated and reapproved | Do not reuse the prior archive hash, approval, upload, or import request. |
| A reference value is structurally valid but unresolved | Do not present local schema success as proof that the reference exists in the target environment. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MIRS.HANDLE_INPUT_ERROR | step | 20 | error_handler | handled->MIRS.RETURN_ISSUES | MIRS.VALIDATE_INPUT | stop | Any documented input or generated archive validation fails |
| MIRS.READY | terminal | 30 | terminal | none | MIRS.VALIDATE_INPUT | stop | All documented input and generated archive validations pass |
| MIRS.RETURN_ISSUES | terminal | 40 | terminal | none | none | stop | Validation issues are returned for correction |
