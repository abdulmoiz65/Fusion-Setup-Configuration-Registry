# Time Layout Sets Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Existing layout | Retrieve all Time Layout Sets pages, evaluate every supplied business attribute including supported child attributes, and select a matching candidate before an update or delete. |
| 2 | Selectable values | Resolve field and category identities before preparing rows. |
| 3 | Web Clock values | Only when a Web Clock Layout is configured, resolve Button Set before Button, then dependent fields. |

## Update Hierarchy Context

For every existing-record update, use the current canonical parent and child
links to construct the complete ancestor chain. The Data Loader source must
contain one `PATCH` row for each ancestor before the changed row. Never submit
a child-only update source.

| Changed section | Required `PATCH` context rows, in order |
|---|---|
| `timeEntryLayout` | `timeLayoutSetsV2` → `timeEntryLayout` |
| `timeCardFields` or `timeTotalsHoursCategories` | `timeLayoutSetsV2` → `timeEntryLayout` → changed child |
| `webClockLayouts` | `timeLayoutSetsV2` → `webClockLayouts` |
| `webClockButtons` | `timeLayoutSetsV2` → `webClockLayouts` → `webClockButtons` |
| `webClockButtonTimecardFields` | `timeLayoutSetsV2` → `webClockLayouts` → `webClockButtons` → changed child |

Each context row retains its current persisted ID and unchanged business values.
Use only returned canonical and child links to determine the chain; do not
construct parent paths or substitute create-only correlations.

## New-Record Data Loader Correlations

For a new Time Layout Set aggregate prepared in one Data Loader DAT, use the live-template-supported local correlations below. They associate rows only within that DAT; they are not persisted Fusion identifiers and must not be replaced by the business codes.

| Level | Local correlation field | Child reference | Rule |
|---|---|---|---|
| Time Layout Set | timeLayoutSetsV2.TimeLayoutSetId | timeEntryLayout.TimeLayoutSetId | Allocate one unique numeric-only local value and repeat it in each new Time Entry Layout row. |
| Time Entry Layout | timeEntryLayout.TimeEntryLayoutId | timeCardFields.TimeEntryLayoutId; timeTotalsHoursCategories.TimeEntryLayoutId | Allocate one different unique numeric-only local value and repeat it in every field and total row for that new layout. |
| Time Layout Set Web Clock branch | timeLayoutSetsV2.TimeLayoutSetId | webClockLayouts.TimeLayoutSetId | When a Web Clock Layout is requested and the live Data Loader template exposes the section, repeat the existing Time Layout Set local correlation in the new Web Clock Layout row. |
| Web Clock Layout | webClockLayouts.WebClockLayoutId | webClockButtons.WebClockLayoutId | When a Web Clock Layout is requested and the live Data Loader template exposes the section, allocate one different unique numeric-only local value and repeat it in every button row for that layout. |
| Web Clock Button | webClockButtons.WebClockButtonId | webClockButtonTimecardFields.WebClockButtonId | When a Web Clock Button is requested and the live Data Loader template exposes the section, allocate one different unique numeric-only local value and repeat it in every button time-card field row for that button. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| TLS_PARENT | Existing layout identity | Yes | Update or delete | Lookup | Fusion REST | search_time_layout_sets_by_criteria | Prevent inferred item keys and ensure every supplied condition is met | Provide one or more business search attributes and select a returned candidate when needed | canonical link and current child snapshot |
| TLS_CREATE_CORRELATIONS | New Time Layout Set aggregate | Yes | Create through Data Loader | Verify | Data Loader DAT local correlations |  | Associate requested Time Entry Layout and Web Clock branches within one flat DAT without using business codes, lookup selection IDs, or persisted Fusion IDs | Use a unique numeric-only local TimeLayoutSetId plus distinct local IDs for each requested Time Entry Layout, Web Clock Layout, and Web Clock Button; omit a Web Clock branch when it is not requested | timeLayoutSetsV2.TimeLayoutSetId; timeEntryLayout.TimeEntryLayoutId; webClockLayouts.WebClockLayoutId; webClockButtons.WebClockButtonId and all documented descendant references |
| TLS_FIELD | Time card field | Yes | A field is selected | Lookup | Fusion REST | resolve_time_card_field | Persisted selection uses a template ID | Provide exact field name | TimeCardFieldTemplateId, Name, Label, Description |
| TLS_CATEGORY | Time category | Yes | Custom total selected | Lookup | Fusion REST | resolve_time_category | Persisted total needs category ID | Provide exact category name | TimeCategoryId and Name |
| TLS_BUTTON | Button Set and Button | Conditional | Web Clock configured | Lookup | Fusion REST | resolve_button_set | Button choices depend on Button Set | Provide both names | ButtonSetId and ButtonId |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | An exact Fusion identity is required | Lookup only |
| Blocked | Required identity is missing or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TLS.CHECK_DEPENDENCIES | step | 20 | resolve_dependency | ready->TLS.RESOLVE_LOOKUPS;blocked->TLS.HANDLE_ERROR | TLS.SEARCH_LAYOUT_SETS | stop | A create, update, or delete request passed the criteria-search or duplicate-check gate |
