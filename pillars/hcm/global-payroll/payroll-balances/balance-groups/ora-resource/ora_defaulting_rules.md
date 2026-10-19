# Balance Groups FSM Defaulting Rules

## Supported Parent-Only Preparation

Use the user's supplied values first. For a new Employee-level group with no requested children, the successful FSM CSV import establishes the minimal parent contract below. Do not require another populated CSV sample or a mapping waiver for this same contract. Use the actual task template, keep all its columns and companion files, and prepare one row in ORA_PAY_BALANCE_GROUP.csv.

These are CSV preparation defaults, not assertions about values generated or stored by Fusion. In particular, a blank restriction flag does not prove that Fusion stores N. This contract does not establish Payroll-level mappings, update/clear semantics, or child setup defaults.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| dataloader_import_mode | FSM | Routing the Balance Groups task | No | |
| businessObject | Empty; no registered Data Loader business object | Routing the Balance Groups task | No | |
| GroupName | No default; use the supplied Balance Group Name | Every create | No | |
| LegislativeDataGroupName | No default; use the supplied LDG name, verified by the reference lookup | Every create | No | |
| Description | Preserve the supplied description; blank when omitted | Parent-only Employee create | No | |
| GroupLevelFlag | N when the supplied Balance Group Level is Employee; Y when it is Organization | Whenever the supplied level is Employee or Organization; a conflicting explicitly supplied raw flag requires clarification | No | |
| BalanceDimensionAttFlag | Blank CSV cell when unspecified | Parent-only Employee create with no requested restrictions | No | |
| BalanceCategoryAttFlag | Blank CSV cell when unspecified | Parent-only Employee create with no requested restrictions | No | |
| ViewInstanceName | Blank CSV cell when unspecified | Parent-only Employee create | No | |
| GroupingKey | Blank CSV cell when unspecified | Parent-only Employee create | No | |
| BaseGroupName | Blank CSV cell when unspecified | Parent-only Employee create | No | |
| LegislationCode | Blank CSV cell when unspecified; the resolved legislation still supplies reference lookup parameters | Parent-only Employee create | No | |
| BalanceGroupId | Blank CSV cell when unspecified; do not invent a new parent ID | Parent-only Employee create | No | |
| LegislativeDataGroupId | Blank CSV cell when unspecified; the verified LDG name identifies the CSV row and the resolved ID supplies reference lookup parameters | Parent-only Employee create | No | |
| Child CSV rows | Zero rows in ORA_PAY_BAL_ATT_DEFINITION.csv, ORA_PAY_BAL_GRP_INCLUSION.csv, ORA_PAY_BALANCE_ATTRIBUTE.csv and ORA_PAY_BAL_ATT_DEFAULT.csv; retain each heading row | Parent-only create with no requested child setup | No | |
| Other supplied values | Preserve explicit supplied values; validate their template contract before use | Any explicit value outside the minimal parent contract | No | |
| New supporting definition name | Requested Balance Group Name for both BaseAttributeName and UserAttributeName when no explicit definition name is supplied | Existing Employee-group update with a complete empty linked-definition lookup; supported combined child or empty-group restriction profile | No | find_balance_group_attribute_links |
| New supporting definition Alterable | Y | New definition prepared by the supported combined profile | No | |
| New supporting definition restrictions | Literal #null for BalanceCategoryId and BalanceDimensionId; other restriction reference columns empty | New definition with no requested restrictions in the supported combined profile; never apply to clearing existing definitions | No | |
| Combined-profile category dates | 0001-01-01 and 4712-12-31 as CSV preparation defaults when unspecified | Supported combined profile with a US legislation category without an LDG and a shared dimension with blank legislation/LDG; preserve any supplied or authoritatively resolved different dates | No | |
| Combined-profile dimension base name | Empty CSV cell; use the exact resolved BalanceDimensionId | Supported combined numeric-dimension profile only | No | resolve_default_inclusion_employee_dimension |
| Restriction-profile category dates | 0001/01/01 and 4712/12/31 when unspecified | Matched developer-confirmed empty-group restriction profile for Employee Tax Credits; preserve an authoritative different date or explicit user value | No | |
| Restriction-profile category qualifiers | Empty category legislation and LDG names; category LDG ID #null | Matched exported base-category reference in Supported Empty-Group Restriction Preparation; do not copy the LOV override legislation into this already-evidenced base reference or apply this default to arbitrary categories | No | resolve_default_inclusion_balance_category |
| Restriction-profile dimension base name | Empty CSV cell; retain the exact resolved BalanceDimensionId and #null dimension LDG ID | Matched empty-group restriction profile with the evidenced shared dimension and blank reference qualifiers | No | resolve_default_inclusion_employee_dimension |

Blank means an empty CSV cell, written as an empty quoted field when using the exported quoted CSV format. Do not substitute literal null, #null, zero, or a generated value. Keep ASM_SETUP_CSV_METADATA.xml unchanged and retain the original member names and column order. Fields returned by a reference lookup are validation evidence; they do not automatically populate blank CSV columns.

The source of the supplied business values is the user's request. The source of the Employee parent preparation contract is the developer-approved minimal CSV and its completed successful import in this session. The Employee and Organization GroupLevelFlag mappings are explicitly supplied by the developer. No runtime lookup is needed to choose these documented preparation defaults; LDG and duplicate verification remain separate mandatory reference lookups.

Do not default a missing group name, LDG, or level. Do not add unrequested business selections, restrictions or usages. Include the supporting definition and group link required by requested children under the supported combined profile; these are preparation dependencies, not additional business selections. Preserve explicit user choices and stop on conflicts or unsupported mappings. Apply defaults during archive preparation, before the immutable Data Loader preflight; during Task Hook execution verify the already-prepared archive against these rules without modifying it. A changed archive restarts preparation and approval.

## Successful Child Values and Default Boundaries

The earlier named-reference import and the subsequently successful combined component log establish the profiles in ora_reference_lookups.md. Reuse their field patterns without a new experimental-mapping waiver. The combined-profile dates above are preparation defaults requested for reuse, not claims about every category's stored effective dates. Preserve authoritative dates and explicit user values; outside the documented scope resolve the applicable mapping. Never default an existing AttDefBaseName from AttributeId. New definition names follow the explicit authoring default above; reuse existing definitions rather than recreating them. Apply defaults before immutable preflight and only verify them during Task Hook execution.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BG.APPLY_DEFAULTS | decision | 2 | apply_default | applied->BG.RESOLVE_REFERENCES;not_required->BG.RESOLVE_REFERENCES;blocked->BG.HANDLE_ERROR | BG.VALIDATE_INPUT | stop | Apply or verify the documented GroupLevelFlag mapping when Employee or Organization is supplied and the remaining defaults only when their stated conditions apply; return not_required only when no documented rule applies and preserve the supplied contract; never mutate an immutable preflight artifact |

## Sources

- Developer request: use FSM setup import with no Data Loader business-object selection, 2026-10-08.
- Developer-supplied FSM configuration-package ZIP, inspected 2026-10-08. Only component and field names are retained here; exported setup values are not repository fixtures.
- The enclosing task SKILL.md owns the FSM CSV import contract and core.data-loader handoff.
- Developer-approved minimal FSM CSV and completed import, 2026-10-09: one BalanceGroup row succeeded, zero failed, zero warnings; child components processed zero rows. The row populated GroupName, LegislativeDataGroupName, Description and GroupLevelFlag=N; the eight other parent columns were blank. No customer names, identifiers or credentials are retained here.
- Developer request, 2026-10-09: reuse the successful supplied-values-first behavior and defaults in this task skill. This replaces the earlier requirement for a separate populated example for the same parent-only Employee mapping.
- Developer request, 2026-10-09: map Employee to GroupLevelFlag=N and Organization to GroupLevelFlag=Y.
- Developer-approved default-inclusion trials and failed import logs, 2026-10-09; trial dates and attribute-definition identity were not established as successful child defaults.
- Subsequent developer-confirmed corrected default-inclusion success, 2026-10-09: accepts the successful target profile without creating universal category-date or attribute-base-name defaults.

- Developer-requested automatic combined child preparation, 2026-10-09, backed by the approved FSM CSV archive and retrieved successful component ProcessLog: one BalanceAttributeDefinition, one BalanceAttribute and one BalanceAttributeDefault processed with zero failures/warnings; the archive also contained their BalanceGroupInclusion link. No customer identifiers are retained here.
