# Manage Legal Jurisdictions Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Guided reference discovery | For incomplete creates, display Territory and then all remaining code choices before requesting selections or exporting a template |
| 2 | Geography and lookup codes | Resolve geography, legislative category, and both registration-code values exactly |
| 3 | Current task export | Export current FSM metadata and CSV templates only after required selections are complete and before deriving package values; a header-only template plus reusable default policy is sufficient, without a populated full-data export |
| 4 | Existing jurisdiction | Check name before create. Check geography/category and identifying impact only with verified canonical mapping; otherwise exclude just those two checks with warnings under the task policy |
| 5 | Registration impact | Before date changes, prove active registrations will not be affected |
| 6 | Legal Functions | Resolve each optional function to an enabled FunctionCode and create the matching child row, or preserve the header-only child file |
| 7 | Final readiness record | Reconcile every package member, column, value, source, and unresolved item before central import preview |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| lj_baseline | Current FSM package baseline | Yes | Every FSM package request | Verify | Fresh task export | verify_jurisdiction_package_baseline | Defines accepted package shape and technical defaults | Export first; preserve source evidence | Members, metadata, headers, defaults, fingerprint |
| lj_geography | Existing geography | Yes | Every create or update request | Lookup | Geography LOV | resolve_jurisdiction_geography | A jurisdiction is tied to a geography | Supply exact territory/geography | Geography natural key and receipt-only ID |
| lj_category | Enabled legislative category | Yes | Every create or update request | Lookup | LEGISLATIVE_CATEGORY lookup | resolve_legislative_category | Category must be valid and unique within geography | Supply category code or exact meaning | Internal category code |
| lj_le_reg_code | Enabled legal-entity registration code | Yes | Every create or update request | Lookup | XLE_REG_CODE lookup | resolve_legal_entity_registration_code | Registration code must be a supported code | Supply exact code or meaning | Internal registration code |
| lj_lru_reg_code | Enabled legal-reporting-unit registration code | Yes | Every create or update request | Lookup | XLE_REG_CODE_EST lookup | resolve_lru_registration_code | Registration code must be a supported code | Supply exact code or meaning | Internal registration code |
| lj_function | Legal Function code | Yes | A Legal Function is supplied | Lookup | XLE_LE_FUNCTION static lookup | resolve_legal_jurisdiction_function_code | Child CSV requires FunctionCode, not displayed function text | Supply exact code or displayed name | Internal FunctionCode |
| lj_existing | Existing jurisdiction comparison | Yes for name; conditional for the two canonical-geography checks | Before create or immutable-field update | Verify | Legal Jurisdictions LOV | find_legal_jurisdiction_existing | Prevent duplicate or contradictory setup data | Reuse an exact match; decide explicitly on a difference | Existing definition or create candidacy |
| lj_registrations | Active registration clearance | Yes | End date or start-date change | Verify | Fresh same-target legal-entity and legal-reporting-unit registration exports | verify_active_jurisdiction_registrations | Active registrations cannot be invalidated | Provide current registration-clearance evidence | Clearance receipt |

## Canonical Mapping Capability

Follow the two-check exclusion policy in ora_reference_lookups.md. Unavailable
canonical mapping does not block a valid create merely for geography/category
or identifying-impact prechecks. Retain individual not_applicable findings and
warning evidence; all other dependencies remain required. Known conflicts,
failed lookups, and incomplete paging are not mapping-capability exclusions.

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required evidence is current, exact, and complete | Continue |
| Lookup | A documented read-only service is required | Read-only only |
| Verify | Export, existence, or impact evidence must be checked | Local verification only |
| Technical lookup gap | A required supported lookup contract is unresolved | No |
| Business decision | An existing definition differs from the requested definition | No, pending user decision |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LJ.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->LJ.APPLY_DEFAULTS;blocked->LJ.HANDLE_ERROR | LJ.RESOLVE_REFERENCES | stop | After references resolve; require name validation, and record geography/category and identifying-impact checks as not_applicable warnings only when canonical mapping is unavailable for a valid create under the two-check policy. |
