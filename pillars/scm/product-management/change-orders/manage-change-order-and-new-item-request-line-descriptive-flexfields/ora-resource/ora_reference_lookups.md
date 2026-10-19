# Change Line DFF Reference Lookups

Retrieve allowed change-type values through the resolver below. Membership and operation applicability are owned by ora_design_enforcement.md; retrieval establishes the allowed set, not DFF setup readiness.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_change_type_internal_name | Explicitly listing or checking allowed Context Code values, creating or updating Contexts, or creating or updating Context Sensitive Segments; excludes enabled-state-only disable | Confirmed target environment; requested Context Codes, including a selected existing Context resolved from the verified baseline. Do not add unrelated preserved Contexts to the membership-check scope | /fscmRestApi/resources/11.13.18.05/productChangeTypes | InternalName | Collect the distinct nonempty InternalName strings from the complete collection; preserve spelling and case; do not substitute a display name or another identifier | allowed_context_codes from InternalName; context_lookup_complete only after successful retrieval of every page | A complete empty collection yields an empty allowed set; multiple values are expected and repeated identical values are deduplicated; incomplete or malformed retrieval returns unverified, not an invalid-code result |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Context validation lookup is reached by the authorized workflow | Use a read-only GET through core.fusion-api.rest-api-client with the confirmed target environment; this resource supplies no authentication or transport implementation. A standalone allowed-value check does not require creating a runbook or exporting unrelated DFF setup; preserve shared access and authorization gates |
| The collection is paginated | Follow its supported pagination until complete before producing allowed_context_codes; a first-page miss is not evidence that a code is invalid |
| Pagination cannot be completed, access is denied, the request fails, or InternalName data is malformed | Stop with an unverified lookup and safe diagnostics; do not accept the code, treat the failure as an empty allowed set, or create a change type |
| No resolver is applicable to the requested operation | Record why the lookup is not applicable; do not mark an unperformed lookup complete |
| Attempting to use productChangeTypes for flexfield metadata | Do not use it to infer a DFF application ID, segment columns, existing contexts or deployment status; it establishes the allowed Context Code values only |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLDFF.LOOKUPS | step | 20 | reference_lookup | success->CLDFF.DEPENDENCIES;failure->CLDFF.RETURN_ISSUES | CLDFF.INPUT | stop | Evaluate the applicable lookup rows for the requested configuration |
