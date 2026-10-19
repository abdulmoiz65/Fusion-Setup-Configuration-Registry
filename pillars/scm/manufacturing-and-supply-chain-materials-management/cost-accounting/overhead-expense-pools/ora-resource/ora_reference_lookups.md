# Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_delete_target | DELETE after any supplied SetName or ExpensePoolTypeCode qualifier is resolved | Current approved Overhead Expense Pools task-export baseline; trimmed ExpensePoolCode; optional resolved SetId and LookupCode qualifiers | Match ExpensePoolCode after trimming and case-insensitive normalization. When supplied, require SetId and LookupCode to agree with the same candidate. Require exactly one candidate; qualifiers constrain identity only and are not delete source fields. | Verified ExpensePoolCode for delete source; sanitized candidate-count evidence | No candidate: reject and ask for a valid ExpensePoolCode. Multiple candidates: ask for SetName or ExpensePoolTypeCode. Qualifier mismatch: reject and identify the conflicting qualifier. Never select the first candidate. |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_expense_pool_type | Create, DELETE, or PATCH when ExpensePoolTypeCode is supplied | One trimmed ExpensePoolTypeCode input treated as a meaning | GET {restBaseUrl}/fscmRestApi/resources/latest/standardLookupsLOV?finder=LookupTypeFinder;LookupType=ORA_CST_EXPENSE_POOL_TYPES | LookupCode, Meaning, hasMore | Retrieve every page for the fixed lookup type. Compare the input and each returned Meaning after trimming and case-insensitive normalization. Require exactly one exact Meaning match and use its LookupCode. | ExpensePoolTypeCode from LookupCode | No exact match: return all allowed Meaning values from the complete paginated result. More than one exact match: reject as ambiguous and ask for a more precise meaning. Authentication, authorization, transport, or response-shape failures stop the workflow. Never select the first result. |
| resolve_reference_set | Create or DELETE when SetName is supplied | One trimmed SetName input; SetId and SetCode are never user input | GET {restBaseUrl}/fscmRestApi/resources/latest/setIdSets?q=UPPER(SetName) like UPPER('%&lt;URL-encoded value&gt;%') with request header REST-Framework-Version: 9 | SetId, SetName, hasMore | Use the verified case-insensitive SetName candidate query. Require exactly one returned record whose SetName matches the input after trimming and case-insensitive normalization before using its SetId. The set is immutable after Create and SetName is not resolved for PATCH. | SetId from SetId; SetName | No candidate: reject and ask for a valid set. More than one candidate or a failed local normalized verification: reject as ambiguous and ask for a more precise set name. Authentication, authorization, transport, or response-shape failures stop the workflow. Never select the first result. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Operation scope | All resolvers are read-only. The local resolver uses only the approved task-export baseline; live resolvers may only call the documented standardLookupsLOV or setIdSets endpoint. They must not create, update, delete, upload, or initiate setup data. |
| Core delegation | `resolve_expense_pool_type` and `resolve_reference_set` invoke `core.fusion-api.rest-api-client` only, using the active approved Fusion environment and read-only GET requests. The pillar skill retains resolver inputs, matching, and stop conditions; the core client owns REST transport, authentication, retry, response redaction, and diagnostics. |
| Environment identity | Join each relative request path to the active, approved Fusion restBaseUrl. Do not allow the lookup contract to supply or override a host. |
| Set lookup header | Send REST-Framework-Version: 9 only with the setIdSets request. Do not add this header to the standardLookupsLOV expense-type request. |
| Result handling | URL-encode user input when constructing a query. For set resolution, use the verified case-insensitive SetName candidate query; do not broaden it to an unbounded set-list request. Retain only documented fields. For expense types, retrieve every page for the fixed lookup type before resolving a Meaning or returning allowed meanings. Do not substitute partial values or select a first result. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| OEP.RESOLVE_EXPENSE_POOL_TYPE | decision | 4 | reference_lookup | resolved->OEP.RESOLVE_REFERENCE_SET;not_applicable->OEP.RESOLVE_REFERENCE_SET;blocked->OEP.HANDLE_ISSUE;failure->OEP.HANDLE_ISSUE | OEP.RESOLVE_DEPENDENCIES | stop | Create, DELETE, or PATCH when ExpensePoolTypeCode is supplied; otherwise not_applicable |
| OEP.RESOLVE_REFERENCE_SET | decision | 5 | reference_lookup | resolved->OEP.RESOLVE_DELETE_TARGET;not_applicable->OEP.RESOLVE_DELETE_TARGET;blocked->OEP.HANDLE_ISSUE;failure->OEP.HANDLE_ISSUE | OEP.RESOLVE_EXPENSE_POOL_TYPE | stop | Create or DELETE when SetName is supplied; otherwise not_applicable |
| OEP.RESOLVE_DELETE_TARGET | decision | 6 | reference_lookup | resolved->OEP.ENFORCE_PAYLOAD;not_applicable->OEP.ENFORCE_PAYLOAD;blocked->OEP.HANDLE_ISSUE;failure->OEP.HANDLE_ISSUE | OEP.RESOLVE_REFERENCE_SET | stop | DELETE; otherwise not_applicable |
