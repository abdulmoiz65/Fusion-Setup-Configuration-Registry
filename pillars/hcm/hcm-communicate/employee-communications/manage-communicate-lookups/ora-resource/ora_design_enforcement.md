# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Establish the business outcome | Identify the affected HCM Communicate process or audience, timing, and desired policy or terminology change. |
| 2 | Prove task ownership | Match the exact requested or returned LookupType to one approved prefix before detailed reads or mutations. |
| 3 | Resolve current identity | Freshly read the exact parent and, when applicable, exact code; prove the requested create identifier is absent. |
| 4 | Establish field support | Use only mutability and protection behavior explicitly documented in current Common Lookups response metadata. |
| 5 | Preserve configuration | Retain type/code identity, ownership basis, seed identity when available, protected fields, and all unrequested values. |
| 6 | Bind approval | Present an immutable business-first minimal-change preview and obtain explicit approval immediately before one mutation. |
| 7 | Verify | Freshly read the exact affected type or code after the delegated action and persist sanitized evidence. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every exact request | Blocker | classify_communicate_lookup_type | LookupType matches none of ORA_IRC or ORA_HCO | Report the ownership-mapping gap and require refreshed approved evidence | No |
| Complete type listing | Blocker | list_communicate_common_lookup_types | Collection completeness is not established or non-owned types remain after filtering | Complete the provider read, de-duplicate, and apply the prefix baseline to every result | Yes |
| Parent create | Blocker | resolve_communicate_common_lookup_type | Proposed LookupType does not pass ownership, already exists, or exact absence is uncertain | Correct the identity or establish exact absence through Common Lookups | Yes |
| Parent update or delete | Blocker | resolve_communicate_common_lookup_type | Exact current parent is absent, ambiguous, stale, or outside the ownership baseline | Refresh one exact current parent read | Yes |
| Code create | Blocker | resolve_communicate_lookup_code | Exact parent is not current and owned, or the proposed LookupCode exists or absence is uncertain | Refresh the parent and code list and resolve the collision | Yes |
| Code update or delete | Blocker | resolve_communicate_lookup_code | Exact current code was not freshly read under the exact owned parent | Resolve one exact current code through the provider | Yes |
| Create or update | Blocker | | Current documented response metadata does not establish every requested field as mutable | Limit the delta to fields explicitly supported by current metadata | Yes |
| Update or delete | Blocker | | LookupType, LookupCode, ownership basis, seed identity, protected fields, or unrequested values would change | Restore every protected and unrequested value and retain only the approved delta | Yes |
| Translation | Blocker | read_lookup_code_translations | A translation create, update, or delete is requested | Return translations as read-only information | No |
| Comparable configuration | Blocker | classify_communicate_lookup_type | A comparison is used as execution authority instead of fresh target state | Use comparison only to inform the proposal and validate the target independently | Yes |
| Mutation preview | Blocker | | Target environment, exact parent/code identity, current state, requested delta, business impact, unchanged configuration, verification read, or approval fingerprint is missing | Regenerate the immutable minimal-change preview | Yes |
| Explicit CSV export or import | Blocker | | Export is not explicitly requested and catalog-supported, or import is not an explicitly requested validated and approved FSM CSV package | Use the catalog route only for the explicit bulk request | Yes |
| Unsupported transport or capability | Blocker | | Direct REST, curl, OAuth handling, browser automation, FSM, or export/import would bypass the Common Lookups contract | Explain the limitation and stop | No |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| classify_communicate_lookup_type | Every requested or returned type | Owned decision, matched prefix, and evidence version | ora_reference_lookups.md |
| list_communicate_common_lookup_types | Complete inventory | Complete eligible type set and returned response fields | ora_reference_lookups.md |
| resolve_communicate_common_lookup_type | Exact type read or parent mutation | Current or absent parent identity, supported fields, and protection evidence | ora_reference_lookups.md |
| resolve_communicate_lookup_code | Code read or mutation | Current or absent code identity, supported fields, protection evidence, and preserved state | ora_reference_lookups.md |
| read_lookup_code_translations | Translation read | Exact parent/code binding and read-only translations | ora_reference_lookups.md |

## Immutable Preview Contract

| Preview Element | Required Content |
|---|---|
| Business summary | Desired HCM Communicate outcome, affected process or audience, timing, assumptions, and impact. |
| Target | Exact environment, owned LookupType, and LookupCode when applicable. |
| Current state | Fresh exact provider response or verified create absence; include only actually returned fields. |
| Requested delta | Only the approved field-level create, update, or delete action. |
| Unchanged configuration | Identity, ownership basis, seed identity when available, protected fields, and all unrequested values. |
| Verification | Exact post-action type or code read, or verified exact-resource absence after delete. |
| Approval fingerprint | Immutable target, current-state receipt, minimal payload or delete target, impact, and verification plan. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CCL.ENFORCE | decision | 6 | design_enforcement | create->CCL.PREVIEW;update->CCL.PREVIEW;delete->CCL.PREVIEW;blocked->CCL.DESIGN_ISSUES | none | stop | An owned parent or code mutation has current or absence evidence |
