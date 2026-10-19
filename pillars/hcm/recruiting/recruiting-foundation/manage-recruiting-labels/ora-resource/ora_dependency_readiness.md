# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Current Manage Recruiting Labels FSM data | Export the current FSM data before evaluating a create or update label request. |
| 2 | Site language configuration | Obtain the site base-language code and enabled Fusion language codes before preparing translations. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| current_recruiting_labels | Current Manage Recruiting Labels FSM data | Yes | Every create or update label request | Lookup | Current environment FSM export | export_current_recruiting_labels | Provides the existing LabelName, LabelCode, and translation evidence required for duplicate detection or update identification. | Stop until the current FSM export is available. | Existing LabelName, LabelCode, and translations |
| site_language_configuration | Site language configuration | Yes | Every create or update label request | Lookup | Current Fusion site language configuration | resolve_site_language_configuration | Provides the base-language and enabled-language codes required to prepare translations. | Stop until the site language configuration is available. | Site base-language code and enabled language codes |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Lookup | Current FSM label data is required | Yes |
| Lookup | Site language configuration is required | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| LABELS.ENSURE_CURRENT_LABEL_EXPORT | step | 20 | resolve_dependency | ready->LABELS.EXPORT_CURRENT_LABELS | LABELS.VALIDATE_LABEL_INPUTS | stop | Every create or update label request |
| LABELS.ENSURE_SITE_LANGUAGE_CONFIGURATION | step | 40 | resolve_dependency | ready->LABELS.RESOLVE_SITE_LANGUAGE_CONFIGURATION | LABELS.EXPORT_CURRENT_LABELS | stop | Every create or update label request |
