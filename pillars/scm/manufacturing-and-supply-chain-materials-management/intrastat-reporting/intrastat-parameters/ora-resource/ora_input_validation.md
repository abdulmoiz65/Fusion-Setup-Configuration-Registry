# Intrastat Parameters UI Input Mapping

## UI Label Mappings

Use these approved aliases for the intrastatParameters BO. This table maps field names only; it does not resolve display values to IDs or codes.

| UI Label | BO Attribute |
|---|---|
| Legal Reporting Unit | LRUName |
| Country | TerritoryName |
| Economic Zone | EconomicZone |
| VAT Registration | VATRegistrationNumber |
| Reporting Calendar | ReportingCalender |
| From Period | StartPeriodName |
| To Period | EndPeriodName |
| Validation Rules | ValidationRuleSetCode |
| Supplementary UOM Rules | SuppUOMRuleSetCode |
| Fiscal Regime | FiscalRegimeRuleSetCode |
| Nature of Transaction Codes | NotcRuleSetCode |
| Exclusion Rules | ExclusionRuleSetCode |
| Statistical value calculation rule | StatValCalculationRuleSetCode |
| Statistical code rules | StatisticalRuleSetCode |
| Exclude Dispatches From | ExcludesDispatchFromName |
| Exclude Arrivals To | ExcludesArrivalToName |
| Tax Office Code | TaxOfficeCode |
| Tax Office Name | TaxOfficeName |
| Tax Office Location | TaxOfficeLocationName |
| Branch Reference | BranchReferenceText |
| Email | ContactEmail |
| Contact | ContactName |
| Contact Phone | ContactPhone |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Approved UI label | Trim outer whitespace and compare labels case-insensitively against UI Label Mappings. Rename to the exact BO Attribute. Keep already canonical BO names unchanged. Unknown labels require Data Loader mapping review; do not guess. | Preparing user input or reviewing incoming task data | |
| Duplicate target | If an alias and canonical attribute, or multiple source headers, map to the same target, stop for reconciliation before preparation. Never silently overwrite a value. | Multiple inputs target one BO attribute | |
| Null and omitted values | Preserve explicit null values in normalized input; retain their mapping even when null. Preserve absent attributes as absent. Let Data Loader's supported serialization and Fusion determine runtime null behavior; never equate null with permission to exclude the field. | Normalizing values | |
| Reporting calendar meaning | Reporting Calendar maps to ReportingCalender, preserving the BO spelling. The value must be the calendar display name, UserPeriodSetName; do not assume it equals PeriodSetName or split it into a calendar name and period type. BO/Fusion owns resolution to PeriodSetName and PeriodType. | Reporting Calendar or ReportingCalender is supplied | |
| Country context | Country maps to TerritoryName as supplied context, not TerritoryCode. Do not convert a country name to a code here. Country need not be requested when omitted because Fusion derives it from the selected LRU; backend handling of supplied context remains authoritative. | Country is supplied or omitted | |
| Value preservation | Preserve names, rule codes, IDs, and scalar types without inventing values or adding local defaults. Leave backend required-field and domain validation to BO/Data Loader/Fusion. | All normalized input | |

## Data Loader Mapping Handoff

Apply the alias table before sample generation or Mapping stage, because that stage precedes Task Hook validation. For structured input, prepare canonical BO attribute keys before passing populate-json input. For an existing CSV/XLSX source, preserve its bytes and use the supported explicit mapping edits for the actual source headers. Validate every target against live BO metadata through the normal Data Loader workflow; an absent target blocks preparation.

Examples for the three reported mappings:

```text
--mapping-edit 'intrastatParameters/Fiscal Regime=FiscalRegimeRuleSetCode'
--mapping-edit 'intrastatParameters/Nature of Transaction Codes=NotcRuleSetCode'
--mapping-edit 'intrastatParameters/Statistical code rules=StatisticalRuleSetCode'
```

Use SECTION/SOURCE=ATTRIBUTE in the same way for each supplied alias, using its actual source-header spelling. These are explicit reviewed mappings, not an instruction to bypass Data Loader mapping validation, preview, or approval.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INTRASTAT_PARAMETERS.NORMALIZE_UI_LABELS | decision | 5 | validate_input | valid->INTRASTAT_PARAMETERS.RESOLVE_EXCLUSIONS;blocked->INTRASTAT_PARAMETERS.RETURN_ISSUES;failure->INTRASTAT_PARAMETERS.RETURN_ISSUES | none | stop | Apply approved UI aliases and preserve values; verify canonical input is unchanged when normalization already ran before Data Loader Mapping stage. |
