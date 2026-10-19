# Manage Item Classes Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Applicability gate | Licensed offering, non-Common Product Model intent, stable purpose, and consultant approval are established |
| 2 | Hierarchy gate | One exact enabled parent is resolved, no cycle is possible, and item-creation policy is intentional |
| 3 | Association gate | Every explicit non-inherited phase, category, NIR participant, entity, group, and attribute is exact and applicable |
| 4 | Existing-class impact gate | Existing matches are reused and any rename, repurpose, parent change, disablement, or removal has approved downstream impact and migration treatment |
| 5 | EFF support gate | EGO_ITEM_USER_DEF_ATTRS associations are absent and any EFF requirement is delegated to the dedicated attribute-group workflow and EGO_ITEM_EFF deployment |
| 6 | Package gate | The final archive derives from the approved baseline, preserves unrelated content, contains only the supported delta, and has an immutable fingerprint |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| A new item class is requested | Error | | CustomerModel is Common Product Model, license confirmation is absent, purpose is unstable, or consultant approval is absent | Use Manage Default Item Class for Common Product Model or establish applicable approval and design intent | Yes |
| CREATE or parent change | Error | resolve_parent_item_class | Parent is absent, disabled, ambiguous, self-referential, or cyclic | Select one exact enabled parent and revalidate inheritance | Yes |
| ItemCreationAllowedFlag is supplied | Error | | The value is not an explicit intentional policy for the class level | Confirm whether items may be created directly in this class | Yes |
| Explicit non-inherited association | Error | resolve_item_class_references | Reference is absent, inactive, ambiguous, incompatible, or unsupported | Select one exact applicable reference or remove it | Yes |
| Material change to an active class | Error | find_item_class_conflict | Downstream item, security, rule, catalog, lifecycle, NIR, integration, or reporting impact is missing or unapproved | Provide impact assessment and migration decision before changing the class | Yes |
| Route association uses EGO_ITEM_USER_DEF_ATTRS | Error | | EFF attribute-group association is included in the Manage Item Classes candidate package | Remove it; configure through Manage Item Attribute Groups and Attributes and deploy EGO_ITEM_EFF | Yes |
| Final-package readiness validation | Error | verify_item_class_package_baseline | Baseline, hierarchy, preservation, inventory, semantic diff, ZIP validity, target identity, or fingerprint evidence is missing or changed | Rerun the selected task SKILL.md local package-preparation workflow from a fresh task export | Yes |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_parent_item_class | CREATE or parent change | Exact parent natural key, enabled state, and non-cyclic hierarchy receipt | ora_reference_lookups.md |
| find_item_class_conflict | CREATE or material UPDATE | Existing definition, create candidacy, or field-level conflict receipt | ora_reference_lookups.md |
| resolve_item_class_references | Explicit supported associations are requested | Exact natural keys and applicability receipts | ora_reference_lookups.md |
| verify_item_class_package_baseline | Before final-package readiness validation | Target and release identity, hierarchy, headers, preservation, inventory, semantic diff, and fingerprint | ora_reference_lookups.md |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MICS.ENFORCE_DESIGN | decision | 40 | design_enforcement | passed->MICS.PACKAGE_PREVIEW_GATE;blocked->MICS.HANDLE_ERROR | MICS.CHECK_DEPENDENCIES | stop | Before final-package readiness validation |
