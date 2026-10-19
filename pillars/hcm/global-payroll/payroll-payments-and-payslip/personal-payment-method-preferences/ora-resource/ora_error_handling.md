# Personal Payment Method Preferences Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Finder or Intent is missing or incompatible with the requested search | Stop and state the required finder and Intent pairing. |
| LDG name has no match or many matches | Stop and ask for a more precise LDG identifier; do not select an LDG automatically. |
| OPM lookup is requested without a resolved LDG | Stop before the lookup and request or resolve the LDG. |
| An OPM name has no match or many matches in the selected LDG | Stop and ask for the exact OPM identity. |
| An OPM ID does not belong to the selected LDG | Stop and identify the user-facing field, supplied value, Organization Payment Method reference type, and invalid LDG-context classification. |
| A pipe-separated OPM value fetched through REST includes an unresolved value | Reject the entire requested operation, identify every invalid value and its index, retain pipe-separated presentation, and do not submit a partial list. |
| A pipe-separated OPM value fetched through REST includes an empty value | Reject the field and identify the empty position; do not remove it silently. |
| A DAT OPM value uses a pipe delimiter | Reject DAT preparation and require comma-separated IDs for OrgPaymentMethodsAvailableToWorker and OrgPaymentMethodsRestrictedForEdit. |
| A reference ID is invalid or a lookup code is invalid | Stop and identify the user-facing field, supplied value, expected reference or lookup type, and invalid-value classification. |
| YES_NO lookup does not return one applicable code | Stop and request an approved value; do not assume Y or N. |
| ValidationExclusionFlag is not Y or N | Stop and request Yes or No or a valid code. |
| PaymentAmountTypes is outside A, P, or B | Stop and request Amount, Percentage, or Both. |
| PaymentMethodsMaximumNumber is not a whole number | Stop and request digits only; do not accept decimals or nonnumeric text. |
| Preference SEARCH returns an ambiguous result | Stop and request resolution of the duplicate or ambiguous preference data; do not derive operation. |
| A caller supplies operation | Ignore the supplied value, derive operation from SEARCH and deletion intent, and do not ask the user to provide operation. |
| The custom-action path has an extra or missing slash, uses an HTTP method other than POST, has another media type, or has RestAction other than POST | Stop before submission and correct it to the supplied custom-action transport contract. RestAction is POST regardless of operation. |
| CREATE is selected but SEARCH found a preference | Stop and reclassify as MERGE; do not create another preference. |
| A MERGE attempts to change the LDG association, omits any returned optional or supplied action-contract attribute, or uses a stale value | Stop, rerun Intent SEARCH for the resolved LDG, and require a corrected complete-state MERGE payload or DAT row. Do not accept a modified-fields-only payload. |
| A DELETE has no existing preference for the resolved LDG | Return a not-found validation message and do not invoke the custom action. |
| A DELETE attributesMap row is absent, has no LegislativeDataGroupId, or has RestAction other than POST | Stop DAT preparation and require one attributesMap DELETE row with PreferencesKey and LegislativeDataGroupId set to the resolved ID, RestAction set to POST, and all other child business attributes blank. |
| Describe metadata is requested but no response is available | State that per-attribute metadata cannot be generated until a redacted describe response or authorized Fusion environment is supplied. |
| A reference cannot be resolved for hierarchy presentation | Retain the ID or code, show Unresolved rather than a fabricated name or meaning, and identify the failed resolver. |
| A live custom-action response is uncertain | Do not retry the POST automatically; reconcile through a read-only preference lookup before any user-authorized retry. |

## User-Facing Error Messages

| Error Condition | Required User-Facing Message |
|---|---|
| No reference or lookup match | No valid <REFERENCE_TYPE> was found for "<INPUT_VALUE>" in field "<FIELD_NAME>". |
| Multiple reference or lookup matches | Multiple <REFERENCE_TYPE> records matched "<INPUT_VALUE>" in field "<FIELD_NAME>". Provide a unique name or ID. |
| OPM outside the resolved LDG | Organization Payment Method "<OPM_NAME_OR_ID>" is not valid for Legislative Data Group "<LDG_NAME>". |
| Duplicate preference before create | A Payment Method Preference already exists for Legislative Data Group "<LDG_NAME>". |
| Preference absent for update or delete | No Payment Method Preference exists for Legislative Data Group "<LDG_NAME>". |
| Unsupported lookup value | "<INPUT_VALUE>" is not a supported value for "<FIELD_NAME>". Supported values are: <VALUES>. |
| Invalid maximum payment-method count | "<INPUT_VALUE>" is not valid for Maximum Personal Payment Methods. Enter a whole number. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required intent, LDG identity, or reference is absent | Request the exact missing fact; do not request operation. |
| METADATA_UNAVAILABLE | A describe response required for field-level metadata is unavailable | Request the describe response; do not infer server metadata. |
| INVALID | Finder, Intent, amount type, or resolved value violates the supplied contract | Correct the reported value and validate again. |
| NOT_FOUND | A required preference, reference, or lookup record does not exist | Provide a valid value or create the prerequisite through an approved workflow. |
| AMBIGUOUS | A lookup has multiple matching records | Request a more precise identifier. |
| DUPLICATE | SEARCH returns more than one preference for the selected LDG | Resolve the duplicate or ambiguous preference data before deriving operation. |
| BLOCKED | A prerequisite, preview, approval, or server-validated detail prevents safe continuation | Resolve the blocker before execution. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Lookup failure | The resolver, supplied value, and whether there was no match or more than one match. |
| Mutation gate | The automatically derived operation, resolved references, SEARCH result, preview, approval, custom-action path, method, media type, and for MERGE the latest SEARCH state plus every returned attribute, including optional attributes, carried into the payload or DAT row. |
| Mutation error | Sanitized server evidence only; never credentials, tokens, or protected identifiers. |
| Functional validation error | Present the applicable required user-facing message first; include redacted backend evidence only when it materially helps diagnosis. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| A mutation is not separately authorized | Do not build a payload template or invoke the custom action from this resource-authoring workflow. |
| A MERGE payload or DAT row contains only modified fields, omits optional returned values, or uses stale values | Do not submit it; require a fresh SEARCH result and a complete latest-state representation. |
| A lookup is ambiguous | Do not select a candidate or continue to preview. |
| A prior write outcome is uncertain | Do not automatically retry the operation. |
| A clearer functional validation exists | Do not return a raw backend error as the only user-facing response. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PPMP.EXECUTION_GATE | decision | 9 | execution_gate | ready_read->PPMP.DONE_READ;ready_mutation->PPMP.DONE_MUTATION;blocked->RETURN_ISSUES | PPMP.ENFORCE_DESIGN | stop | Any request after validation and design enforcement |
| RETURN_ISSUES | terminal | 10 | terminal | none | none | stop | A validation, lookup, dependency, design, or write-contract blocker occurs |
| PPMP.DONE_READ | terminal | 11 | terminal | none | PPMP.EXECUTION_GATE | stop | A read-only request completed with documented results |
| PPMP.DONE_MUTATION | terminal | 12 | terminal | none | PPMP.EXECUTION_GATE | stop | A separately authorized and verified CREATE, MERGE, or DELETE action completed; MERGE used a fresh complete-state payload or DAT row including optional returned attributes. |

## Sources

- Developer-supplied safety requirements and REST scope.

## Data Loader Route Guard

| Situation | What Should Happen |
|---|---|
| Actual data create, import, or load is requested | Route the request to core.data-loader using paymentMethodOptions. The existing REST material remains reference-only. |
| A CRUD endpoint or custom action is proposed for actual data creation, import, or load | Stop before execution and require the Data Loader business-object workflow. |
| The Data Loader source changes after preview | Stop and require a new preview and approval before any load. |

## Execution Policy Source

- Developer instruction: retain documented instructions for reference; perform actual data create, import, and load through the documented business object.
