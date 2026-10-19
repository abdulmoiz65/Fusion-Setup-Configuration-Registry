# Reference Lookups

## Source

- Oracle readiness: Redwood: Configure Collaboration Messaging, 26B, https://docs.oracle.com/en/cloud/saas/readiness/erp/26b/fins26b/26B-fin-wn-f43222.htm
- Oracle readiness: Streamline the Import and Export of Messaging Setup Data, 26C, https://docs.oracle.com/en/cloud/saas/readiness/scm/26c/sccv26c/26C-sccv-wn-f46531.htm
- Oracle FSM 26C: migration preparation and setup security, printed pages 41 and 75–79, https://docs.oracle.com/en/cloud/saas/applications-common/26c/oafsm/using-functional-setup-manager.pdf
- Oracle readiness: Redwood with classic flows, 26D, https://docs.oracle.com/en/cloud/saas/readiness/scm/26d/proc26d/26D-procurement-wn-f50500.htm

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_simplified_feature_state | Automatically before simplified configuration export or import; do not ask the user to check the feature | Configured source or destination host and `ORA_CMK_B2B_DOCUMENT_SETUP` | Route through `core.fusion-api.rest-api-client` using its `references/fusion-rest-api.md` and `scripts/fusion_rest_client.py`; GET `/fscmRestApi/resources/11.13.18.05/features` with `q=FeatureCode='ORA_CMK_B2B_DOCUMENT_SETUP'`, `fields=FeatureCode,FeatureType,EnabledFlag`, and `onlyData=true` | `FeatureCode,FeatureType,EnabledFlag` | Exactly one same-host item with the exact feature code, `FeatureType: FEATURE`, and `EnabledFlag: Y`; a Redwood page profile is not evidence | Feature code, enabled flag, source or destination host, environment, UTC read time | Stop before export or import if disabled, absent, ambiguous, unreadable, or cross-environment |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A simplified configuration export or import is requested | Invoke `resolve_simplified_feature_state` automatically for the exact operation host through the central Core REST client. This read-only check needs no user confirmation. Continue only after `EnabledFlag: Y`; never ask the user whether the feature is enabled. |
| A documented UI procedure is available without an API contract | Preserve it as guidance; do not substitute browser automation or another endpoint |
| A Redwood configuration-page profile is enabled | Do not use it as a substitute for the Simplify opt-in; classic Redwood and simplified models are distinct |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CMKSC.RESOLVE_FEATURE_STATE | decision | 20 | reference_lookup | enabled->CMKSC.ENFORCE_DESIGN;blocked->CMKSC.RETURN_ISSUES | CMKSC.VALIDATE_INPUT | stop | Check the Simplify feature on the selected operation host |
