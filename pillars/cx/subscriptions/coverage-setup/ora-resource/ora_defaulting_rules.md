# Default Coverage Defaulting Rules

## Standard Defaults

| Task Code | Task Name | Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Applicable coverage | Customer-level selected Standard Coverage | A Default Coverage is configured for the customer | Yes; customer default values override global defaults for that customer | list_default_coverages |
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | Applicable coverage | Global-level selected Standard Coverage | A global Default Coverage is configured and no customer-level default applies | No; do not replace a customer-level default | list_default_coverages |

## Task Nodes

| Task Code | Task Name | Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|---|---|
| CUSTOM_MANAGE_DEFAULT_COVERAGE | Manage Default Coverage | DEFCOV.APPLY_DEFAULT | decision | 60 | apply_default | customer_default->DEFCOV.CUSTOMER_DEFAULT_APPLIED;global_default->DEFCOV.GLOBAL_DEFAULT_APPLIED;no_applicable_default->DEFCOV.NO_APPLICABLE_DEFAULT | DEFCOV.RESOLVE_DEFAULTS | stop | Applying the configured Default Coverage after the read-only collection lookup returns data |
