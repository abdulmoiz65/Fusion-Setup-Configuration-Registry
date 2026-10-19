# Manage Legal Entity Registrations Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_entity_registration_address | Before CREATE | Fresh same-target, scope-complete XLE_LE_LEGAL_ADDRESS.csv; supplied formatted natural key and jurisdiction country | Require one exact active internal address compatible with the jurisdiction country; export yields the legal-address natural key only | FormattedAddress and receipt-only location semantics | Zero or many blocks; expand export scope before treating zero as absence; never copy LocationId |
| find_entity_registration_conflict | Before CREATE | Complete target XLE_REGISTRATION.csv; SourceTable XLE_ENTITY_PROFILES, parent identifier, jurisdiction, registration number, name, address, dates, identifying state | Match exact parent, jurisdiction, and number, then compare the complete definition and existing identifying rows in scope | Existing-match, conflict, or create-candidacy receipt | Zero after scope-complete proof is candidacy; exact match, conflicting definition, multiple, or incomplete scope blocks CREATE |
| verify_entity_registration_package | Before preview | Fresh target ASM, exact current parent row, XLE_REGISTRATION.csv, and header-only ORA_XLE_LEGAL_ENTITY_REGISTRATION_FUNCTION.csv | Require exact hierarchy, header/order, unchanged parent, zero function candidate rows, unrelated-row preservation, target/release identity, task-scoped successful-status evidence, and fingerprint | Package-shape and parent receipt | Stale, partial, child-only, wrong-target, required-object failure or warning, or ambiguous evidence blocks |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_registration_parent_entity | Parent is supplied | Exact LegalEntityIdentifier or name and as-of date | /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV | LegalEntityId, Name, LegalEntityIdentifier, EffectiveFrom, EffectiveTo | Require one exact effective identifier match; name may locate candidates but identifier owns the child row | LegalEntityIdentifier and receipt-only LegalEntityId | Zero, many, inactive, or ineffective blocks |
| resolve_entity_registration_jurisdiction | Jurisdiction is supplied | Exact jurisdiction name, parent geography, registration type, and as-of date | /fscmRestApi/resources/11.13.18.05/legalJurisdictionsLOV | JurisdictionId, Name, GeographyId, IdentifyingFlag, LegislativeCategoryCode, LegalEntityRegistrationCode, StartDate, EndDate | Require one exact active/effective geography-compatible row | Name, IdentifyingFlag, LE registration type code, and legislative context; record a localized UI number label only when separately evidenced and never treat the code as that label; JurisdictionId receipt-only | Zero or many blocks; no list-order or export fallback |
| resolve_enabled_registration_function_code | Function input is supplied for scope assessment | Exact function code or meaning | /crmRestApi/resources/11.13.18.05/fndStaticLookups with finder LookupTypeIsActiveEnabledFinder; BindLookupType=XLE_LE_FUNCTION | LookupCode, Meaning, EnabledFlag | Require one exact enabled code or case-insensitive exact meaning match; known mappings include ICINV, ITC, DAS2, SITC | Enabled code/meaning receipt only; no CREATE value because function scope is blocked | Zero or many confirms invalid input; one match still does not prove jurisdiction permission or authority/site readiness |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Free-text LOV input | Normalize only outer whitespace, require exact eligible cardinality one, follow every page, and never fuzzy-match or select the first row |
| Export use | Use only for current shape, unchanged parent rows, collision/existence checks, verification, and exact legal-address natural-key resolution |
| Function code lookup succeeds | Record the receipt but keep the candidate blocked because XLE_JUR_FUNCTIONS permission and authority/site coupling remain unproven |
| Receipt | Record target, release, as-of, normalized inputs, method/path, requested fields, counts, natural keys, receipt-only IDs, eligibility, derivations, and fingerprint |
| Broader export container | A task-level export must complete successfully. A broader functional-area or offering export may have overall status Completed with errors only when its archive is available, the exact process log identifies every failed object, every object/member required by this task completed successfully with zero failed, warning, or partial rows, every failure is provably outside this task, and target, release, freshness, fingerprint, hierarchy, and headers are verified. Record and disclose the scoped exception; any required-object failure, warning, partial result, missing counter, or indeterminate status blocks. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LER.RESOLVE_REFERENCES | step | 20 | reference_lookup | resolved->LER.CHECK_DEPENDENCIES;blocked->LER.HANDLE_ERROR;failure->LER.HANDLE_ERROR | LER.VALIDATE_INPUT | stop | Resolve every applicable local and live reference |
