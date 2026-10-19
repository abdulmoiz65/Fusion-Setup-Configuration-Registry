# Configure Legislations for Human Resources Defaults

This file owns omission behavior for Search, Create preparation and Delete.
Lookup mechanics and response-to-field mappings belong to ora_reference_lookups.md.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Optional search filters | Absent; do not infer a text, Predefined, or Implemented criterion | Search and a validated optional filter is absent | No | |
| limit | 25 | Starting any installed-legislation collection traversal; preserve the existing Search page size | No | |
| offset | 0 | Starting a primary, deletion-target, verification, or declared diagnostic traversal | No | |
| InstalledLegislationKey | Resolved legCode; this dummy attribute repeats the exact target code | Delete and the draft value is absent after the resolver succeeds | No | resolve_installed_legislation_for_delete |
| Content-Type | application/vnd.oracle.adf.action+json | Delete and the draft value is absent | No | |
| REST-Framework-Version | 9 | Delete and the draft value is absent | No | |
| RestAction | POST | Delete and the draft value is absent; the business operation is an ADF custom action | No | |
| legislation_name / legCode | No default; require available-legislation selection | Create | No | resolve_available_legislation_for_create |
| Tax Year Start Date | No default; ask the user for month/day | Create and value absent | No | |
| Payroll Relationship Rule | Live Meaning Create New Record, whose returned LookupCode must be I | Create and value absent with no pending option-selection request; default candidate already validated | No | resolve_payroll_relationship_rule |
| Deduction Card - Tax Reporting Unit Association Rule | No default; user must choose from live Meanings | Create and value absent | No | resolve_deduction_card_tru_rule |
| Default Currency | Sole live default candidate for selected legCode | Create and currency omitted | No | resolve_default_currency |
| Payroll Relationship Type Mapping | Complete ordered default mapping candidates | Create and mapping input omitted; explicit row edits apply to these defaults | No | resolve_default_relationship_mappings |
| Explicit mapping replacement | Preserve the supplied final rows, including an explicitly empty list; do not restore removed defaults | Create and user replaces all mappings | No | |
| Default disclosure | Retain a per-field default_used marker for the final summary; no separate confirmation of omitted defaults | Create | No | |

Search never defaults a business record or code. Delete never defaults legCode:
it must come from the selected Fusion record. Conflicting constants or a dummy
key that differs from the selected code fail validation; they are not overwritten.
For phase=validate_artifact, this node computes expected values in task context
only; the next node compares the existing archive and rejects omissions or conflicts.
Pagination after the first page belongs exclusively to ora_reference_lookups.md.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLHR.SEARCH_DEFAULTS | step | 4 | apply_default | applied->CLHR.ENFORCE_SEARCH_SCOPE;unchanged->CLHR.ENFORCE_SEARCH_SCOPE;invalid->CLHR.ERROR | CLHR.SELECT_OPERATION | stop | Search only; initialize omissions and page-start controls without changing supplied filters |
| CLHR.DELETE_DEFAULTS | step | 12 | apply_default | applied->CLHR.VALIDATE_DELETE_CONTRACT;unchanged->CLHR.VALIDATE_DELETE_CONTRACT;invalid->CLHR.ERROR | CLHR.RESOLVE_DELETE_TARGET | stop | Delete only after unique target resolution; compute fixed values without changing a prepared immutable archive |
| CLHR.CREATE_DEFAULTS | step | 63 | apply_default | applied->CLHR.VALIDATE_CREATE_RULE_INPUTS;unchanged->CLHR.VALIDATE_CREATE_RULE_INPUTS;invalid->CLHR.ERROR | CLHR.CREATE_OPTION_REQUEST | stop | Apply only omitted Create values from resolved candidates; preserve invalid explicit values for validation, edited rows and explicit empty replacement; never default date or TRU rule |
