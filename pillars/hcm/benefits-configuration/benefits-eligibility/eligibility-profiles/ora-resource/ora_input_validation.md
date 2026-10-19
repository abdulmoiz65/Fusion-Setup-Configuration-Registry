# Input Validation

Validate the Benefits workbook and the immutable Plan Copy package before the
governed REST runbook is allowed to perform a Fusion write.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Eligibility workbook | A readable end-user copy of the included Fusion_Elpro_Setup.xlsx sample, with at least one setup row; any filename is accepted. Unused tabs may be removed or left blank/header-only and contribute zero objects. Populated sections retain the sample's names and headers; their referenced dependencies must resolve | Stop only for unreadable, entirely empty, or invalid populated data, not for omitted or empty tabs | Copy the included sample workbook, replace its examples with your own data, and correct invalid populated rows or missing referenced dependencies | Always | |
| Effective date | An explicit ISO `YYYY-MM-DD` value; the governed launcher defaults to the current date | Stop before package generation | Supply a valid effective date or accept the launcher's current-date default | Before metadata generation | |
| Task context | Existing Run Book task-context JSON for Eligibility Profiles and the selected target environment | Stop before preview | Supply the matching task context | Always | |
| Target identity | OAuth `restBaseUrl` identifies an HTTPS origin; the OpenAPI document is host-neutral | Stop before any target lookup or write | Use the selected target environment's OAuth properties and the reviewed OpenAPI document | Always | |
| Plan Copy OpenAPI contract | plan-copy.openapi.json declares RequestSource FDOS metadata creation, PackageContent upload, the combined generateMappings import action, mapping reads, parent-status reads, ESS reads, and processing-log reads with their documented methods and media types; submitImport is absent | Stop before preview | Correct the OpenAPI document or importer and create a new preview | Before preview or import | |
| Immutable Plan Copy package | Nested ZIP passes checksum, expected XML-member, row-count, and object-inventory validation and has a recorded SHA-256 digest | Stop before preview | Regenerate and validate the package from the same workbook and target-pod lookup results | Before preview or import | |
| Complete target mappings | Every source mapping that has a source name has a target-pod TrgId; no manual mapping is required | Stop before generateMappings | Resolve the exact target ID through the maintained REST resolver catalog and regenerate the package | Before import submission | resolve_eligibility_profile_references |
| Immutable approval preview | Target, Plan Copy name, effective date, package digest, OpenAPI digest, setup-object counts, and intended action | Stop before live execution | Generate a fresh preview from the exact package and API contract | Before the first Fusion write | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Workbook lookup data has not been resolved on the selected target environment | Blocked | Resolve every applicable value through the maintained target-pod REST catalog | resolve_eligibility_profile_references |
| A required REST resolver returns zero or multiple exact active matches, except the documented Department first-row policy | Blocked | Correct or disambiguate the workbook value; do not use a database or source-pod identifier | resolve_eligibility_profile_references |
| Package, OpenAPI document, target, metadata, or effective date differs from the immutable preview | Blocked | Generate a new preview and obtain a new approval | |
| A generated Plan Copy mapping has a source name and null TrgId | Blocked | Resolve the mapping through REST and regenerate before a new approved generateMappings request | inspect_plan_copy_mappings |
| Combined mapping/import ESS completes but the Plan Copy parent has not reached ImportPlDesign 12 | Not successful | Continue read-only parent polling; classify ImportPlDesign 10 as failure and retrieve processing logs | inspect_plan_copy_result |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Workbook schema and supported columns | Reject missing required values, unsupported criteria, invalid enumerations, and cross-sheet references that do not resolve to objects in the package or target pod | Before XML generation | resolve_eligibility_profile_references |
| Profile Usage product | Accept all 11 enabled BEN_BNFT_CAGR_PRTN products by display name or code, including Opportunity Marketplace; preserve the mapped product in BnftCagrPrtnCd. Reject unknown values and disabled CAGR/MUSE rather than substituting Benefits. See the supported-product table in eligibility-reference.md | Before XML generation | |
| Effective date consistency | Bind the validated explicit/current effective date into metadata, target-pod lookup context, and the immutable preview | Always | |
| Archive contract | Reopen the nested ZIP, validate checksums and expected XML members, and record its SHA-256 and object inventory | Before preview and again before approved execution | |
| OpenAPI contract | Validate OpenAPI version, identity, host-neutral server, operation IDs, paths, methods, parameters, responses, metadata constants, and media types | Before preview and again before approved execution | |
| Mapping completeness | Pre-resolve every packaged target ID, then read every mappings page and reject each populated SrcName whose TrgId is null or blank | Before generateMappings and again after its combined mapping/import ESS request | inspect_plan_copy_mappings |
| Final application status | Report success only when ImportPlDesign is 12 and RequestStatus is not terminally unsuccessful; ImportPlDesign 10 is an application failure | After combined mapping/import ESS completion | inspect_plan_copy_result |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_PLAN_COPY.VALIDATE_INPUT | step | 1 | validate_input | valid->BEN_PLAN_COPY.CONFIRM_DEPENDENCIES;invalid->BEN_PLAN_COPY.FAILED | none | stop | Before package preview or execution of the Benefits Plan Copy REST runbook. |
