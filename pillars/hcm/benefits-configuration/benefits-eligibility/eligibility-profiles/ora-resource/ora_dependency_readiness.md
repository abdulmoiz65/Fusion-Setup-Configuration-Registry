# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Eligibility workbook, effective date, and task context | Confirm Fusion_Elpro_Setup.xlsx and the Eligibility Profiles task context are readable, and validate the explicit/current effective date. |
| 2 | Selected target environment OAuth configuration | Confirm the OAuth properties identify the target and no credential is copied into an artifact or command. |
| 3 | Target-pod reference resolvers | Resolve all applicable workbook lookup values through the maintained REST catalog using the workbook effective date and required enterprise context. |
| 4 | Generated Plan Copy package | Generate all applicable XML batches and BEN_PL_COPY_MAP.xml, assemble the nested ZIP, validate it, and record its digest and object inventory. |
| 5 | Plan Copy OpenAPI contract | Validate references/plan-copy.openapi.json as OpenAPI 3.1.2 and against the benefitPlanCopyParameters importer. |
| 6 | Immutable preview and approval | Bind the exact target, metadata, OpenAPI digest, package digest, object counts, and intended action to a later standalone approve message. |
| 7 | Governed REST runbook | Use references/eligibility-reference.md#import-and-recovery and scripts/eligibility.py import for the RequestSource FDOS POST, enclosure PUT, single generateMappings ADF action, ESS monitoring, and application-result verification. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| benefits_workbook | Fusion_Elpro_Setup.xlsx, explicit/current effective date, and task context | Yes | Always | Blocked until validated | User-supplied workbook, launcher date, and existing Run Book task context | | The package, effective date, and setup-object inventory must be derived from explicit source data | Supply the maintained workbook and matching task context; override the current date only when required | Workbook path, selected worksheets, setup rows, effective date, and task identity |
| benefits_target | Selected target environment | Yes | Always | Blocked until validated | OAuth `restBaseUrl` plus the host-neutral OpenAPI document | | Lookup IDs and Plan Copy writes must come from the same target pod | Use the selected target environment's OAuth properties and reviewed OpenAPI document | Target origin and environment name |
| target_reference_resolution | Target-pod reference values and identifiers | Yes | When populated workbook fields require lookup codes or target identifiers | Lookup | Maintained resolver catalogs and read-only Fusion REST responses | resolve_eligibility_profile_references | Cross-pod names and IDs are not interchangeable | Correct any missing or ambiguous natural key before package generation | XML lookup codes, object labels, context IDs, source IDs, and target IDs |
| plan_copy_package | Valid immutable Plan Copy package | Yes | Before preview or live execution | Blocked until validated | Combined package generator output | | Fusion receives the package through the PackageContent enclosure | Regenerate after any workbook, lookup, XML, or target change | ZIP path, digest, object inventory, mapping count, and effective date |
| plan_copy_openapi | benefitPlanCopyParameters API contract | Yes | Before preview or live execution | Satisfied | references/plan-copy.openapi.json | | The importer permits only the reviewed Plan Copy lifecycle and media types | Update the OpenAPI document, importer, tests, and runbook together when the Fusion contract changes | Resource paths, operations, parameters, responses, schemas, and media types |
| immutable_approval | Immutable preview and explicit approval | Yes | Before the first Fusion mutation | Blocked until validated and approved | Preview JSON and a later standalone user message exactly approve | | Approval must apply to the exact package, contract, target, metadata, and intended effect | Review the preview and reply exactly approve in a later message | Approval fingerprint and approved execution intent |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Input validation | Workbook, task context, effective date, XML, mapping, archive, or conformance validation fails | No |
| Lookup blocker | A target-pod resolver is unavailable, unauthorized, unmatched, ambiguous, inactive, or missing its required ID field | No |
| Approval blocker | The immutable preview is absent, stale, changed, or not explicitly approved | No |
| Transport or authorization | OAuth, TLS, target reachability, REST privilege, or ESS access fails | No |
| Process failed | Combined mapping/import ESS, Plan Copy parent, or processing logs indicate an unsuccessful result | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PLAN_COPY.CONFIRM_DEPENDENCIES | step | 2 | resolve_dependency | ready->BEN_PLAN_COPY.RESOLVE_REFERENCES;blocked->BEN_PLAN_COPY.FAILED | BEN_PLAN_COPY.VALIDATE_INPUT | stop | After input validation and before any target-pod lookup or package generation. |
