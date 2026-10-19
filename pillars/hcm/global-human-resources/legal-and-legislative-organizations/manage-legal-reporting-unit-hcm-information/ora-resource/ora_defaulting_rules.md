# Legal Reporting Unit HCM Information Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Manage Legal Reporting Unit HCM Information. This file does not own input
validation, lookup mechanics, design policy, payload construction, or execution
routing.

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
| Effective read date | Today's system date | Get omits a date | Yes |  | Request one unambiguous YYYY-MM-DD date only when the user overrides the default |
| Tax Reporting Unit category | Tax Reporting Unit Details | A generic Tax Reporting Unit view omits a category | Yes | resolve_tax_reporting_unit_eff_metadata | Block when current metadata does not resolve the category |
| Reporting Establishment category | Reporting Establishment Details | A generic Reporting Establishment view omits a category | Yes | resolve_reporting_establishment_eff_metadata | Block when current metadata does not resolve the category |
| Synchronization loader object | ManageLegalReportingUnit | Current synchronization is required | No | resolve_lru_loader_contract | Block when the registered object or current contract is unavailable |
| Classification loader object | ManageLegalReportingUnitHcmClassifications | A classification change is requested | No | resolve_lru_loader_contract | Block when the registered classification contract is unavailable |
| Tax Reporting Unit EFF loader object | taxReportingUnitsEFF | A supported mutation affects the Tax Reporting Unit branch | No | resolve_lru_loader_contract | Block when the registered object or current contract is unavailable |
| Reporting Establishment EFF loader object | reportingEstablishmentsEFF | A supported mutation affects the Reporting Establishment branch | No | resolve_lru_loader_contract | Block when the registered object or current contract is unavailable |
| Correction action loader object | ModifyOrganizationUnitForChildCorrect | An EFF correction affects one or more branches | No | resolve_lru_loader_contract | Block when the registered object or current contract is unavailable |
| Dated-update action loader object | SplitOrganizationUnitForEFFUpdate | An EFF dated update affects one or more branches | No | resolve_lru_loader_contract | Block when the registered object or current contract is unavailable |
| Date-effective parent-delete loader object | DeleteOrganizationUnitForDTDelete | An eligible date-effective parent-row delete is requested | No | resolve_lru_loader_contract | Block when the registered parent-delete contract is unavailable |
| Multi-object order | taxReportingUnitsEFF, reportingEstablishmentsEFF | Both EFF branches contain requested changes | No |  | Block when branch scope is ambiguous |
| Empty context display | No configured segments | A describe-backed requested or default context has no current row | No | read_lru_eff_context | Render the context heading and this exact marker; block only when the context itself is absent from current metadata |
| Terminal end date display | End of Time | A returned end date is the Fusion terminal date | No |  | Preserve the returned nonterminal date otherwise |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Classification answers | A classification mutation is requested | Require explicit Yes/No answers for both business-facing questions. While both questions are pending, `Both` or `Yes to both` is itself an explicit Yes/Yes response, not a default; never infer any other omitted answer | not_required |
| Omitted EFF segment | Every mutation | Preserve the freshly read value and omit it from changed-value mapping | preserved |
| Mutation operation | Every mutation | Derive it only from requested intent, current effective boundary, row existence, and the selected object's current contract; never default it | not_required |
| New EFF context row | The exact context child read returns no row | Preserve the fresh parent locator set. Leave child OrgInformationId, EffectiveStartDate, and EffectiveEndDate blank; never default child dates from either a parent or requested operation date | preserved |
| Correction or dated-update action | Edit is requested | Never default the action; derive it from the requested date and each affected top-level organization's current start | not_required |
| EFF controls | An EFF context mutation is requested | Resolve context and category controls from current metadata; never infer them from an example | not_required |
| Date-effective delete target | An unqualified supported delete is requested | Use only the greatest eligible current history start; never default an older or first row | not_required |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRU.DEFAULTS | decision | 18 | apply_default | applied->LRU.DESIGN;preserved->LRU.DESIGN;not_required->LRU.DESIGN;blocked->LRU.ERROR | LRU.DEPENDENCIES | stop | After validation and all applicable resolvers complete |
