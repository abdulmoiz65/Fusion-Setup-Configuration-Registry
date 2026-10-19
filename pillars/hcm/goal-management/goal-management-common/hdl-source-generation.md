# Goal Management HDL Source Generation

This contract applies only after the deterministic router selects HDL.

## Capability and route policy

- Goal Plan (`GoalPlan`) and Library Goal (`ContentItem`) support HDL.
- Review Period has no Goal Management HDL route and remains REST-only.
- REST is the default below 25 resolved root records. HDL is selected by an
  explicit HDL/HCM Data Loader/data-load request or by at least 25 root rows.
  An explicit REST request overrides automatic volume routing.
- A DAT, ZIP, workbook, or functional document alone is input evidence, not
  permission to select HDL. Never change an approved or failed REST route to
  HDL automatically.

## Generated-source mode

When HDL is selected and no valid DAT/ZIP is supplied, the object task must:

1. resolve business rows from the functional input;
2. apply the same required-field, defaulting, reference, duplicate, key,
   date, type, audience, relationship, and object-specific validations used by
   the REST route;
3. block on every unresolved or ambiguous business value;
4. hand the resolved rows, business object, operation, target environment, and
   project/task context to `core.data-loader`;
5. have Core retrieve current target metadata, generate the editable source,
   convert it to the required DAT components, and build the immutable ZIP.

The consultant is not required to author a DAT or ZIP. Generated technical
keys, audit values, safe target defaults, component order, and metadata field
names come from the current target contract—not guesses or captured examples.

## Supplied-source mode

Preserve the supplied bytes. Validate a separate prepared copy with
`hdl_dat_preflight.py` and the object skill's current rules. If the source is
malformed but the business intent is complete and unambiguous, retain the
original as evidence and rebuild a new generated source through Core. Never
silently patch or upload a malformed source. If business intent is incomplete
or metadata cannot be obtained, fail closed with a diagnostic.

## Priority on goal creates

For Performance and Development Library Goals, materialize omitted priority
as `MEDIUM` (Medium) before preview/approval. Apply the same create-only rule
to `Goal` and `GoalPlanGoal`, including manual and library-derived plan goals.
These two components expose priority in Oracle's
[current loading examples](https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/examples-of-loading-goal-components.html).
Do not add priority to `GoalPlan` headers, eligibility, or other unrelated rows.

Preserve explicit priority and every unrelated supplied field. For a copied
goal, carry the fresh source priority through the existing resolved values
(`derivedValues` or evidence-bound `resolvedSemanticValues`/`rowBindings`),
unless the caller explicitly overrides it; apply Medium only when neither
provides a value. Do not default omitted fields on update or delete. An
explicit blank, null, or `#NULL` is not omission: preserve it for the existing
validation contract to accept or reject, never silently replace it with Medium.

The Library Goal catalog maps `PriorityCode` to `ItemText2`, established by
`LibraryGoalCommonPVO` entity mapping; see `hdl-mappings/library-goal-priority-source.md`.
Check this physical field against the full current template and component
metadata even when its label is generic. Reject contradictory explicit labels
or context evidence. An alternative mapping requires a unique template label or a
fresh, environment-bound `priorityMapping` proof with `ContextName=GOAL`,
`semantic=PriorityCode`, and `field`. Do not guess an `ItemText` slot. Resolve
enabled, effective codes from `HRG_PRIORITY`; the declared HDL read adapter
retrieves the complete lookup. A supplied context must carry the same current
mapping and allowed-value evidence. Missing/ambiguous metadata remains a
validation failure, not permission to omit priority.

The prepared DAT/ZIP and its preview must include the resolved priority.
Execution preflight rejects goal creates that still omit it. After load,
compare fresh stored priority **codes** with the approved values for every
created goal; a missing display meaning alone does not prove the code is absent.
Preserve the original supplied DAT/ZIP and all existing approval, identity,
route, status, and post-load reconciliation requirements.

## Approval and reconciliation

Core Data Loader owns the exact DAT/ZIP, digest, immutable preview, single
approval gate, upload and import initiation. Follow Core's status contract:
poll only when status/progress/results monitoring is explicitly requested,
including an explicit request to track the load to completion. Otherwise report
initiation as in progress, not successful configuration or completed runbook.
Do not add a second Goal Management approval for the same load. Approval is
valid only for the exact environment and immutable ZIP digest. Verify every
requested root row and key outcome after a successful load; a completed
process alone is not proof of correct business data.

No object validation failure is waivable. Do not fall back to FSM CSV, browser
entry, or a different transport when metadata/template generation fails.

## Executable preflight evidence

### Deterministic Library Goal create resolver (HDL only)

For root Performance/Development Library Goal creates routed as `hdl_generate`
or `hdl_dat_preflight`, use the executable resolver, not model-authored field
mapping or source-owner questions. This section does not apply to REST, ESS,
FSM, browser, Goal Plan, update/delete, translations or measurement bundles.
Those retain their existing workflows and validation contracts.

The discoverable configuration is local to this Goal Management folder:

- `goal-management-common/hdl-mappings/library-goal.json`: versioned semantic-to-HDL mappings,
  defaults, supported codes and provenance.
- `goal-management-common/hdl-mappings/library-goal.schema.json`: validated catalog contract.
- `goal-management-common/hdl-mappings/source-system-policy.json`: preserve supplied owner first;
  otherwise use the configured environment owner (`Fusion` -> `FDOS`). Always
  check that exact owner is enabled/effective in `HRC_SOURCE_SYSTEM_OWNER`;
  never choose the first active owner, create a lookup code or silently switch.
- `goal-management-common/scripts/library_goal_hdl_resolver.py`: checks the full UCM template
  and component metadata, constructs internal mappings/evidence, resolves the
  policy owner, and validates canonical business values.
- `goal-management-common/scripts/library_goal_hdl_search_adapter.py`: reads `result.items` and
  `result.summary`, normalizes string booleans, follows every page and rejects
  malformed/incomplete results. An exact-name match requires reconciliation;
  it never silently becomes create or update intent.

Canonical requirements are an internal JSON object, not a new consultant form:

```json
{
  "route": "hdl_generate",
  "profile": "performance_library_goal",
  "environment": "Fusion",
  "operation": "create",
  "rows": [{
    "GoalName": "Example library goal",
    "Description": "Business description",
    "StartDate": "2026-01-01",
    "TargetCompletionDate": "2026-12-31"
  }]
}
```

Derive these business values from the approved input. Use the development
profile for Development Library Goals; never infer a variant from the name.
The catalog supplies `GOAL`, `ItemText9=PERFORMANCE/DEVELOPMENT`, inactive
`ItemText1=I`, and company-wide `ItemText10=ALL`. The audience slot comes from
Oracle's HDL goal example; the `ALL` business code/default is the shared Goal
Management field contract. The code must not contradict advertised live
allowed values. A reduced DAT sample is not the complete target schema.
Unsupported restrictions/fields are errors, not permission to omit them.
BusinessUnitId still requires fresh owning-lookup value evidence.

Only after the owning task obtains a fresh allowed execution control, selects
this HDL read step and completes its required read prerequisites, run:

```sh
python3 pillars/hcm/goal-management/goal-management-common/scripts/hdl_dat_preflight.py \
  --requirements /protected/runtime/library-goal-requirements.json \
  --live-control /protected/runtime/allowed-owning-task-control.json \
  --prepared-output /protected/runtime/prepared-library-goal \
  --output /protected/runtime/library-goal-final-data.json
```

The live adapter reuses Core Data Loader configuration, authentication,
full-template retrieval and request services. It performs metadata, owner and
duplicate-search reads only; the search action's POST is read-only. This is
not an alternative route or permission to bypass workflow/controller gates.
`--read-evidence` replaces `--live-control` for offline replay/testing; preserve
actual read timestamps and environment identity, never relabel fixture data
as live evidence. Do not store customer/runtime payloads in tracked files.

For `hdl_dat_preflight`, also pass `--source` with the immutable original DAT
or flat ZIP. Supplied keys and supported mapped values are extracted and
validated automatically; conflicts with business requirements fail before
preparation. Both modes generate internal runtime context and the validated
`finalData` fragment. Core's renderer handles generated DAT serialization;
Core still owns ZIP creation, digest, immutable preview, approval and load.
No resolver result authorizes upload, task completion or a route switch.

Configuration/template drift produces a precise configuration diagnostic;
do not ask the consultant to discover technical fields/owners or guess them.
Missing business decisions, access failures or genuinely contradictory tenant
metadata remain blockers under the existing governance rules.

`hdl_dat_preflight.py` always uses execution validation. Structural-only reports
from `hdl_dat_validator.py` are for offline fixtures and cannot authorize upload.
Outside the root Library Goal create resolver above, the routed caller supplies
current `fieldMetadata` per component (operation
capabilities, allowed codes, date/integer/boolean types and boolean/code
`valueMap`), plus `semanticFields` mapping canonical Goal Plan/Library Goal
fields to the current HDL fields. Never infer lifecycle or audience slots from
a sample. Shared business rules apply after this mapping.

Resolve create/update/delete before enrichment. Only creates receive defaults.
Updates preserve omitted fields; provide `existingRows` keyed by the scoped row
identity and matching fresh `targetEvidence` for merged-state validation.
Provide operation-required update identities in `operationMandatoryFields`.
Every evidence record must match the execution environment and retain its
actual read timestamp. Preparation must not renew stale evidence. Regular Goal
Plans require per-row `reviewPeriodBounds` from the exact resolved period.

## Additional root Library Goal columns

For a Performance or Development `ContentItem` create, the existing catalog
fields and defaults remain the baseline. Only a consultant-supplied additional
column triggers the VO crosswalk and current-template resolution in
`goal-management-common/scripts/library_goal_hdl_fields.py`. The versioned
`goal-management-common/hdl-mappings/library-goal-vo-crosswalk.json` records direct
`LibraryGoalCommonPVO` to `ContentItemEO` attribute evidence. It does not make
joined display attributes, server-managed fields, or unsupported child
components writable.

Accept a business/VO field name, an unambiguous current HDL label, or an exact
current `ContentItem` HDL attribute. Require that the selected physical field
appears in both the full current UCM template and component metadata, has a
supported datatype, and is available for create. Reject two input names that
resolve to one physical field, duplicate labels, a contradictory established
mapping, an invalid advertised code, or a field that cannot be resolved.
Preserve the established `PriorityCode` source-backed exception for a uniquely
proved alternate tenant slot. An `ItemNumber*` scope/reference value also needs
fresh owning-lookup evidence before preparation; a VO association alone does
not prove the supplied numeric value. Keep every selected semantic-to-HDL
mapping in the internal manifest for approval and post-load reconciliation.

The simple supplied-`ContentItem.dat` route retains additional exact physical
headers and defers their acceptance to this same live metadata check. It does
not discard unknown columns. Existing requests without additional fields use
the original catalog mappings and generated DAT values.

## Resolved HDL identities and mappings

These requirements apply only to HDL preparation. They do not change REST or
ESS payloads, clients, approvals or submission behavior. The routed object
skill resolves the following context through its existing read capabilities;
the consultant supplies business requirements, not this internal structure.

- Fetch the selected configured owner from `HRC_SOURCE_SYSTEM_OWNER` in the
  target environment. Retain `evidenceSources.HRC_SOURCE_SYSTEM_OWNER` as a
  structured record with `source`, `environment`, actual `verifiedAt`,
  `lookupType: HRC_SOURCE_SYSTEM_OWNER` and `items` containing `LookupCode`,
  `EnabledFlag`, `StartDateActive` and `EndDateActive`. Null effective-date
  bounds are unbounded. Retain the advertised `allowedValues` in field metadata
  as well. Never default to USER01, invent an owner, or select another enabled
  owner merely because the requested owner is invalid. Preserve valid supplied
  source keys. Create source IDs are deterministic and include the resolved
  worker/goal context to avoid collisions between otherwise identical goals.
- Preserve every requested library restriction in `resolvedSemanticValues`,
  keyed by original `filename|component|line:N`. Each canonical field has
  `{value, evidenceRef}` after exact tenant lookup. This covers business unit,
  department, job family and other supplied restrictions; do not omit a field
  because its mapping is unavailable. A populated `ItemNumber*` in a supplied
  GOAL ContentItem also requires resolution of its meaning and target value.
- `semanticFields[component][semantic]` gives the actual HDL attribute.
  `mappingEvidence[component][semantic]` contains `{field, evidenceRef}`.
  The cited evidence contains `mappings: {component: {semantic: field}}`;
  the value lookup evidence contains `values: {semantic: resolvedValue}`.
  Both records retain the target environment, source and actual read time.
  Require current field metadata for the mapped attribute. For example, the
  Greenfield run established BusinessUnitId -> ContentItem.ItemNumber1;
  that observation must not be extrapolated to department/job-family slots.
  Consult authoritative semantic mapping evidence as well as the live template:
  existence of an unlabeled ItemNumber attribute does not prove its meaning.
- Library source keys (`SourceSystemOwner`, `SourceSystemId`), any supported
  business external identifier, and server-generated content IDs are distinct.
  Resolve a requested external identifier through the same mapping contract;
  never copy GoalPlanExternalId into ContentItem. Mark advertised server-only
  attributes `serverGenerated: true` in field metadata and omit them on create.
  Do not invent a business external identifier when the component does not
  require one; stable source keys already provide HDL idempotency.

## Goal and eligibility relationship evidence

Supply `rowBindings[filename|component|line:N]` with `evidenceRef` and a `values`
object containing the resolved DAT values. The structured evidence contains
the same values and its actual environment/read time. Preparation fills absent
fields but rejects supplied values that conflict with this resolution.
The manifest builder converts original row locations into final row identities;
unmatched input locations block preparation instead of losing a requirement.

- Goal bindings declare `kind: worker`, `template` or `organization`. Worker
  and template rows use WorkerPersonNumber and WorkerAssignmentNumber, plus
  GoalName, GoalTypeCode, GoalVersionTypeCode, StartDate and TargetCompletionDate.
  Resolve the intended worker separately from the requester. For a template,
  resolve its explicit administrative context; ordinary employee goals must
  never inherit the logged-in administrator. Numeric PersonId/AssignmentId
  substitutions are not accepted in this worker-user-key route. Organization
  goals require their resolved OrganizationName instead.
- GoalPlanGoal requires GoalPlanExternalId, GoalName, GoalTypeCode,
  GoalVersionTypeCode, GoalStartDate and GoalTargetCompletionDate. In Goal.dat
  use GoalWorkerPersonNumber/GoalWorkerAssignmentNumber; the supplied GoalPlan.dat
  template uses GoalPersonNumber/GoalAssignmentNumber. Keep these file-specific
  names distinct and confirm them with current metadata. Verify the complete
  Goal key against a row in the bundle or a fresh exact target read. Only that
  target read may set `existingGoal: true` on its evidence record. Unsupported
  GoalPlanId(SourceSystemId/SourceSystemOwner) hints fail before upload.
- EligibilityProfileObject bindings contain ObjectId, GoalPlanExternalId,
  EligibilityProfileName and the explicitly resolved RequiredFlag. Both the
  binding and evidence also retain `massRequestId`, `goalPlanExternalId`, and
  `talentObjectType: GOAL` from the resolved relationship. ObjectId is the
  MassRequest ID, not the Goal Plan ID. TalentObjectType is relationship evidence,
  not a DAT column unless a later live template explicitly advertises it.
- Resolve existing parents first. For a new plan whose MassRequest ID is not
  yet available, plan parent creation, successful reconciliation, then the
  eligibility package. Do not create placeholder IDs or trial-load dependencies.
  Each generated archive remains subject to the existing Data Loader approval
  contract; this sequencing does not authorize unapproved writes.

Runtime relationship values and lookup response details are omitted from the
durable audit manifest. Keep the original runtime context in protected runtime
storage; the redacted audit manifest is not a reusable execution input.
