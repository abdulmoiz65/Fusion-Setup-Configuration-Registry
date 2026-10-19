# Service Provider Prerequisite Lookups

## Creation-Only Reference

The prior creation-only draft used `confirm_request_scope` for its one-provider
request boundary and `confirm_runbook_provider_input` for customer-confirmed
Runbook values and explicit B2B-adapter applicability. Neither performed a
Fusion lookup; unknown adapter use required clarification, and documentation
examples were not customer values. These historical names are not runtime
aliases or prerequisites for the current FSM import graph. An unchanged
exported package is not restricted to a one-provider creation request.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_cmksp_b2b_document_setup_enabled | Automatically before the Service Providers export process is created, or during import preapproval Task Hook validation; do not ask the user to check the feature | Configured host for the source export or destination import; exact code `ORA_CMK_B2B_DOCUMENT_SETUP` | Route through `core.fusion-api.rest-api-client` using its `references/fusion-rest-api.md` and `scripts/fusion_rest_client.py`; GET `/fscmRestApi/resources/11.13.18.05/features` with `q=FeatureCode='ORA_CMK_B2B_DOCUMENT_SETUP'`, `fields=FeatureCode,FeatureType,EnabledFlag`, and `onlyData=true` | `FeatureCode,FeatureType,EnabledFlag` | Exactly one same-target item with exact FeatureCode, `FeatureType: FEATURE`, and `EnabledFlag: Y`; do not infer enabled from `checkedFlag` or a catalog snapshot | Redacted host, exact code, enabled flag, read time; confirm the query returns this combination feature in the qualified release | Stop if absent, disabled, unauthorized, malformed, cross-environment, or ambiguous; do not create an export process or upload/import |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A Service Providers export or import is requested | Invoke `verify_cmksp_b2b_document_setup_enabled` automatically for the exact operation host. A feature-state lookup is read-only and needs no user confirmation. Continue only after the result is `EnabledFlag: Y`; never ask the user whether the feature is enabled. |
| The filtered Features collection has not been validated for this code on the selected pod | Keep the operation blocked; public API documentation supplies the generic read contract but does not prove this code is returned on every pod. The read was verified on FSCR_CDRM on 2026-10-01 |
| The feature response is not a fresh exact-code `EnabledFlag: Y` from the operation's host | Stop before the first export POST or import upload; recheck after a separate opt-in action |
| Access is insufficient | Request authorized access; do not assign roles or submit an import to test permissions |
| A creation-only rule is encountered during FSM import | Do not apply it; package validation remains owned by ora_input_validation.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CMKSP.RESOLVE_PREREQUISITES | decision | 15 | reference_lookup | verified->CMKSP.CHECK_DEPENDENCIES;blocked->RETURN_ISSUES | CMKSP.INPUT_CONTRACT | stop | Before task-CSV import approval |

## Sources

- [Oracle FSM 26C: migration preparation and setup security](https://docs.oracle.com/en/cloud/saas/applications-common/26c/oafsm/using-functional-setup-manager.pdf), printed pages 41 and 75–79.
- [Oracle 26C security reference](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/fammm/Order_Administrator_job_roles.html): provider management and provider web-service access are distinct privileges; one is not proof of the other.
- [Oracle Features collection GET, 26B](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-features-get.html): filter by `FeatureCode` and read `EnabledFlag`; the item API recommends querying the collection rather than constructing an item key.
- [Oracle CMK opt-in code reference, 26B](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26b/oedsc/cmkapplpartnerssetupvl-3023.html): the view uses `ORA_CMK_B2B_DOCUMENT_SETUP` in its feature-enable test.
