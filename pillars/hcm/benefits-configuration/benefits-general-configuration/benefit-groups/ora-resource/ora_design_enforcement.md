# Benefit Groups Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Scope | Restrict the request to the benefitGroups HDL business object |
| 2 | Schema | Validate the single benefitGroups section and its current live HDL attributes through core.data-loader |
| 2a | LegalEmployer reference | Record an exact-match result for each supplied LegalEmployer; a 403 is unverified_forbidden, not an invalid value |
| 3 | Destructive operation | Require Delete to use an explicitly reviewed delete artifact and current approval |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every request | Blocking |  | The request names another business object or an undocumented substitute | Keep the object as benefitGroups | Yes |
| Create, Update, or Delete | Blocking |  | The artifact has not passed core.data-loader live-schema validation | Validate the exact immutable artifact before approval | Yes |
| Create | Blocking |  | BenefitGroupName is empty or longer than the live 240-character limit | Supply a valid BenefitGroupName; do not synthesize a surrogate BenefitGroupId | Yes |
| Create | Blocking |  | RestAction is missing or is not POST | Use POST in the validated create artifact | Yes |
| Create or Update | Blocking |  | A supplied BenefitGroupDescription, LegalEmployer, or LegalEntityId exceeds its live metadata length | Correct the supplied value; do not truncate it automatically | Yes |
| A supplied LegalEmployer has zero or multiple distinct exact matches | Blocking | legalEmployersLov | The supplied name is invalid or ambiguous | Correct the name or resolve its identity; do not select a candidate | Yes |
| A supplied LegalEmployer is unverified_forbidden | Load readiness blocker only; field validation continues | legalEmployersLov | The name remains unverified after a 403 | Resolve access or use another workflow-approved authoritative check before live load | Yes |
| Update or Delete | Blocking |  | Required live-schema user keys are missing, ambiguous, or duplicated | Correct the source data; do not infer an identity | Yes |
| Delete | Blocking |  | The operation or target effect is not explicitly approved | Use the core.data-loader approval workflow for the exact delete artifact | Yes |
| Every request | Blocking |  | CSV export/import is proposed | Use HDL only; CSV support is not catalog-supported | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_GRP.ENFORCE_DESIGN | decision | 40 | design_enforcement | compliant->BEN_GRP.GATE_EXECUTION;blocked->BEN_GRP.HANDLE_ISSUE | BEN_GRP.LOOKUP_LEGAL_EMPLOYER | stop | Enforce Benefit Groups scope, live-schema validation, identity, delete approval, and the HDL-only route |
