# Manage Item Classes Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Applicability and approval | Confirm the licensed product model, exclude Common Product Model class creation, and retain implementation-consultant approval |
| 2 | Target baseline | Bind a fresh same-target successful Manage Item Classes task export and fingerprint |
| 3 | Hierarchy and identity | Resolve one exact eligible parent and classify the requested class as create, reuse, or explicit update |
| 4 | Explicit references | Resolve each supported non-inherited lifecycle phase, attachment category, assignee, entity, group, and attribute reference |
| 5 | New Item Request graph | Validate exact route, step, participant, association, and attribute parent-child keys |
| 6 | EFF separation | Remove EGO_ITEM_USER_DEF_ATTRS associations and route them to the dedicated attribute-group workflow plus EGO_ITEM_EFF deployment |
| 7 | Immutable package | Preserve the baseline, create the smallest supported delta, validate the ZIP, and calculate its fingerprint |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| mics_applicability | Licensed product model and consultant approval | Yes | A new item class is requested | Satisfied | Approved Run Book context | | New classes are not the Common Product Model route and require an applicable licensed offering | Confirm applicability and approval before authoring | CustomerModel, LicenseConfirmed, ImplementationConsultantApproval |
| mics_baseline | Current task package baseline | Yes | Always | Verify | Fresh same-target task export | verify_item_class_package_baseline | Safe authoring depends on the current target hierarchy and member contract | Refresh the exact task export | Baseline receipt and fingerprint |
| mics_parent | Eligible parent item class | Yes | CREATE or parent change | Verify | Complete current item-class export | resolve_parent_item_class | Parent identity owns hierarchy and inheritance | Supply one exact enabled parent | ParentItemClassName and receipt |
| mics_identity | Existing class state | Yes | CREATE or material UPDATE | Verify | Complete current item-class export | find_item_class_conflict | Prevent duplicate identities and accidental repurposing | Reuse an exact match or approve a documented update | Create, reuse, or update classification |
| mics_references | Explicit supported references | Yes | Explicit non-inherited associations are requested | Verify | Fresh task export and approved Run Book | resolve_item_class_references | References must exist and be applicable in the target | Correct or remove unresolved references | Natural keys and receipts |
| mics_nir | Consistent NIR graph | Yes | New Item Request is required | Satisfied | Normalized Run Book rows | | Child rows depend on exact parent identities and unique keys | Correct orphan or duplicate rows | Route graph |
| mics_eff | EFF association separation | Yes | EGO_ITEM_USER_DEF_ATTRS is requested | Blocked | Explicit unsupported-scope rule | | Manage Item Classes import does not reliably add the EFF attribute group and may finish with a warning | Remove it and use Manage Item Attribute Groups and Attributes, then deploy EGO_ITEM_EFF | Separate EFF work item |
| mics_package | Immutable supported package | Yes | Before Data Loader preview | Verify | Final locally prepared FSM ZIP | verify_item_class_package_baseline | Preview and approval must bind to the exact package | Rebuild and revalidate after any change | Inventory, semantic diff, and fingerprint |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Approved evidence or normalized rows already establish the dependency | Continue |
| Verify | Export, hierarchy, identity, reference, or package evidence must be checked locally | Local verification only |
| Blocked | Required evidence, eligibility, uniqueness, or supported scope is missing | No |
| Delegated | The requirement belongs to a different declared setup workflow | Run the named workflow separately; do not include it in this package |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MICS.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->MICS.ENFORCE_DESIGN;blocked->MICS.HANDLE_ERROR | MICS.RESOLVE_REFERENCES | stop | After reference resolution and before design enforcement |
