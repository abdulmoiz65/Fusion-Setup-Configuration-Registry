# Document Types Defaulting Rules

## Purpose

Defines source-backed defaults, preservation behavior, and no-default rules for
Document Types. This file does not own input validation, lookup mechanics,
design policy, payload construction, or execution routing.

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

## Standard Defaults

| Field | Default Value | Applies When | Can User Override? | Resolver | If Unavailable or Invalid |
|---|---|---|---|---|---|
| LegislationCode | blank/null | A create explicitly selects All Countries | No |  | Block when a nonblank legislation value is combined with All Countries |

## Preservation and No-Default Rules

| Field or Situation | Applies When | Required Behavior | Outcome |
|---|---|---|---|
| Requested operation | Intent is absent | Do not infer an operation; return the missing-input result | blocked |
| Unchanged edit value | An edit omits an existing value | Preserve the fresh reviewed current value | preserved |
| Parent HierarchyCode | A Delivery Preferences mutation is authored through Data Loader | Preserve the nonblank value from the fresh exact parent item on the root DocumentType row; never infer or default it | preserved |
| Create HierarchyCode | A Document Type create has no explicitly requested Delivery Preferences | Apply no value. Do not ask for, infer, or default `GENERAL` or `PAYROLL`; the declared REST parent-create payload must omit the attribute. | not_required |
| Delivery Preferences country representation | A country is supplied and exactly one current country resolves | Use CountryName only for the exact `Country` loader attribute and TerritoryCode only for the exact `LegislationCode` attribute; this is field mapping, not a default | preserved |
| Data Loader payroll statutory unit identity | A PSU name is supplied, exactly one current trimmed exact LOV match resolves, and Data Loader is selected | Use exact canonical PayrollStatutoryUnitName with blank PsuId on the anchor; use OrganizationId in PsuId with blank name on lower rows | preserved |
| Delivery Preferences legal employer identity | A Legal Employer name is supplied and exactly one current trimmed exact LOV match resolves | Use exact canonical LegalEmployerName with blank LempId on the anchor; use OrganizationId in LempId with blank name on lower rows | preserved |
| Delivery Preferences hierarchy anchor | A Department or Location row is requested | Add the applicable `Payroll Statutory Unit` or `Legal Employer` anchor with the explicitly requested delivery modes; this structural completion is mandatory and is not an inferred organization | applied |
| Delivery Preferences reconciliation | An expected hierarchy row already exists with the requested modes | Preserve it in Fusion and omit it from the retry source | preserved |
| Delivery Preferences mode-only edit | Exactly one existing child is matched and only Online or Paper is explicitly changed | Preserve the other mode from the fresh child read, use the fresh DocumentDeliveryPreferenceId, author only that child row, and omit an unchanged anchor | preserved |
| Missing anchor route | Reconciliation finds a missing organization anchor | Select the Data Loader route from current physical hierarchy state before applying technical identity. If the current metadata cannot represent the missing anchor, stop with a catalog mismatch. | applied |
| Missing anchor source key | A missing organization anchor is routed to Data Loader and requires source identity | Generate a deterministic collision-checked child source owner and ID without asking the user; do not apply either to the existing parent | applied |
| Optional create value | Country, subcategory, status, attachment, tag, HierarchyCode, or another optional value is omitted | Leave it unpopulated; do not request or infer it solely to complete intake, and omit an unpopulated loader attribute from the DAT | not_required |
| Lookup-backed value | Exactly one enabled current resolver result is available | Retain the current resolver result | preserved |
| Lookup-backed value | Resolution is missing or ambiguous | Apply no value and stop | blocked |
| Delivery Preferences group or child value | A group, delivery method, consent, level, organization, or person value is omitted | Never infer or default it | not_required |
| Runtime identity | A runtime ID is required | Use only an ID resolved for the current run; never reuse a saved ID or display label | blocked |
| Stale source | The reviewed source is stale | Require a fresh read or review before preview | blocked |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOCT.DEFAULTS | decision | 4 | apply_default | applied->DOCT.ENFORCE;preserved->DOCT.ENFORCE;not_required->DOCT.ENFORCE;blocked->DOCT.ERROR | DOCT.READ | stop | After validation, current-state reads, and required resolvers are complete |
