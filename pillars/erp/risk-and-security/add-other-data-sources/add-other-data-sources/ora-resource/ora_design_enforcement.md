# Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Contract-source verification | Require the approved Add EPM Data Sources connector-definition contract. |
| 2 | Source-type resolution | Resolve the canonical source type name and code from the local connector-source-types registry. |
| 3 | OCI seeded-source readiness | Require approved seeded-source verification only when the resolved source type is OCI. |
| 4 | Contract verification | Require a complete credential-free payload and target binding. |
| 5 | Task handoff gate | Require validation and dependency evidence before task handoff. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Error |  | The connector-definition operation differs from the approved shared POST contract | Restore the approved shared contract, then revalidate | Yes |
| A configuration request is supplied | Error |  | Payload is incomplete, contains credentials, or is not bound to the target | Correct the payload and rebuild the preview | No |
| Resolved source type is OCI | Error | verify_oci_seeded_source | OCI seeded-source verification has not completed successfully | Complete the approved read-only OCI verification before downstream work | Yes |
| Resolved source type is USER-DEFINED | Error |  | A seeded-source check is requested | Do not run a seeded-source check | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| verify_oci_seeded_source | Resolved source type is OCI | Seeded connector collection; connector ID; OCI seeded-source readiness | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDS.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->CDS.READINESS_GATE;blocked->CDS.HANDLE_ISSUE | CDS.CHECK_DEPENDENCIES | stop | After contract dependency evaluation and any required OCI verification |
