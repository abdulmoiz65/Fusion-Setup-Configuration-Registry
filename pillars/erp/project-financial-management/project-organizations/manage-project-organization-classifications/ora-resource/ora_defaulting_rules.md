# Defaulting Rules

**Omitted classification input means preserve existing state.**

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| requested_target_classification | No implicit target | Omitted | No; explicit permission input expresses PTO intent | |
| New PTO omitted permissions | N | REST proves requested PTO absent | No; explicit enabled values become Y | find_existing_project_organization |
| Existing PTO omitted permissions | Preserve by omitting their HDL update columns | REST proves PTO present | No; never read or compare exported flags | find_existing_project_organization |
| PEO | Preserve if present; create only if explicitly requested and REST proves absent | PEO scope resolution | No | find_existing_project_organization |
| source_system_owner | HRC_SQLLOADER | New components and omitted/blank owner | No | |
| Existing PTO source keys | No default; exact original registered OrgInformation binding | Legacy existing PTO with supplied permissions; bulk also requires update_existing_pto_permissions=true | No replacement keys; bulk without opt-in needs no update key | resolve_existing_pto_update_identity |
| Effective dates | Selected parent's actual dates | New child rows; existing update must match resolved range | No | find_existing_project_organization |
| PTO code/category | PA_PROJECT_ORG | New PTO | Reject conflicts | |
| PEO code/category | PA_EXPENDITURE_ORG / NO_EFF_CATEGORY | New PEO | Reject conflicts | |
| Status | A | New classification | Reject conflicts | |
| PTO context / FLEX / category / sequence | Project Type Class Information / same / PA_PROJECT_ORG / 1 | PTO information | Reject conflicts | |
| New source IDs | Allocate once, persist/reuse | New components only | No | verify_classification_mapping |
| SetCode | Omit | Every artifact | Reject supplied value | |
| Bulk existing PTO update | false | update_existing_pto_permissions omitted | No; creation permissions never imply existing update | |
| Bulk omitted scope/permissions | Apply omission/new-PTO defaults independently per REST-resolved organization | Bulk request | Never default existing permission values | find_existing_project_organization |

New PTO values come only from request normalization plus omitted-field N defaults. Do not require any existing permission values. All-N values are allowed through local preparation under the user instruction; do not restore the earlier at-least-one-Y gate. Fusion load errors remain failures without automatic replay. APPLY_DEFAULTS normalizes supplied values/owner; actual permission defaults wait for REST existence resolution.

## Task Nodes
| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PORGCLASS.APPLY_DEFAULTS | step | 2 | apply_default | applied->PORGCLASS.FIND_ORGANIZATION;failure->PORGCLASS.RETURN_ISSUES | PORGCLASS.VALIDATE_INPUT | stop | Normalize supplied values/owner; defer new PTO N defaults until REST state resolves |
