# Legal Entity HCM Information Reference Lookups

## Purpose

Own every read-only Fusion lookup used to resolve the Legal Entity, its applicable HCM branches, current EFF metadata and values, value sets, and date-effective history. The registered `ManageLegalEntity` Core Data Loader synchronization is not a lookup; its readiness handoff is owned by `ora_error_handling.md`.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_legal_entity_exact | Every read or mutation precheck | Legal Entity Name or LegalEntityIdentifier | /hcmRestApi/resources/latest/hcmLegalEntities/action/findByAdvancedSearchQuery using the declared read-only advanced-search action | Name, LegalEntityId, LegalEntityIdentifier, LegalEmployerFlag, PsuFlag, legislation and current effective facts | Follow pagination and require exactly one normalized exact Name or identifier match | Current Legal Entity identity, routing flags, and synchronization input | Stop and request a unique business identifier |
| resolve_legal_entity_hcm_roots | Synchronization is recorded complete | Fresh LegalEntityId, current routing flags, and effective read date | `/hcmRestApi/resources/latest/legalEmployers?q=LegalEntityId={LegalEntityId}&limit=500` and/or `/hcmRestApi/resources/latest/payrollStatutoryUnits?q=LegalEntityId={LegalEntityId}&limit=500` | Name, LegalEntityId, OrganizationId, CategoryCode, ClassificationCode, effective dates, status, legislation, EFF envelope, canonical links | Require exactly one row whose LegalEntityId equals the fresh lookup value and whose effective range covers the selected read date for every applicable branch; use that returned OrganizationId and require shared Basic details to agree when both apply | Applicable Legal Employer and/or PSU roots, returned OrganizationId, selected boundaries, exact CategoryCode, EFF envelopes, and all required root locators: OrgUnitClassificationId, OrganizationEffectiveStartDate, OrgUnitClassEffectiveStartDate, and OrgUnitClassEffectiveEndDate | Stop; do not substitute a LegalEntityId for OrganizationId, one branch for the other, guess a localization suffix, or reuse links from another effective row |
| resolve_legal_entity_eff_metadata | A branch, view, edit, deletion precheck, or verification needs EFF metadata | Applicable root and exact CategoryCode | /hcmRestApi/resources/latest/legalEmployers/describe?polymorphicType=legalEmployers.legalEmployersEFF:{CategoryCode} or /hcmRestApi/resources/latest/payrollStatutoryUnits/describe?polymorphicType=payrollStatutoryUnits.payrollStatutoryUnitsEFF:{CategoryCode} | Business categories, contexts, labels, schemas, cardinality, attribute types, updateability, and value-set contracts | Environment, resource, and exact CategoryCode must match the selected branch | Current category/context mapping, attributes, labels, cardinality, updateability, and value-set requirements | Stop; never append or guess a CategoryCode suffix or writable field |
| resolve_legal_entity_eff_context | A requested/default context, mutation precheck, or verification read is required | Link-bearing EFF envelope from the selected-date root, exact describe, category/context request, and row selector when multirow | Follow the returned legalEmployersEFF or payrollStatutoryUnitsEFF item link and then the exact describe-matched child href | Business values, display companions, OrgInformationId, EffectiveStartDate, EffectiveEndDate, row identity, and canonical links | For View, zero rows retain a describe-backed Not configured context; otherwise require the exact branch/category/context and, for multirow contexts, one exact selected row | Business values, row existence, row cardinality, selected context row and its effective dates, or the describe-backed empty-context result | Stop on stale, reconstructed, or ambiguous links or rows; a zero-row collection is valid for View and must not be treated as a missing link |
| resolve_legal_entity_eff_value_set | A proposed EFF value has a describe-declared value set | Value-set contract and proposed business value | Exact read-only LOV or value-set path returned by current describe metadata | Stored value, display value, enabled status, and effective dates when supplied | Require one exact enabled stored or display-value match | Canonical stored value and display companion | Stop; do not send an unverified or disabled value |
| resolve_legal_entity_hcm_history | Date-effective deletion or deletion verification is requested | Fresh synchronized OrganizationId | /hcmRestApi/resources/latest/hcmDateEffectiveObjectHistory with the HcmLeLruOrganizationHistoryDef history definition and full pagination | EffectiveStartDate, EffectiveEndDate, FirstSplitFlag, SecondaryObjectId, ChangedAttributes, DEHLastUpdateDate, and DEHLastUpdatedBy | Select only the greatest current start whose range covers today, require FirstSplitFlag=false and a predecessor, and preserve the complete ordered before-history fingerprint | Selected range, predecessor range, row count, and before-history evidence used to bind the loader preview | Stop on missing pages, first/only row, historical/future selection, or ambiguity |
| resolve_legal_entity_loader_contract | A supported mutation is being prepared | legalEmployersEFF, payrollStatutoryUnitsEFF, or both in manifest order with their embedded ModifyOrganizationUnitForChildCorrect correction action or SplitOrganizationUnitForEFFUpdate dated-update action; DeleteOrganizationUnitForDTDelete only for date-effective parent deletion | Core Data Loader read-only business-object metadata, UCM template, child components, and attribute metadata | Registered discriminator, template member, section hierarchy, keys, attributes, operation fields, action sections, and source-reference columns | Require each selected EFF object and its exact embedded action section to be supported by its current live template; do not infer parity from another object | Selected objects, exact DAT schema, embedded action contract, and immutable-source requirements | Stop with a catalog-mismatch or readiness blocker; never fall back to direct REST mutation |

## Legal Entity Advanced-Search Request Contract

For `find_legal_entity_exact`, send one read-only POST to
`/hcmRestApi/resources/latest/hcmLegalEntities/action/findByAdvancedSearchQuery`
with `Content-Type: application/vnd.oracle.adf.action+json`. Use this verified
request shape, replacing only the search value:

```json
{
  "query": "<name-or-identifier-fragment>",
  "displayFields": [
    "Name",
    "LegalEmployerFlag",
    "PsuFlag",
    "ParentPsuName",
    "LegalEntityIdentifier",
    "EffectiveFrom",
    "EffectiveTo",
    "LegalEntityId"
  ],
  "searchFields": ["Name", "LegalEntityIdentifier"],
  "limit": "500",
  "filters": [],
  "offset": 0
}
```

Although the generic action metadata labels these parameters optional, do not
omit `displayFields`, `searchFields`, `limit`, `filters`, or `offset`: this
tenant rejects sparse payloads with HTTP 400 and no diagnostic body. Treat the
POST as read-only search behavior, paginate if `hasMore` is true, and accept
only one exact normalized `Name` or `LegalEntityIdentifier` after local
matching.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| One Legal Entity matches | Retain only its fresh identity and routing facts; continue to synchronization readiness |
| Synchronization outcome is uncertain | Reconcile through fresh advanced search and roots; do not invoke the action again automatically |
| Synchronization is complete | Query each applicable root with `q=LegalEntityId={LegalEntityId}`; retain its returned OrganizationId only after the exact LegalEntityId and effective-range match |
| LegalEmployerFlag is Y | Resolve the Legal Employer root and legalEmployersEFF branch |
| PsuFlag is Y | Resolve the Payroll Statutory Unit root and payrollStatutoryUnitsEFF branch |
| Both flags are Y | Resolve both branches independently and require shared Basic details to agree |
| Neither requested branch applies | Stop with a branch-readiness error; do not change classification flags |
| A read omits an effective date | Use today's system date for the top-level applicable-root GET |
| A read supplies an effective date | Normalize it to YYYY-MM-DD, retain only the `q=LegalEntityId` root row whose returned effective range covers that date, and follow only that row's returned links |
| A generic Legal Employer view is requested | Return only contexts currently assigned to Legal Employer Details, under `EFF Name: Legal Employer HCM Information` after the Legal Employer details |
| A generic PSU view is requested | Return only the current information category containing PER_PSU_PAYROLL_INFO, under `EFF Name: Payroll Statutory Unit HCM Information` after the Payroll Statutory Unit details |
| A context is rendered for View | Render its business label as a heading and list only configured business segments using display values; do not expose technical names, identifiers, or audit fields |
| A describe-backed View context has zero rows | Render its business-label heading followed by `No configured segments`; do not report a retrieval failure or enumerate empty segment fields |
| Edit operation mode is required | Compare the requested operation EffectiveStartDate with the affected legalEmployersEFF or payrollStatutoryUnitsEFF top-level organization's current EffectiveStartDate. Equality selects `RangeMode=CORRECTION` and ModifyOrganizationUnitForChildCorrect; a later date selects `RangeMode=UPDATE` and SplitOrganizationUnitForEFFUpdate; an earlier date is invalid. Apply the same comparison when the EFF child context is new. OrganizationEffectiveStartDate and OrgUnitClassEffectiveStartDate are locators and must not choose the mode |
| Parent date-effective delete is required | Use the synchronized OrganizationId and selected complete-history EffectiveStartDate as organizationId and effectiveStartDate in DeleteOrganizationUnitForDTDelete; do not substitute an EFF child date or add EFF/root locator identifiers |
| Loader metadata differs from task guidance | The current live registered object and template govern the handoff; stop when the requested operation cannot be proven |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LE.SEARCH | decision | 2 | reference_lookup | unique->LE.SYNC_GATE;none->LE.ERROR;many->LE.ERROR;failed->LE.ERROR | LE.VALIDATE | stop | A read or mutation precheck requires one exact Legal Entity |
| LE.ROOTS | decision | 5 | reference_lookup | view->LE.METADATA;mutation->LE.METADATA;delete->LE.HISTORY;failed->LE.ERROR | LE.SYNC_GATE | stop | Synchronization is recorded complete and effective-date-aware applicable HCM roots must be resolved |
| LE.METADATA | decision | 6 | reference_lookup | resolved->LE.CONTEXT;failed->LE.ERROR | LE.ROOTS | stop | Every read or mutation context requires exact EFF metadata |
| LE.CONTEXT | decision | 7 | reference_lookup | resolved->LE.VALUESET;empty_view->LE.DEPENDENCIES;no_value_set->LE.DEPENDENCIES;shown->LE.DEPENDENCIES;failed->LE.ERROR | LE.METADATA | stop | A requested/default context, mutation precheck, or verification read is required |
| LE.HISTORY | decision | 8 | reference_lookup | selected->LE.DEPENDENCIES;unsupported->LE.BLOCKED;failed->LE.ERROR | LE.ROOTS | stop | Date-effective deletion or verification is requested |
| LE.VALUESET | decision | 9 | reference_lookup | resolved->LE.DEPENDENCIES;failed->LE.ERROR | LE.CONTEXT | stop | A proposed EFF value has a describe-declared value set |
