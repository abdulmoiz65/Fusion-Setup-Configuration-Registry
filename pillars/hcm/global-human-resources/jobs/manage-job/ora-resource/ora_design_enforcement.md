# Manage Job Design Enforcement

## Purpose

Defines the mandatory Job, reference-data-set, Job Family, and Job Subfamily
design gates evaluated before preview or routing. It does not perform lookups,
apply defaults, or infer related setup.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact business record for read, edit, inactivation, or delete-effective-split; confirm zero exact duplicates for create |
| 2 | Validate context | Confirm effective context and recognized fields |
| 3 | Validate dependencies | Resolve supplied Job Family, Job Subfamily, and reference-data-set values through their declared resolvers |
| 4 | Validate mutation scope | Keep only explicitly modified child or EFF objects |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Read, edit, inactivate, or delete-effective-split | Blocking | find_manage_job | Identity is absent, unresolved, or ambiguous | Supply one exact business identifier | Input fix |
| CREATE_UNIQUENESS | Create | Blocking | find_manage_job | One or more exact matches already exist, or the uniqueness check is ambiguous | Supply a unique exact job identity | Input fix |
| DATE_EFFECTIVE_HISTORY | A create supplies multiple effective rows | Blocking |  | Rows do not form one valid Job history under the same JobCode and SetCode | Author the earliest row as create and later rows as updates in one logical object | Source rebuild |
| DATE_EFFECTIVE_SPLIT_DELETE | delete-effective-split is requested | Blocking | resolve_job_delete_history | Source uses HDL `DELETE`, omits `SET PURGE_FUTURE_CHANGES Y`, would remove the logical first split, or does not exactly bound future splits to remove | Use a Job `MERGE` row with the confirmed retained EffectiveStartDate and inclusive EffectiveEndDate; omit child rows and non-key attributes | Source rebuild |
| EFF_SHAPE | A Job EFF row is supplied | Blocking |  | Its category, context discriminator, or configured multirow unique key is incomplete or inconsistent | Correct the EFF row through input validation | Input fix |
| JOB_EFF_CHILD_CREATE_SHAPE | A new Job includes JobLegislative or JobExtraInfo | Blocking | read_job_eff_context | The child omits a parent link, context identity, effective boundary, multirow key, or fixed/default value required by the current child contract | Resolve the current child contract, apply only its confirmed values, and rebuild the source | Source rebuild |
| MODIFIED_OBJECTS_ONLY | Create, edit, or delete | Blocking |  | XLSX or DAT contains a child or EFF object that the user did not modify | Remove its worksheet and Data Loader Map row; retain only modified objects | Source rebuild |
| JOB_FAMILY_CONTEXT | A Job Family is supplied for create or edit | Blocking | resolve_job_family_for_job | The Job Family is unresolved, ineffective, ambiguous, or cannot be confirmed in the selected reference-data-set context | Resolve one effective Job Family and carry its code and confirmed set context into the base Job row | Lookup fix |
| CONTEXT | A date-effective or contextual value is requested | Blocking | find_manage_job | Required effective context is absent or invalid | Supply one supported effective context | Input fix |
| JOB_SUBFAMILY | A Job Subfamily is supplied | Blocking | resolve_job_subfamily_for_job | Job Subfamily is unresolved, ineffective, or ambiguous for the resolved Job Family | Resolve one exact effective Job Subfamily | Lookup fix |
| REFERENCE_DATA_SET | Reference-data scope is required | Blocking | resolve_job_reference_data_set | Set value is unresolved, unsupported, or ambiguous | Resolve one exact allowed set value | Lookup fix |
| DESIGN | A Job Family, Job Subfamily, or set is used | Blocking |  | The value is inferred from display text rather than exactly resolved | Supply or resolve one approved business value | Input fix |
| NAMING | Create or edit | Warning |  | Job name or code is not meaningful, or the code contains business logic | Use a meaningful name and an identifying code | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_job | Target, create-uniqueness, or effective-context evaluation | Exact identity, current values, effective context, and cardinality | ora_reference_lookups.md |
| resolve_job_delete_history | delete-effective-split | Confirmed retained start, inclusive deletion end, and preserved predecessor values | ora_reference_lookups.md |
| resolve_job_reference_data_set | Reference-data scope is required | One exact allowed stored set value | ora_reference_lookups.md |
| resolve_job_family_for_job | A Job Family is supplied | One effective Job Family in the selected set context | ora_reference_lookups.md |
| resolve_job_subfamily_for_job | A Job Subfamily is supplied | One effective Job Subfamily compatible with the resolved Job Family | ora_reference_lookups.md |
| read_job_eff_context | A new Job includes JobLegislative or JobExtraInfo | Current child linkage, identity, effective-boundary, multirow-key, and fixed/default contract | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JOB.DESIGN | decision | 6 | design_enforcement | passed->JOB.ROUTE;not_required->JOB.ROUTE;blocked->JOB.ERROR | JOB.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
