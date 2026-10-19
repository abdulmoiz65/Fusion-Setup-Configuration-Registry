# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Connector source type | Resolve OCI or USER-DEFINED to its canonical source type name and code from the local registry. |
| 2 | OCI seeded-source readiness | When the resolved source type is OCI, verify seeded-source readiness before downstream work. No seeded-source check is required for USER-DEFINED. |
| 3 | Connector-definition contract | Use the approved Add EPM Data Sources connector-definition POST contract. |
| 4 | Connector configuration contract | Confirm supported fields, relationships, and action from that contract. |
| 5 | Risk Cloud authentication | Use the approved Add EPM Data Sources client scope and target-environment binding. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| connector_definition_rest_contract | Connector-definition REST contract | Yes | Every request | Satisfied | User-confirmed reuse of the Add EPM Data Sources connector-definition contract |  | Prevents inferred endpoint and payload behavior | Use only the approved shared connector-definition POST contract | POST /api/risk-cloud/rc-tools-ms/dataintegration/v1/dataIntegratorConnectorDefinitions; credential-free payload contract |
| connector_definition_authentication | Risk Cloud authentication | Yes | Every request | Satisfied | User-confirmed reuse of the Add EPM Data Sources Risk Cloud authentication readiness |  | Ensures the selected REST client uses the intended Risk Cloud scope | Use the approved shared client scope and target-environment binding | Target environment; rmc_scope readiness |
| connector_source_type | Connector source type | Yes | Every request | Lookup | pillars/erp/risk-and-security/add-other-data-sources/connector-source-types.json | resolve_connector_source_type | Prevents caller-supplied source type names or codes from diverging from the shared registry | Supply OCI or USER-DEFINED; the registry supplies the canonical values | sourceTypeName; sourceTypeCode |
| oci_seeded_source | OCI seeded-source readiness | Conditional | Resolved source type is OCI | Verify | Read-only BOSS connectorDefinitions query response | verify_oci_seeded_source | OCI is seeded and must be verified before downstream work | Run the approved read-only OCI verification; do not run this check for USER-DEFINED | Seeded connector collection; connector ID; OCI seeded-source readiness |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| REST contract verified | Approved source identifies endpoint, method, and credential-free payload contract | Yes |
| Authentication verified | Approved evidence identifies target environment and client scope | Yes |
| OCI seeded source verified | Resolved source type is OCI and its approved read-only verification succeeds | Yes |
| USER-DEFINED source type | Resolved source type is USER-DEFINED | No; no seeded-source check is required |
| Contract or authentication blocked | A required contract or protected authentication value is missing or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CDS.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | oci->CDS.VERIFY_OCI_SEEDED;user_defined->CDS.ENFORCE_DESIGN;blocked->CDS.HANDLE_ISSUE | CDS.RESOLVE_SOURCE_TYPE | stop | After input validation and source-type resolution |
