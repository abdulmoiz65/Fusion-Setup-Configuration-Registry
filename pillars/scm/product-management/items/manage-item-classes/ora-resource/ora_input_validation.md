# Manage Item Classes Input Validation

Validate the normalized task input and generated FSM archive before the package
is handed to the central Data Loader preview. Business-design decisions belong
to design enforcement, and target-reference evidence belongs to reference
lookups.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Applicability evidence | CustomerModel, LicenseConfirmed, ImplementationConsultantApproval | Block before package preparation | Confirm that the customer is licensed for Product Hub, Product Development, or Product Management; confirm that Common Product Model is not the intended route; retain consultant approval in the Run Book | A new item class is requested | |
| Item-class identity | ItemClassCode, ItemClassName, ParentItemClassName, ItemClassType | Block before package preparation | Supply stable identity values and resolve one exact eligible parent | Every item-class row | resolve_parent_item_class |
| Item-class flags | DefaultItemClassFlag, EnabledFlag, ItemCreationAllowedFlag, PublicFlag, NewItemRequestRequiredFlag | Block before package preparation | Supply Y or N for every required flag | Every item-class row | |
| Generation methods | ItemNumberGenMethodValue, ItemDescriptionGenMethodValue, CfgItemNumberGenMethodValue, ItemNumberGenMethodCode, ItemDescriptionGenMethodCode | Block before package preparation | Supply consistent method values and codes | Every item-class row | |
| Existing-class change context | ChangeIntent and ImpactAssessment when the class may already exist | Block an ambiguous create or material update | Compare the requested definition with the complete current target export and state create, reuse, or update intent | Before CREATE or material UPDATE | find_item_class_conflict |
| New Item Request route | ItemClassCode, RouteInternalName, TemplateFlag | Reject the route | Supply a route that references the generated item class | A route is requested | |
| New Item Request route step | RouteInternalName, StepSeqNumber, AdhocStepFlag, ResponseRequiredFrom, SkipFlag | Reject the step | Supply a step that references one generated route | A route step is requested | |
| Workflow participant | ItemClassCode, RouteInternalName, StepSeqNumber, ObjectPk2, AdhocPeopleFlag, AssigneeName, AssigneeTypeCode, ResponseRequiredFrom | Reject the participant | Supply a participant that references one generated route step | A participant is requested | |
| Route association or attribute | Participant ObjectPk2 and association ObjectPk2Value plus the applicable entity, group, and attribute fields | Reject the orphan or unsupported row | Supply exact parent keys and supported association values | An association or route attribute is requested | resolve_item_class_references |
| Immutable package evidence | Fresh task export receipt, package inventory, semantic diff, target identity, release identity, SHA-256 fingerprint | Block before Data Loader preview | Rebuild from a fresh same-target task export and rerun all validations | A final FSM ZIP is prepared | verify_item_class_package_baseline |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| CustomerModel is Common Product Model | Creating an additional item class is outside the supported design | Route the requirement to Manage Default Item Class and stop this candidate | |
| A parent is supplied | Continue only when one exact enabled parent exists and the requested relationship cannot form a hierarchy cycle | Correct the parent or hierarchy before package preparation | resolve_parent_item_class |
| A create or update is requested | Continue only when the complete target export proves create candidacy, an exact reusable match, or an explicitly approved material update | Reuse the exact match or resolve the conflicting definition | find_item_class_conflict |
| A lifecycle phase, attachment category, assignee, entity, group, or attribute is explicitly assigned | Continue only with an exact applicable reference established by approved evidence | Correct or remove the unresolved reference | resolve_item_class_references |
| A lifecycle phase or attachment category is marked Inherited Y | Treat the row as evidence of parent inheritance, not as a child-class delta | Exclude the inherited row from the child-class payload | |
| DefinitionEntityName is EGO_ITEM_USER_DEF_ATTRS | The EFF attribute-group association is unsupported in the Manage Item Classes package path | Remove it from this package; use Manage Item Attribute Groups and Attributes and then deploy EGO_ITEM_EFF | |
| A route, step, participant, association, or route attribute is generated | Every child identity must exactly match one generated parent identity | Reject any orphan, duplicate, or ambiguous child row | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ItemClassCode, ItemClassName, ParentItemClassName, and ItemClassType are nonblank after trim | Reject the item-class row | Every item-class row | |
| Boolean-style flags are exactly Y or N | Reject the affected row and identify the field | A documented flag is supplied | |
| StepSeqNumber, ObjectPk2, and ObjectPk2Value are positive integers and unique within their parent scope | Reject the affected row | A step, participant, association, or attribute is supplied | |
| ItemNumberGenMethodCode and ItemDescriptionGenMethodCode agree with their method values | Stop and require corrected source values | Generation methods are supplied | |
| NirReqd and NewItemRequestRequiredFlag agree | Stop and require one consistent NIR requirement | Either value is supplied | |
| ResponseRequiredFrom is EGO_ONE or EGO_ALL | Reject any other value | A route step or participant is supplied | |
| Route, step, participant, association, and attribute parent keys match exactly | Reject the orphan or ambiguous row | A NIR child row is supplied | |
| EGO_ITEM_USER_DEF_ATTRS is absent from candidate route associations | Block the candidate and route EFF work separately | A route association is supplied | |
| Inherited lifecycle phases and attachment categories are absent from the child delta | Remove the inherited row and preserve parent inheritance | Inherited is Y | |
| The final archive preserves expected FSM metadata, member hierarchy, CSV headers, order, and encoding | Block before Data Loader preview | A final package exists | verify_item_class_package_baseline |
| Any validated source or archive content change invalidates prior validation and approval | Rebuild, revalidate, calculate a new fingerprint, and require a new central preview | Input or package changes | verify_item_class_package_baseline |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MICS.VALIDATE_INPUT | step | 10 | validate_input | valid->MICS.RESOLVE_REFERENCES;invalid->MICS.HANDLE_ERROR | none | stop | Before any reference resolution or final-package readiness validation |
