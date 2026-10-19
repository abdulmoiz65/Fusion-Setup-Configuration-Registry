# Legal Entity HCM Information Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Legal Entity HCM Information. This file does not own input validation,
lookup mechanics, design policy, payload construction, or execution routing.

## Defaulting Precedence

| Priority | Condition | Required Action | Outcome |
|---|---|---|---|
| 1 | A valid explicit value is supplied and user override is allowed | Preserve the supplied value | preserved |
| 2 | An edit omits a field that must retain its current value | Preserve the freshly read current value | preserved |
| 3 | Exactly one Standard Defaults row applies | Apply that default | applied |
| 4 | No defaulting or preservation rule applies | Make no change | not_required |
| 5 | A required resolver is unresolved, ambiguous, or failed | Apply no value and stop | blocked |
| 6 | Multiple conflicting default rows apply to the same field | Apply no value and stop | blocked |
| 7 | A supplied value conflicts with a non-overridable default | Apply no value and stop | blocked |

## Metadata Default Gate

Before applying a Standard Defaults row, confirm that current task evidence and
the selected object's operation-specific loader metadata support the field and
value. If an optional default is not confirmed, omit it; if a required value
cannot be resolved, ask only for that value and block the handoff.

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| Legal Employer loader object | legalEmployersEFF | A supported mutation affects an applicable Legal Employer branch | No | resolve_legal_entity_loader_contract | Block when the registered object or current contract is unavailable |
| Payroll Statutory Unit loader object | payrollStatutoryUnitsEFF | A supported mutation affects an applicable Payroll Statutory Unit branch | No | resolve_legal_entity_loader_contract | Block when the registered object or current contract is unavailable |
| Correction action section | ModifyOrganizationUnitForChildCorrect | An EFF correction affects one or more branches | No | resolve_legal_entity_loader_contract | Block when the current embedded action contract is unavailable |
| Dated-update action section | SplitOrganizationUnitForEFFUpdate | An EFF dated update affects one or more branches | No | resolve_legal_entity_loader_contract | Block when the current embedded action contract is unavailable |
| Date-effective parent-delete loader object | DeleteOrganizationUnitForDTDelete | An eligible date-effective parent-row delete is requested | No | resolve_legal_entity_loader_contract | Block when the registered parent-delete contract is unavailable |
| Multi-object order | legalEmployersEFF, payrollStatutoryUnitsEFF | Both branches contain requested changes | No |  | Block when branch scope is ambiguous |
| Effective read date | Today's system date | Get omits a date | Yes | resolve_legal_entity_hcm_roots | Request one unambiguous YYYY-MM-DD date only when the user overrides the default |
| Legal Employer default category | Current contexts assigned to Legal Employer Details | A generic Legal Employer view omits a category | Yes | resolve_legal_entity_eff_metadata | Block when current metadata does not resolve one applicable category |
| Payroll Statutory Unit default category | Current information category containing PER_PSU_PAYROLL_INFO | A generic Payroll Statutory Unit view omits a category | Yes | resolve_legal_entity_eff_metadata | Block when current metadata does not resolve one applicable category |
| Empty context display | No configured segments | A describe-backed requested or default context has no current row | No | resolve_legal_entity_eff_metadata | Render the context heading and this exact marker; block only when the context itself is absent from current metadata |
| Terminal end date display | End of Time | A returned end date is the Fusion terminal date | No |  | Preserve the returned nonterminal date otherwise |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Omitted EFF segment | Every mutation | Preserve the freshly read value and omit it from changed-value mapping | preserved |
| Mutation operation | Every mutation | Derive it only from requested intent, current effective boundary, row existence, and the selected object's current contract; never default it | not_required |
| New EFF context row | The exact context child read returns no row | Preserve current top-level organization evidence and let Core Data Loader apply the current create contract | preserved |
| Correction or dated-update action | Edit is requested | Never default the action; derive it from the requested date and each affected top-level organization's current start | not_required |
| EFF controls | An EFF context mutation is requested | Resolve context and category controls from current metadata; never infer them from an example | not_required |
| Date-effective delete target | An unqualified supported delete is requested | Use only the greatest eligible current history start; never default an older or first row | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.DEFAULTS | decision | 11 | apply_default | applied->LE.DESIGN;preserved->LE.DESIGN;not_required->LE.DESIGN;blocked->LE.ERROR | LE.DEPENDENCIES | stop | Readiness is satisfied and safe defaults or preservation rules must be applied |
