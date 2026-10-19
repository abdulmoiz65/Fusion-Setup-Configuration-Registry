# Manage Legal Reporting Unit Registrations Reference Lookups

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| resolve_lru_registration_address_exact | Before CREATE | Fresh same-target, scope-complete XLE_LE_LEGAL_ADDRESS.csv; supplied formatted natural key and jurisdiction country | Require one exact active internal address compatible with jurisdiction country; export yields the natural key only | FormattedAddress and receipt-only location semantics | Zero or many blocks; never copy LocationId |
| find_lru_registration_conflict | Before CREATE | Complete target ORA_XLE_LEGAL_REPORTING_UNIT_REGISTRATION.csv scoped to the entity and every sibling LRU; entity, LRU, jurisdiction, number, definition | First compare exact LRU definition, then scan all sibling LRUs for the same jurisdiction and number and existing identifying context | Existing match, sibling collision, identifying conflict, or create-candidacy receipt | Zero collisions is candidacy; same-LRU match, sibling collision, ambiguity, or incomplete scope blocks CREATE |
| verify_lru_registration_package | Before preview | Fresh target ASM, exact unchanged entity and LRU parent rows, registration CSV, and header-only function child | Require exact hierarchy, headers/order, both parents, zero function candidates, unrelated-row preservation, target/release identity, task-scoped successful-status evidence, and fingerprint | Package-shape, ownership, parents, and fingerprint receipt | Stale, partial, child-only, wrong-target, required-object failure or warning, or ambiguous evidence blocks |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| verify_lru_registration_parents | Entity and LRU are supplied | Exact entity identifier or name, exact LRU name, and as-of date | /fscmRestApi/resources/11.13.18.05/legalEntitiesLOV then /fscmRestApi/resources/11.13.18.05/legalReportingUnitsLOV | LegalEntityId, Name, LegalEntityIdentifier, EffectiveFrom, EffectiveTo, LegalReportingUnitId, LegalReportingUnitName, StartDate, EndDate, MainLegalReportingUnitFlag | Require one exact effective entity and one exact effective LRU under its LegalEntityId | LegalEntityIdentifier and LegalReportingUnitName; physical IDs receipt-only | Zero, many, inactive, ineffective, or ownership mismatch blocks |
| resolve_lru_registration_jurisdiction | Jurisdiction is supplied | Exact jurisdiction name, LRU geography, registration type, and as-of date | /fscmRestApi/resources/11.13.18.05/legalJurisdictionsLOV | JurisdictionId, Name, GeographyId, IdentifyingFlag, LegislativeCategoryCode, LegalReportingUnitRegistrationCode, StartDate, EndDate | Require one exact active/effective geography-compatible row | Name, IdentifyingFlag, LRU registration type code, and legislative context; record a localized UI number label only when separately evidenced and never treat the code as that label; physical ID receipt-only | Zero or many blocks; no list-order or export fallback |
| resolve_lru_enabled_function_code | Function input is supplied for scope assessment | Exact function code or meaning | /crmRestApi/resources/11.13.18.05/fndStaticLookups with finder LookupTypeIsActiveEnabledFinder; BindLookupType=XLE_LE_FUNCTION | LookupCode, Meaning, EnabledFlag | Require one exact enabled code or case-insensitive exact meaning match; known mappings include ICINV, ITC, DAS2, SITC | Enabled code/meaning receipt only; no CREATE value because function scope remains blocked | Zero or many confirms invalid input; one still does not prove XLE_JUR_FUNCTIONS permission or authority/site readiness |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Free-text LOV input | Normalize only outer whitespace, require exact active/effective eligible cardinality one, paginate fully, and never fuzzy-match or select first row |
| Two-level parent lookup | Resolve entity first and require LRU LegalEntityId equality; never resolve LRU name globally |
| Export use | Limit to current shape, exact unchanged parents, collision/existence checks, verification, and exact legal-address natural-key resolution |
| Function code lookup succeeds | Record the receipt but keep the branch blocked because jurisdiction permission and authority/site dependency remain unproven |
| Receipt | Record target, release, as-of, normalized inputs, method/path, requested fields, counts, natural keys, receipt-only IDs, eligibility, derivations, and fingerprint |
| Broader export container | A task-level export must complete successfully. A broader functional-area or offering export may have overall status Completed with errors only when its archive is available, the exact process log identifies every failed object, every object/member required by this task completed successfully with zero failed, warning, or partial rows, every failure is provably outside this task, and target, release, freshness, fingerprint, hierarchy, and headers are verified. Record and disclose the scoped exception; any required-object failure, warning, partial result, missing counter, or indeterminate status blocks. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LRUR.RESOLVE_REFERENCES | step | 20 | reference_lookup | resolved->LRUR.CHECK_DEPENDENCIES;blocked->LRUR.HANDLE_ERROR;failure->LRUR.HANDLE_ERROR | LRUR.VALIDATE_INPUT | stop | Resolve every applicable local and live reference |
