# Manage Legal Jurisdictions Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Input and reference gate | Validate required fields and resolve exact geography and lookup codes |
| 2 | Existence gate | Compare the requested definition with existing jurisdictions before any create artifact is generated |
| 3 | Jurisdiction policy gate | Enforce name uniqueness, one category per geography, effective-date integrity, immutable post-create attributes, and identifying-jurisdiction behavior |
| 4 | Date-impact gate | For date changes, prove no active registrations are affected |
| 5 | First-go package gate | Complete the import-readiness record from fresh exported metadata before central Data Loader preview |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Every create or update request | Error | resolve_jurisdiction_geography | Geography is missing, unavailable, ambiguous, or ineffective | Resolve one current geography | Yes |
| Every create or update request | Error | resolve_legislative_category | Legislative Category is absent, disabled, ambiguous, or represented only by an unproven UI label | Resolve its internal code and export evidence | Yes |
| Every create or update request | Error | resolve_legal_entity_registration_code | Legal Entity Registration Code is absent, disabled, ambiguous, or represented only by an unproven UI label | Resolve its internal code and export evidence | Yes |
| Every create or update request | Error | resolve_lru_registration_code | Legal Reporting Unit Registration Code is absent, disabled, ambiguous, or represented only by an unproven UI label | Resolve its internal code and export evidence | Yes |
| Legal Functions supplied | Error | resolve_legal_jurisdiction_function_code | A child row lacks an enabled resolved FunctionCode or its parent geography transients do not match the XLE_JURISDICTION row | Resolve the code and rebuild the matching child row | Yes |
| Before create | Error | find_legal_jurisdiction_existing | Equivalent jurisdiction exists, requested definition conflicts, Name is duplicate, or a verified category already occurs for geography; unavailable canonical mapping excludes only the geography/category subcheck under the task policy | Reuse exact match or obtain an explicit update-versus-new decision | Yes |
| Every identifying create or update | Error | find_legal_jurisdiction_existing | With verified canonical mapping, more than one IdentifyingFlag=Y would remain for a geography, or the expected automatic identifying outcome is not disclosed. Without mapping on a valid create, exclude identifying-impact verification only and retain the warning and generic identifying behavior disclosure | Reconcile the identifying jurisdiction set and disclose that setting Y clears another; if none is Y, Oracle makes the saved jurisdiction identifying | Yes |
| Existing jurisdiction update | Error | find_legal_jurisdiction_existing | Name, Territory/Geography, or Legislative Category changes after creation | Create a new jurisdiction or remove the immutable-field change | Yes |
| Effective-date update | Error | verify_active_jurisdiction_registrations | Start is after end, active registrations exist, or registration clearance is unresolved | Correct dates or obtain authoritative clearance | Yes |
| FSM package preview | Error | verify_jurisdiction_package_baseline | A required member, metadata XML, column, generated/defaulted value, source evidence, or technical default is unresolved | Refresh export and complete the readiness record | Yes |

## Conditional Two-Check Exclusion

Apply the create policy in ora_reference_lookups.md when canonical geography
mapping cannot be verified. Do not request a waiver or claim either check passed.
Retain both warnings in preview and rely on the reviewed import result for the
actual outcome. Do not exclude name, primary geography selection, code, date,
immutable-field, registration, package, or approval validation.

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| resolve_jurisdiction_geography | Every create or update request | Geography natural key and receipt-only ID | ora_reference_lookups.md |
| resolve_legislative_category | Every create or update request | Enabled internal category code | ora_reference_lookups.md |
| resolve_legal_entity_registration_code | Every create or update request | Enabled internal legal-entity registration code | ora_reference_lookups.md |
| resolve_lru_registration_code | Every create or update request | Enabled internal legal-reporting-unit registration code | ora_reference_lookups.md |
| resolve_legal_jurisdiction_function_code | Legal Functions supplied | Enabled internal FunctionCode | ora_reference_lookups.md |
| find_legal_jurisdiction_existing | Before create and policy validation | Existing definitions and identifying set | ora_reference_lookups.md |
| verify_active_jurisdiction_registrations | Date changes | Active-registration clearance | ora_reference_lookups.md |
| verify_jurisdiction_package_baseline | Package readiness | Metadata/template/default evidence and fingerprint | ora_reference_lookups.md |

## Source Mapping

| Decision or Rule | Supporting Source |
|---|---|
| Required fields, unique name, identifying semantics, dates, and registration-code selection | Oracle Financials Create Legal Jurisdictions, Addresses and Authorities: https://docs.oracle.com/en/cloud/saas/financials/26b/faigl/create-legal-jurisdictions-addresses-and-authorities.html |
| Geography relationship, category-code semantics, and jurisdiction ID relationship | Oracle Enterprise Data Model: XLE_JURISDICTIONS_B, https://docs.oracle.com/en/cloud/saas/financials/26a/oedmf/xlejurisdictionsb-25028.html |
| Name maximum length and translation/name uniqueness context | Oracle Enterprise Data Model: XLE_JURISDICTIONS_TL, https://docs.oracle.com/en/cloud/saas/financials/26b/oedmf/xlejurisdictionstl-11172.html |
| Legal entity and legal reporting unit registration dependency | Oracle Financials legal-entity setup and legal-entity registrations guidance; current task reference contracts |
| Lookup endpoints, default policy, approval and first-go readiness | Task-local ora_reference_lookups.md and ora_defaulting_rules.md; core Data Loader and Task Hook contracts; fresh FSM template metadata |
| Exact FSM members, columns, hierarchy order, and available UI function labels | Fresh same-target FSM template/export and current UI evidence |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LJ.ENFORCE_DESIGN | decision | 50 | design_enforcement | passed->LJ.PACKAGE_PREVIEW_GATE;blocked->LJ.HANDLE_ERROR | LJ.APPLY_DEFAULTS | stop | Before final FSM package readiness validation; enforce all applicable checks, retaining the two individually excluded canonical-geography checks as warnings without a readiness override. |
