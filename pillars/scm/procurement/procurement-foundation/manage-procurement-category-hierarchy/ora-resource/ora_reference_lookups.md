# Supplied FSM Reference Evidence

Task: POR_MANAGE_AGENT_ASSIGNMENTS_CATEGORY_HIERARCHY. Expected TYPE: SOURCING. FSM CSV only; execution remains with the generated skill’s routed export, validation, and core.data-loader services. These resources perform local preparation and evidence assessment; they declare no product REST operation.

Source: user-approved rules derived from reviewed native FSM exports and import receipts (September 2026). Preventive safeguards below are authoring policy, not claims of tested Oracle rejection behavior.

Successful FSM tests cover synthetic browsing-category creation and parent–child relationships with PurchasingCatFlag N. Agent assignments and purchasing-category eligibility were not tested; the task code does not establish coverage of those operations.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| inspect_target_hierarchy_export | Preparing a relationship and assessing available target evidence | User-supplied or routed-workflow-supplied target FSM export, environment identity, export process/time/scope, intended parent and child identity | Use only evidence attributed to the intended target and task; compare exact strings and TYPE; browse identities use category name and TYPE, purchasing relationships additionally compare any supplied CategoryCode; retain all observed parent relationships | Evidence status, provenance, matching rows and observed parents only; never populate or rewrite CategoryCode, CategoryName or an internal ID | Missing export, scope, freshness or identity yields unverified evidence; no row means not observed in this snapshot, not nonexistent; conflicting identity matches yield ambiguous evidence requiring reconciliation |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Local evidence evaluation | Read only the supplied artifact; return evidence status even if it is unverified. This is evaluate_result on the local route, not a live reference_lookup action |
| Target evidence is absent or outdated | Disclose limits and retain the original request for routed FSM validation; do not claim live reference validation or launch an exploratory lookup |
| Purchasing category missing from hierarchy export | An unassigned item can be absent; the snapshot is not a complete item-master or eligibility source |
| Source and target have equal names but different codes | Return a discrepancy for explicit reconciliation; do not assume equivalence, code-first matching, name-first matching or a portable internal CategoryId |
| Internal FSM identity resolution | Matching precedence and purchasing eligibility are unverified; defer acceptance to the declared FSM process without inventing a REST endpoint or automatic mapping |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PCH.EVIDENCE | step | 20 | evaluate_result | assessed->PCH.DEPENDENCIES;error->RETURN_ISSUES | PCH.INPUT | stop | Assessing supplied target evidence, including an explicit unverified outcome |
