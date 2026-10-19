# External Purchase Prices Requisitioning BU Mapping Design Enforcement

## Source Anchors

| Source | Scope Used |
|---|---|
| [Oracle Procurement 26C — How do I create mappings?](https://docs.oracle.com/en/cloud/saas/procurement/26c/faepp/how-do-i-create-mappings.html) | Source organization, procurement BU and associated requisitioning BU grouping; this setup guide is not the REST interface contract |
| [Oracle Procurement 26C — Prerequisites for External Purchase Prices](https://docs.oracle.com/en/cloud/saas/procurement/26c/faepp/what-are-the-prerequisites-for-setting-up-oracle-external-purchase-prices.html) | Procurement/BPA readiness and Purchase Pricing Manager-equivalent access, applied by [Dependency Rules](ora_dependency_readiness.md#dependency-rules) |
| [FSCR Design Rules](#design-rules), [Field Validation](ora_input_validation.md#field-validation) and [Standard Defaults](ora_defaulting_rules.md#standard-defaults) | Existing FSCR preflight policy: one active source per requisitioning BU, exact identity, optional IDs, operation applicability and false/omitted-value handling; these safeguards are not presented as additional Oracle API requirements |
| [EPPBU-LOOKUP-1.2](ora_reference_lookups.md#lookup-contract-v1) | Versioned, sanitized reference for the existing parent/child read contract and direct-GET routing; runtime evidence must come from the current authorized lookup, not a historical response |

The exact Oracle links above were recovered from existing reviewed source
material; the pinned 26C edition was not refreshed in this routing change.
No new documentation lookup or Fusion request was performed. The unavailable
internal Confluence links are not authority. The reviewed loader request defines
intended operations; it never proves existing Fusion state. Product guidance,
FSCR preflight policy and current-run lookup evidence have the distinct scopes
listed above.

## Enforcement Order

This sequence applies to mutation validation. Pure reads return through the
direct REST read branch before this node; they do not need mutation design approval.

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Readiness gate | Confirm the existing Procurement/BPA and access prerequisites |
| 2 | Identity gate | Require an unambiguous lookup result for an existing target; names are accepted without requiring numeric IDs |
| 3 | Proposed state | Start with complete existing membership for updates; apply only the requested additions and removals. Preserve omitted children. Use the explicit activation value, a new-parent default, or the existing activation state, as applicable |
| 4 | Exclusivity gate | Evaluate each retained or added candidate in a proposed active mapping against complete lookup evidence and other active proposals in the same reviewed artifact |
| 5 | Scope and handoff | Keep this task limited to source/procurement/requisitioning BU mappings; core.data-loader owns the artifact, approval and mutation lifecycle |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Parent POST | Error | resolve_existing_bu_mapping | The exact natural-key parent already exists | Use a separately reviewed update; do not reinterpret or replay a create | No |
| Parent PATCH or DELETE; child operation under an existing parent | Error | resolve_existing_bu_mapping | Existing target is missing, ambiguous or inconsistent with supplied IDs/names; child DELETE target is absent | Correct the exact target or reconcile the earlier result; never use the first row | No |
| Proposed active parent POST, child addition to an active parent, or reactivation | Error | find_active_requisitioning_bu_mapping | A retained or added requisitioning BU has another active source organization outside the exact current MappingId, or the same artifact proposes that BU under two active source organizations | Reuse, amend or retire the conflicting mapping through a separately approved change; do not auto-fix the competing record | No |
| Same-parent update | Error | resolve_existing_bu_mapping | The request adds a child that already exists or supplies contradictory operations for one child | Do not replay a POST; select the intended operation. A current active membership alone is not an exclusivity conflict | No |
| Membership removal only; parent DELETE; explicit deactivation | Information | resolve_existing_bu_mapping | No active-addition exclusivity check applies to the removed or deactivated membership | Record exclusivity as not applicable with the operation reason, not passed. Exact identity, other loader validations and mutation approval still apply | No |
| Name-only candidate | Error | find_active_requisitioning_bu_mapping | Required active-membership evidence was skipped only because RequisitioningBUId was omitted, or the name is ambiguous | Keep IDs optional and apply the same exact-name membership check; unresolved evidence blocks preview | No |
| Applicable conflict validation | Error | find_active_requisitioning_bu_mapping | Visibility, pagination, identity or active state is incomplete | Stop before preview; do not claim zero conflicts or infer an unmapped BU's eligibility | No |
| Pure read-only request | Information | resolve_existing_bu_mapping | Mutation design gates are not applicable | Use direct core REST GET and RETURN_READ_RESULT for complete records or not-found; do not enter Data Loader, default, prepare a load, request mutation approval or write | No |
| Mapping design | Warning |  | Source-system values already match Oracle Procurement values | Retain the existing guidance to create mappings only when external attribute values differ | No |
| Group mapping design | Warning |  | Proposed BUs should not share resulting BPA access | Group only requisitioning BUs intended to share that access | No |

A lookup may return many membership rows for one BU. A repeated row in the
current parent is not automatically a conflict; two distinct BU IDs for a
name-only candidate are ambiguous. Another mapping under the same source does
not by itself violate the existing one-active-source rule, but its identity and
all other domain validations still require evaluation.

For activation of an existing parent, the candidate set includes every retained
current child, not just newly supplied child rows. For an inactive proposed
parent, record the exclusivity gate as not applicable; do not claim other
eligibility or Fusion business validations have passed.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_existing_bu_mapping | Existing-target operations, create duplicate checks and requested record reads | Exact parent match count, current activation, complete children and supplied-key agreement | ora_reference_lookups.md |
| find_active_requisitioning_bu_mapping | Proposed active membership, with child names or IDs | Complete conflict membership evidence, exact current-parent exclusion, ambiguity and visibility outcome | ora_reference_lookups.md |

## Golden Scenarios

All fixture labels below are synthetic; these are preflight expectations, not
Oracle service calls or approved payloads.

| Scenario | Requested Change and Evidence | Expected Result |
|---|---|---|
| parent-post-clear | New parent; complete lookup finds no active conflicting membership for named child | Conflict gate passes; only the loader approval workflow may execute |
| parent-post-duplicate | Parent POST natural keys already match an existing parent | Block duplicate create |
| patch-same-parent | Update exact parent P1; child's only active membership is P1 | Exclude P1; do not block merely because it is already active |
| child-post-conflict | Child POST by name; another active source owns that BU | Block before preview |
| child-post-clear | Child POST by name under an active parent; complete evidence has no other active source | Conflict gate passes; child ID need not be supplied |
| child-post-inactive-parent | Child POST under a parent remaining inactive | Exclusivity not applicable; retain identity, eligibility and loader checks |
| child-delete-existing | Delete one exact current child, no additions or activation | Resolve the child; exclusivity not applicable to the removed member |
| child-delete-missing | Delete a child not present under the resolved parent | Block missing target; do not replay deletion |
| mixed-child-change | Delete Fixture BU Alpha and add Fixture BU Beta under an active parent | Remove Alpha from candidates; check Beta and retained members; preserve omitted children |
| parent-delete | Delete the exact parent; no conflicting child operations | Exclusivity not applicable; preserve approval/destructive-scope checks |
| explicit-deactivation | Parent PATCH ActivationFlag=false | Preserve false; exclusivity not applicable; no approval bypass |
| reactivation-retained-conflict | Parent PATCH false to true; retained child has another active source | Block even if no child POST row is supplied |
| later-page-conflict | Conflict appears only on a later parent or child page | Block after complete enumeration, never pass from page one |
| pending-proposal-conflict | Same reviewed artifact assigns one BU to two proposed active sources | Block the conflicting proposals before preview |
| read-only | Retrieve an existing parent and its children | Return records only; no mutation defaults or execution |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPBU.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->EPPBU.READY_FOR_DATA_LOADER_REST;blocked->EPPBU.HANDLE_ERROR | EPPBU.APPLY_DEFAULTS | stop | Evaluate only applicable business policy from lookup evidence before core.data-loader handoff; record not-applicable reasons |
