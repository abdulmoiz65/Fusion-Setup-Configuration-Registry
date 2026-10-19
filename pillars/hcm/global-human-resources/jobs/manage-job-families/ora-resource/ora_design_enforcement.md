# Manage Job Families Design Enforcement

## Purpose

Defines the mandatory Job Family and Job Subfamily-association design gates
evaluated before preview or routing. It does not perform lookups, apply
defaults, or infer associations.

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Confirm identity | Resolve one exact business record for read, edit, or delete; confirm zero exact duplicates for create |
| 2 | Validate context | Confirm effective context and recognized fields |
| 3 | Validate dependencies | Resolve each supplied Job Subfamily association through Common Lookups |
| 4 | Validate mutation scope | Keep only explicitly modified child objects |
| 5 | Decide readiness | Continue only when no applicable blocking rule remains |

## Design Rules

| Rule ID | Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|---|
| IDENTITY | Read, edit, or delete | Blocking | find_manage_job_families | Identity is absent, unresolved, or ambiguous | Supply one exact business identifier | Input fix |
| CREATE_UNIQUENESS | Create | Blocking | find_manage_job_families | One or more exact matches already exist, or the uniqueness check is ambiguous | Supply a unique exact job-family identity | Input fix |
| MODIFIED_OBJECTS_ONLY | Create, edit, or delete | Blocking |  | XLSX or DAT contains JobSubFamilyAssociation when the user did not modify that child object | Remove its worksheet and Data Loader Map row | Source rebuild |
| CONTEXT | A date-effective or contextual value is requested | Blocking | find_manage_job_families | Required effective context is absent or invalid | Supply one supported effective context | Input fix |
| JOB_SUBFAMILY | A Job Subfamily association is supplied | Blocking | resolve_job_family_subfamily | Job Subfamily is unresolved, disabled, ineffective, or ambiguous | Resolve one exact effective stored code | Lookup fix |
| ASSOCIATION_LIMIT | Associations are supplied | Blocking | resolve_job_family_association_limit | The resulting count exceeds a configured numeric limit | Reduce the requested associations | Input fix |
| DELETE_MODE | Delete with multiple date-effective records | Blocking | find_manage_job_families | Effective-split versus zap intent is absent or ambiguous | Require the user to choose the destructive scope | Input fix |
| SINGLE_DE_RECORD_ZAP | Delete with exactly one date-effective record | Blocking | find_manage_job_families | The route is not zap | Route to zap; do not request a delete-mode choice | Route fix |
| DELETE_REFERENCES | Delete | Blocking | find_job_references_for_job_family | The Job Family has any Job reference, incomplete reference evidence, or an unsupported reference filter | Resolve complete zero-reference evidence before authoring | Lookup fix |
| ZAP_DELETE | Zap delete | Blocking | find_manage_job_families | The exact logical Job Family is unresolved, its native JobFamily.dat fails current live Data Loader validation, the artifact uses MERGE, contains child rows, or mixes DELETE and MERGE for that Job Family | Author one validated DELETE&#124;JobFamily row using its resolved supported business key and disclose complete logical-object purge | Input or payload fix |
| DATE_EFFECTIVE_SPLIT_DELETE | Effective-split delete | Blocking | read_job_family_delete_history | The selected row is first, nonfinal, nonfuture, lacks an adjacent predecessor, is unresolved or ambiguous, or the final artifact does not use `SET PURGE_FUTURE_CHANGES Y` plus one JobFamily `MERGE` from the predecessor start through the selected end | Rebuild the bounded `MERGE` from fresh finder evidence; never use `DELETE` for a split | Lookup or payload fix |
| DESIGN | A Job Subfamily association is used | Blocking |  | The association is inferred rather than explicitly supplied and exactly resolved | Supply or resolve one approved stored code | Input fix |
| JOB_FAMILY_NAMING | Create or edit | Warning |  | Job family name or code is not meaningful, or family/subfamily associations are not confirmed | Use identifying codes and valid associations | Input fix |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_manage_job_families | Target, create-uniqueness, or effective-context evaluation | Exact identity, current values, effective dates, and cardinality | ora_reference_lookups.md |
| resolve_job_family_subfamily | A Job Subfamily association is supplied | One enabled exact stored code effective on the Job Family date | ora_reference_lookups.md |
| resolve_job_family_association_limit | Associations are supplied | Numeric maximum or not_configured | ora_reference_lookups.md |
| find_job_references_for_job_family | Delete | Complete zero-reference evidence | ora_reference_lookups.md |
| read_job_family_delete_history | Effective-split delete | Retained start, deleted end, and final-future eligibility | ora_reference_lookups.md |

## Enforcement Outcomes

| Outcome | When Used | Next Action |
|---|---|---|
| passed | Every applicable blocking rule is satisfied | Continue to the declared routing node |
| not_required | No design rule applies to the requested operation | Continue without changing the request |
| blocked | An applicable blocker remains or required evidence is unavailable | Stop and require the declared correction |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| JF.DESIGN | decision | 5 | design_enforcement | passed->JF.ROUTE;not_required->JF.ROUTE;blocked->JF.ERROR | JF.DEFAULTS | stop | After validation, dependencies, lookups, and defaulting are complete |
