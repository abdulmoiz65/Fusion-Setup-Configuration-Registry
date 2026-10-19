# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

**Omitted classification input means preserve existing state.**

External reads require the active workflow's target, identity, privilege and evidence-destination preflight and delegate to core services. Permission inputs never initiate a pre-import task export.

Before invoking `resolve_project_organization_baseline.py --execute`, resolve the
framework version from the selected core workflow and supply it through
`--rest-framework-version`. The wrapper passes that same value as the core CLI's
header and records it in diagnostics. It never supplies an independent default.
Its exact-name query preserves semicolons inside the supplied name as data.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_existing_project_organization | Every request before defaults or additions | Exact name, configured target and effective date; optional confirmed selection | GET /hcmRestApi/resources/11.13.18.05/organizations through scripts/resolve_project_organization_baseline.py and core | OrganizationId, Name, ClassificationCode, Status, actual dates, all pages | Complete exact-name search; group by ID, select one effective identity, retain all selected classifications; resolve PA_PROJECT_ORG and PA_EXPENDITURE_ORG independently. scripts/validate_project_organization_classifications_hdl.py resolve_classification_state validates the REST evidence | Fresh complete identity/classifications and existing/missing requested targets; no permission/EFF read | Missing/ambiguous/incomplete/inactive/conflicting identity or PTO/PEO classification stops before artifacts; never use export absence to override REST existence |
| verify_classification_source_owner | Mutation; after approved new-owner creation | New owner or verified original update owner | GET /fscmRestApi/resources/11.13.18.05/commonLookups/HRC_SOURCE_SYSTEM_OWNER/child/lookupCodes/{owner} through core | LookupCode, EnabledFlag, active dates | Exact enabled effective owner; preserve original update owner | SourceOwner, LookupAsOfDate | Missing original owner blocks; confirmed missing new owner may enter separately approved creation; never retry |
| verify_classification_schema | Mutation | Organization and original/new component identity | core.data-loader load_business_object_schema with complete target metadata | Supported headers, references, key lengths and supplied segments | build_schema_evidence validates all attributes and partial projection | HdlSchema | Missing or unsupported metadata stops |
| verify_project_classifications_after_load | Terminal HDL success only | Baseline, approved additions/supplied changes and loader receipt | Governed organizations GET; fresh task-scoped populated FSM export through shared.setup-export.task-level-export only for post-load permission readback, parsed by scripts/resolve_classification_export.py | Identity/classification status/dates and readback permissions when applicable | Verify approved changes and preservation after mutation; export values never supply or default pre-import permissions | ClassificationVerified, ParentPreserved, PermissionUpdateVerified, VerificationEvidenceRef | Mismatch/unavailable readback stops completion; no resubmission |

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_existing_pto_update_identity | Legacy single request: existing PTO with supplied permissions; bulk request: additionally require update_existing_pto_permissions=true on that entry | Already available registered task-export projection and original OrgInformation binding, selected REST identity/target/date; no current permission values | Verify receipt success/completeness/freshness/task/target/date/run/checksum/provenance, one exact PTO identity and original OrgInformation owner/key/context/sequence. classification_export(..., verify_permissions=False) and existing_pto_information read keys only; never initiate an export or compare Permissions | ExistingPtoInformation identity without Permissions; original owner/key | Missing/ambiguous/stale/wrong-target identity or key blocks this explicit existing update; bulk without opt-in bypasses this resolver and needs no existing update keys; never infer new PTO, fabricate keys or export to obtain flags |
| verify_classification_mapping | Mutation | Verified original update identity, persisted new-component ledger, REST baseline and request | New keys only for REST-confirmed absent components; bind normalized values and baseline reference; existing updates retain original keys | SourceKeyMapping, PersistedMappings, ParentReference | Guessed/replacement keys, collision or stale/mismatched binding blocks |
| verify_classification_archive | Preview | Request-derived delta and target-supported metadata/evidence | One Organization.dat; no parent MERGE; new rows only for REST-confirmed missing requested targets; existing information update only supplied columns; regenerate exact bytes | checksum and rows | Unsupported/omitted-field/unrequested mutation or mismatch blocks |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| New PTO, PEO-only addition or omission/no-op | Bypass existing-update identity resolution entirely; no pre-import FSM export, ClassificationsExport, existing Permissions or original PTO keys required |
| Existing PTO permission input | Legacy single input or bulk update_existing_pto_permissions=true: use request values directly, never compare to old flags; verify already available original identity only. Bulk without opt-in preserves existing PTO and needs no original update key |
| REST shows a classification present | Preserve it; never create another row because an export is empty or unavailable |
| Post-load export | Readback only after terminal HDL success; shared exporter --data mode and local read_export validate actual bytes/provenance; no pre-import permission dependency |
| Write route | HCM Data Loader Organization only through core.data-loader; no FSM import |

## Execution Evidence Contract

Bulk evidence uses `{TargetEnvironment, RunId, Organizations, PersistedMappingsComplete, PersistedMappings}`. Organizations is ordered exactly like the request and contains a complete independent single-organization baseline for each entry, including unique EvidenceRef, timezone-aware CollectedAt and ValidationRunId equal to RunId. The governed collector performs fresh fully paginated reads for every name and publishes no aggregate on failure. TargetEnvironment must equal the request's configured target. Numeric selected parent IDs must be unique. Existing update identity is needed only for entries explicitly setting update_existing_pto_permissions=true; new-PTO permission input otherwise never initiates an existing update. Owner, target schema, ParentReference and registered SourceKeyMapping remain mandatory per active new organization; the top-level ledger covers the complete batch and prior registered mappings. New mapping bindings include validation_run_id, baseline_collected_at and baseline_as_of_date. Proposals from allocate_bulk_mappings have Persisted=false and must be registered before use.

generate_bulk_dats plans every entry before producing role-separated payloads; validate_bulk_text/validate(..., bulk_role) allow multiple parents, require unique keys and correct role/header/pairing. Regenerate exact bytes from trusted evidence before preview. write_bulk_archives refuses overwrite and emits per-ZIP target/run/organization/baseline/checksum/gate provenance; this is preparation, not approval or submission. Per-ZIP post-load readback must cover all its organizations; no-op entries need no archive or approval.

REST evidence keeps TargetEnvironment, EvidenceRef, Fresh, AsOfDate, OrganizationSearchComplete, OrganizationMatches, SelectedOrganization, SelectionConfirmed, ClassificationsComplete and Classifications. The REST collector issues completeness only after all pages succeed; flags are governed attestations, never user substitutes for reads. PTO and PEO existence is determined independently from those classifications. Inactive, duplicate or conflicting target rows block, including a target already present outside requested mutation scope.

For an existing update only, an already registered ClassificationsExport/ExportRunId receipt retains successful complete fresh task-data scope, TaskCode, ProcessId, target/date/run, SHA-256, EvidenceRef and MetadataEvidenceRef. Its exact PTO row and original SourceKeyBinding identify Component=OrgInformation, SourceSystemOwner, SourceSystemId, OrgInformationContext=Project Type Class Information and SequenceNumber=1. Permissions may be absent, empty or disagree with the request; they are neither required nor read/compared by the planner. No new export is triggered to populate this receipt. Without original keys, report the existing-update identity blocker and never allocate a replacement key.

ParentReference, SourceOwner, LookupAsOfDate, HdlSchema and persisted new-component mappings retain their prior core metadata/approval requirements. The mapping binds classification_baseline_ref; classification_export_ref is only identity provenance for an existing update. plan_request returns export_required=false and update_identity_required for the appropriate branch. An explicit matching-value request remains an explicit update: no equality/no-op claim is possible without reading old values. Total omission or no explicit mutation is no-op.

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PORGCLASS.FIND_ORGANIZATION | step | 3 | reference_lookup | resolved->PORGCLASS.CHECK_PERMISSION_UPDATE;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.APPLY_DEFAULTS | stop | Collect fresh fully paginated exact effective identity and independent PTO/PEO REST state per organization, bound to configured target and current run; no EFF or permission export |
| PORGCLASS.CHECK_PERMISSION_UPDATE | decision | 4 | evaluate_result | update_required->PORGCLASS.RESOLVE_UPDATE_IDENTITY;not_required->PORGCLASS.ROUTE_OPERATION;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.FIND_ORGANIZATION | stop | Bulk: only existing PTO entries with update_existing_pto_permissions=true and supplied permissions require identity; legacy single requests use requires_existing_pto_update_identity; additions/no-op bypass identity entirely |
| PORGCLASS.RESOLVE_UPDATE_IDENTITY | step | 5 | evaluate_result | resolved->PORGCLASS.ROUTE_OPERATION;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.CHECK_PERMISSION_UPDATE | stop | resolve_existing_pto_update_identity validates already available authoritative original keys only; no external export and no existing permission read |
| PORGCLASS.ROUTE_OPERATION | decision | 6 | evaluate_result | add_missing->PORGCLASS.VERIFY_SOURCE_OWNER;update_permissions->PORGCLASS.VERIFY_SOURCE_OWNER;already_configured->PORGCLASS.RETURN_ALREADY_CONFIGURED;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.CHECK_PERMISSION_UPDATE | stop | plan_request dispatches bulk to plan_bulk_request; independently add only requested missing roles, preserve others, aggregate ADD_MISSING/UPDATE_PERMISSIONS/ALREADY_CONFIGURED; skip no-op entries and require verified original identity for explicit updates |
| PORGCLASS.VERIFY_SOURCE_OWNER | step | 7 | reference_lookup | valid->PORGCLASS.VERIFY_SCHEMA;absent->PORGCLASS.OWNER_CREATION_GATE;invalid->PORGCLASS.RETURN_ISSUES;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.ROUTE_OPERATION | stop | Every explicit mutation including pure permission update; missing original owner never enters creation |
| PORGCLASS.RECHECK_SOURCE_OWNER | step | 9 | reference_lookup | valid->PORGCLASS.VERIFY_SCHEMA;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.OWNER_CREATION_GATE | stop | Verify exact owner after approved or uncertain creation; no replay |
| PORGCLASS.VERIFY_SCHEMA | step | 10 | reference_lookup | valid->PORGCLASS.RESOLVE_DEPENDENCIES;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.ROUTE_OPERATION | stop | Owner valid from initial check or recheck |
| PORGCLASS.VERIFY_POST_LOAD | step | 16 | reference_lookup | verified->PORGCLASS.RETURN_CLASSIFIED;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.LOAD_COMPLETION_GATE | stop | On requested verification after each ZIP's terminal success verify every included organization by fresh governed REST and requested permissions/preservation; post-load export is readback only; all requested ZIPs must verify before completion |
