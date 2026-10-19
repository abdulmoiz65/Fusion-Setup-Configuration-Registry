# External Purchase Prices Requisitioning BU Mapping Reference Lookups

## Source Boundary

Use the [lookup contract v1](#lookup-contract-v1) and the
[source anchors](ora_design_enforcement.md#source-anchors), not conversation
history, as the reusable references. No new endpoint, BU list-of-values service,
SQL lookup, compound filter syntax, or write is introduced here. The reviewed
loader input supplies requested mutation operations and values; a record-read
request supplies lookup keys without a loader file. Fusion supplies existing
mapping state. This resource owns lookup mechanics, not business-policy
decisions or Data Loader serialization.

## Lookup Contract v1

Contract ID: EPPBU-LOOKUP-1.2; recorded 2026-09-24 in skill version 0.2.1.
This sanitized contract preserves the paths, fields and lookup rules already
authored in skill version 0.1.0; it is not a captured Fusion response or evidence
of a new live verification. Historical GET/Describe response bodies are not
retained in this reusable package and must not be assumed available or current.
Version 1.1 implements the user's direct-GET / loader-only-writes routing
requirement; it does not change the existing REST paths or response fields.
Version 1.2 makes the observed framework-v9 `@context.links` location explicit,
using the existing sanitized read receipt reviewed in EPPBU-MIN-001. The example
below is synthetic, not a retained response or a new live verification.

| Contract Part | Authoritative Reference | Evidence Boundary |
|---|---|---|
| Parent and child read interface | [Live Lookups](#live-lookups) | Pinned API version 11.13.18.05 and exact field spellings; no new interface inferred from public setup guidance |
| Identity, pagination, security and read limits | [Lookup Execution Rules](#lookup-execution-rules) | Current-run complete evidence is required; a contract version is not proof of environment access or record state |
| Expected outcomes | [Golden Scenarios](#golden-scenarios) | Synthetic expectations, not live Oracle test results |
| Execution owner | [Core REST API Client](../../../../../../core/fusion-api/rest-api-client/SKILL.md) | Direct GET after the read-only workflow or mutation-validation preflight; record reads do not invoke Data Loader |

If the selected environment cannot supply this contract's required fields,
linkage or pagination evidence, apply the existing incomplete-lookup stop rules.
Refresh a changed interface only through a separately selected documentation or
read-only validation workflow; do not invent replacement fields or services.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_existing_bu_mapping | Before evaluating parent or child writes; also for an explicitly requested record read | SourceOrganization and ProcurementBUName or ProcurementBUId; MappingId when supplied; child names or IDs when supplied | GET /fscmRestApi/resources/11.13.18.05/externalPurchasePricesBusinessUnits, then the returned requisitioningBusinessUnits child link for the exact parent | Parent: MappingId, SourceOrganization, ProcurementBUName, ProcurementBUId, RequisitioningBUGroupId, ActivationFlag, LastUpdateDate, context links; child: RequistioningBUMappingId, RequisitioningBUName, RequisitioningBUId, RequisitioningBUGroupId; collection: items, count, hasMore, limit, offset, links | Apply the complete-page and exact-identity rules below; all supplied parent keys must agree with one record | Current parent identity, activation state and complete current child membership, or explicit parent-not-found | Zero is a valid lookup result for a new parent POST or a record read; it is a missing target for an existing-parent operation. More than one exact parent or inconsistent supplied keys blocks |
| find_active_requisitioning_bu_mapping | Before an operation that would create or retain candidate membership in an active mapping, including name-only child POST and parent reactivation; never only because an ID was supplied | Candidate RequisitioningBUName and/or RequisitioningBUId, resolved current MappingId if any, requested SourceOrganization and effective parent state | GET /fscmRestApi/resources/11.13.18.05/externalPurchasePricesBusinessUnits, then each relevant parent's returned requisitioningBusinessUnits child link | Parent: MappingId, SourceOrganization, ProcurementBUName, ProcurementBUId, ActivationFlag, context links; child: RequistioningBUMappingId, RequisitioningBUName, RequisitioningBUId, RequisitioningBUGroupId; collection: items, count, hasMore, limit, offset, links | Enumerate all visible parents and complete memberships of active parents without filtering to the requested source or procurement BU; match supplied child IDs or exact child names and retain all matches | Complete matching membership evidence, distinct matched BU IDs, other active source organizations, completeness and visibility result | Zero means no conflicting membership was observed in the confirmed complete security scope, not that the BU exists or is eligible. Ambiguous identity or incomplete visibility blocks; multiple membership rows are evidence for design evaluation, never select the first |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Execution owner | Use only core/fusion-api/rest-api-client/scripts/fusion_rest_client.py with GET and REST-Framework-Version=9. The task's Read-Only Mapping Workflow selects this client directly for record retrieval, without core.data-loader, Task Hook, template generation or loader initialization. Mutation validation also uses this client for GET evidence; all writes remain exclusively with core.data-loader |
| Before the first GET | The selected workflow must have confirmed the exact environment, task/catalog, identity, required read privileges and safe input/evidence scope. Apply the read bounds and visibility rules before enumeration. Pure reads require no loader file, mutation approval, write privilege or Procurement/BPA maintenance readiness. Missing read preflight evidence blocks; later dependency-node evaluation is not permission to skip it |
| Lookup order | Resolve the exact existing parent and its current membership first. Pure reads run resolve_existing_bu_mapping only; evaluate whether find_active_requisitioning_bu_mapping applies only for mutation validation. Reuse only fully read pages from the same run; do not reuse a prior run's receipts |
| Parent collection request | Use the confirmed parent collection path with limit=100 and offset=0, without q, expand, fields, or onlyData overrides. Compare identities in the returned items. An unfiltered scan avoids relying on undocumented compound-filter syntax or the parent display-summary field |
| Framework-v9 record links | For REST-Framework-Version=9, read each selected parent item's @context.links array. Select its returned rel=canonical link and the rel=child link whose name is requisitioningBusinessUnits; require one unambiguous link for each role. Do not assume record links are in item.links or use collection-level links as the parent's links. Missing, malformed or ambiguous required context links makes the lookup incomplete; do not construct a replacement URL from MappingId or RequisitioningBUGroupId |
| Complete parent pagination | Continue while hasMore is true using a validated same-environment next link, or offset plus the positive returned limit on the same collection. Require a consistent nonnegative offset, items array, boolean hasMore and forward progress; stop only at hasMore=false. An empty page with hasMore=true, repeated page/key, changing identity, missing pagination metadata, timeout, or failed page makes the result incomplete, not empty |
| Child collection request | Read each relevant parent's returned child link named requisitioningBusinessUnits. Accept links only in the selected environment and under the exact returned parent canonical resource; never use RequisitioningBUGroupId as the parent URL key. Do not treat the parent's RequisitioningBUName display summary as a member list |
| Complete child pagination | Apply the same limit=100, offset=0 and complete-page rules independently to every child collection. Parent hasMore=false does not prove child completeness. Compare each child's RequisitioningBUGroupId with its parent's group ID; inconsistent or missing linkage blocks |
| Read bounds | Honor the shared client's configured timeout and the selected read or validation run's finite read budget. Set a finite bound before enumeration; if absent, exhausted or interrupted, stop as incomplete and preserve sanitized next-check evidence. Never turn a partial scan into not-found or a no-conflict result |
| Visibility | Confirm read security scope for the requested parent and relevant children before record retrieval. If that scope is unconfirmed, report read-inconclusive rather than not-found. Mutation exclusivity requires visibility across all relevant procurement/requisitioning BUs, not just the requested parent; restricted conflict coverage is conflict-check-inconclusive and blocks preview. Do not infer global absence from accessible rows |
| Parent identity | Match SourceOrganization exactly and match ProcurementBUName or ProcurementBUId exactly. If both BU name and ID are supplied they must agree on the same row. If MappingId is supplied it must also agree. Do not use case folding, fuzzy matching, first-row selection, or group ID as a substitute for MappingId |
| Child identity with an ID | Match RequisitioningBUId exactly. If a name is also supplied require both to agree on the same child identity; a name observed with a different ID is not a silent match. Validate a supplied RequistioningBUMappingId against the exact current-parent child |
| Child identity with only a name | Match RequisitioningBUName exactly across complete relevant memberships. A name resolving to multiple distinct RequisitioningBUId values blocks as ambiguous. Multiple rows for the same BU ID are memberships to evaluate, not duplicate identities |
| Current-record exclusion | Only after exact target resolution, identify the current parent by MappingId. Exclude only that MappingId from other-parent conflict evidence. Do not exclude all rows with the requested source or procurement BU, and do not exclude a record merely because its group ID matches |
| Active-state evidence | Use the returned boolean ActivationFlag, not Status text or a default assumed for an existing record. Missing or indeterminate activation on a relevant record prevents a complete conflict result |
| Candidate membership | Pass the current child set and requested child operations to design enforcement. For parent activation, include retained children as well as additions. For a child DELETE, resolve the exact existing child but do not check that removed member as an active addition |
| Request consistency | Reject conflicting ID/name pairs, duplicate exact parents, contradictory operations on the same child, or a parent DELETE mixed with child POST/PATCH under it. Preserve original input values; lookup-only IDs must not silently rewrite the reviewed loader artifact |
| Zero versus missing | Zero active-membership matches supports conflict-check candidacy. Zero target matches for PATCH or DELETE is a missing target. A read-only request returns not-found without making a write. Never confuse these outcomes |
| Eligibility boundary | Mapping scans do not prove that an unmapped BU exists, is enabled, or belongs to the procurement BU. Do not claim those validations passed; retain the established Fusion/loader reference validation boundary and stop if a selected workflow requires unsupported eligibility evidence |
| Receipt | Keep normalized identities and IDs only in transient evaluation state. Persist sanitized resolver names, page/member counts, completion flags, lookup time, outcome and evidence references; do not persist raw response bodies, unrelated BU records, opaque links, tokens or ETags |
| Read-only requests | Return only the requested current parent and child details through the direct GET route. Mutation defaults, dependency/design gates, approval, upload and initiation are not applicable; do not enter Data Loader even if no matching record exists |
| Node outcome | Select read_complete only when intent is pure record retrieval and exact-parent/child evidence is complete, including confirmed not-found. Select resolved for successful mutation-validation lookups and continue the existing loader gates. Select blocked or failure for incomplete, ambiguous or failed reads; never use read_complete to bypass a requested mutation's validation |

## Synthetic Framework-v9 Link Example

This minimal parent collection illustrates link selection only. The reserved
host, names, IDs and resource key are synthetic. It is not a request template
or permission to contact that host. Collection-level `links` describe the
collection; the exact parent item's `@context.links` supplies its canonical and
child links. The canonical resource key is deliberately not either numeric ID.

```json
{
  "items": [
    {
      "MappingId": 101,
      "SourceOrganization": "Fixture Source Alpha",
      "ProcurementBUName": "Fixture Procurement BU",
      "ProcurementBUId": 201,
      "RequisitioningBUGroupId": 301,
      "ActivationFlag": true,
      "@context": {
        "links": [
          {
            "rel": "canonical",
            "href": "https://fusion.example.invalid/fscmRestApi/resources/11.13.18.05/externalPurchasePricesBusinessUnits/fixture-parent-key"
          },
          {
            "rel": "child",
            "name": "requisitioningBusinessUnits",
            "href": "https://fusion.example.invalid/fscmRestApi/resources/11.13.18.05/externalPurchasePricesBusinessUnits/fixture-parent-key/child/requisitioningBusinessUnits"
          }
        ]
      }
    }
  ],
  "count": 1,
  "hasMore": false,
  "limit": 100,
  "offset": 0,
  "links": [
    {
      "rel": "self",
      "href": "https://fusion.example.invalid/fscmRestApi/resources/11.13.18.05/externalPurchasePricesBusinessUnits"
    }
  ]
}
```

After exact parent matching, select the two href values from that item's
`@context.links`, then verify the selected environment and exact-parent child
scope before following the child link. Parent `hasMore=false` does not complete
the read: child pagination and group-linkage checks still apply. If the required
links are absent, conflict, point outside the selected environment or identify
another parent, stop as incomplete; do not substitute collection links, guess
a URL, or fall back to Data Loader.

## Golden Scenarios

All names and IDs below are synthetic fixture labels, not an environment payload.
These expected results cover lookup evidence; the design resource owns acceptance.

| Scenario | Input and Observed Pages | Expected Result |
|---|---|---|
| exact-existing-parent | One parent matches all supplied natural keys and optional ID; child pages complete | Resolve one current MappingId and complete children |
| framework-v9-context-links | Synthetic example above: exact parent has canonical and named child links only in @context.links; collection links describe only the collection | Select the returned parent canonical and requisitioningBusinessUnits child hrefs, validate same environment and exact-parent scope, then enumerate children; do not require item.links or substitute numeric IDs into the URL |
| required-context-link-missing | Exact parent lacks a required @context.links role, even if collection links are present | Block: incomplete lookup; no invented URL, diagnostic retry to guess the envelope or loader fallback |
| context-link-scope-mismatch | Returned child href points to another environment or another parent's canonical resource | Block before following the link; no first-link selection or URL repair |
| context-link-ambiguous | Exact parent's @context.links has multiple canonical or named requisitioningBusinessUnits child candidates | Block: ambiguous link evidence; never pick the first candidate |
| parent-missing-update | Parent PATCH; zero exact parents after complete enumeration | Block: missing existing target |
| parent-ambiguous | Two distinct parents match the same natural keys | Block: ambiguous parent, never first row |
| parent-key-disagreement | Supplied MappingId selects a different parent from the supplied natural keys | Block: inconsistent supplied keys |
| name-only-no-match | Candidate Fixture BU Alpha; complete active memberships contain no exact name | Complete with zero observed conflict matches; no claim of BU existence or eligibility |
| name-only-ambiguous | Fixture BU Alpha appears with distinct BU IDs 101 and 202 | Block: ambiguous child identity |
| id-name-disagreement | Candidate ID 101 and name Fixture BU Alpha disagree in returned membership | Block: inconsistent child identity |
| conflict-on-parent-page-two | First parent page hasMore=true; matching membership exists on page two | Return the later match; do not stop after the first page |
| conflict-on-child-page-two | Parent list complete; relevant child's first page hasMore=true; match on page two | Return the later child match |
| incomplete-child-page | A relevant child page fails or is missing hasMore | Block: incomplete lookup, not zero matches |
| repeated-page | A page does not advance or repeats a previously read record key | Block: incomplete or changing result |
| restricted-visibility | Caller can inspect only an unconfirmed subset of relevant BUs | Block: conflict-check-inconclusive |
| read-not-found | Explicit read-only request; no exact parent after a complete authorized read | read_complete to RETURN_READ_RESULT with not-found; no Data Loader |
| read-without-loader-file | Explicit read request with exact natural keys and read preflight complete; no XLSX or mutation approval | Direct core REST GET; complete parent/children via read_complete; no loader, dependency/default/design checks or active-membership scan |
| read-incomplete | Explicit read request; one required child page fails | failure or blocked to RETURN_ISSUES; no read_complete, no loader fallback |
| mutation-lookup-complete | A requested mutation's applicable GET evidence is complete | resolved to CHECK_DEPENDENCIES; never return read_complete for the mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| EPPBU.RESOLVE_REFERENCES | step | 20 | reference_lookup | read_complete->EPPBU.RETURN_READ_RESULT;resolved->EPPBU.CHECK_DEPENDENCIES;blocked->EPPBU.HANDLE_ERROR;failure->EPPBU.HANDLE_ERROR | EPPBU.VALIDATE_INPUT | stop | Direct GET after preflight; pure complete reads select read_complete, mutation-validation evidence selects resolved; record not-applicable reasons explicitly |
