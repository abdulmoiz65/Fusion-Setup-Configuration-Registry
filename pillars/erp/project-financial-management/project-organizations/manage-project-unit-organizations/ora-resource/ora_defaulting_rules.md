# Defaulting Rules

Apply defaults only while preparing a new approved load. A later explicit
status request resumes the accepted request identity without reapplying defaults
or changing the approved archive.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| EffectiveStartDate | 0001/01/01; FSCR policy, not a UI claim | DerivedAction = CREATE_NEW and omitted | No | |
| EffectiveStartDate | Selected organization's relevant effective-start date, including 0001/01/01 | DerivedAction = USE_EXISTING_ORGANIZATION and omitted; selection must finish first | No | find_active_organization |
| EffectiveEndDate | Blank; retain an explicitly supplied valid end date in create sections or existing child sections, but keep the existing Organization anchor blank | Both actions | No | |
| ProjectUnitCode | No default; suggest trimmed uppercase name with non A-Z/0-9/underscore characters replaced by underscores, repeated underscores collapsed and length limited to 150; require explicit acceptance or a manual nonblank code | Both actions; block and ask when omitted or blank; if suggestion is empty or underscores only, require manual entry | No; retain the chosen code unchanged | |
| ClassificationCode | PRJ_PROJECT_UNIT | Organization in create; OrgUnitClassification in existing flow | Reject conflicting value | |
| ClassificationCode | Exact selected existing ClassificationCode | Organization anchor in existing flow after exact selection | No | find_active_organization |
| ClassificationName | Project Unit Classification | New flow only | Reject conflicting value | |
| ClassificationName | Exact organizationClassificationsLOV display label for the selected existing ClassificationCode | Existing flow Organization anchor and child parent references | No | resolve_organization_classification |
| FLEX:PER_ORGANIZATION_INFORMATION_EFF | PRJ_PU_ATTRIBUTES | OrgInformation | Reject conflicting value | |
| EFF_CATEGORY_CODE | PRJ_PROJECT_UNIT | OrgInformation | Reject conflicting value | |
| OrgInformationContext | PRJ_PU_ATTRIBUTES | OrgInformation | Reject conflicting value | |
| SequenceNumber | 1 | OrgInformation | Reject conflicting value | |
| Status | A | OrgUnitClassification | Reject conflicting value | |
| SourceSystemOwner, SourceSystemId, SetCode, reference-data-set | Omit; never default FUSION, USER01 or COMMON | Both actions | Reject supplied HDL fields | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUORG.APPLY_DEFAULTS | step | 5 | apply_default | applied->PUORG.RESOLVE_DEPENDENCIES;failure->PUORG.RETURN_ISSUES | PUORG.ROUTE_OPERATION | stop | After DerivedAction, exact existing selection, and required existing-classification LOV resolution are complete |
