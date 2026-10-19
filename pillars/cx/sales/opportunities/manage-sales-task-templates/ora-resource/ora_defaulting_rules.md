# Defaulting Rules

Apply only defaults explicitly documented for the Opportunity task-template setup page or the Functional Setup Manager import contract. Preserve an explicit requester choice where Oracle allows it.

`template_set` has no automatic default in this workflow. When it is in scope,
the user must confirm Common Set or select a different exact Set ID or Set Code.

Sources: [Shared task-template fields and defaults](https://docs.oracle.com/cd/G55130_01/trans/F77858-09/getting-started-with-your-partner-relationship-management-implementation.pdf#page=112) and [Create a setup task CSV import](https://docs.oracle.com/en/cloud/saas/applications-common/26b/farca/op-fscmrestapi-resources-11.13.18.05-setuptaskcsvimports-post.html).

The current field/default example is illustrated for Partner Profile. Use its
shared Active, subtype and template-set semantics only. This skill's enclosing
catalog contract fixes Opportunity as the template type and preserves the
Manage Sales Task Templates task and its current exported CSV schema.

## Defaults

| Business Value | Default | Applies When | Can User Override? | Why This Default Is Safe |
|---|---|---|---|---|
| active_flag | Y | change_mode is create_template and no value was supplied | Yes | Oracle documents that Active is selected by default on a new task template. |
| template_type | Opportunity | change_mode is create_template and no value was supplied | No within this task skill | Oracle documents that the business object is defaulted, and this catalog skill is specifically for Opportunity task templates. |
| template_subtype | blank | change_mode is create_template, no subtype was supplied, and assessment_template_flag is not true | Yes, only by explicitly selecting Assessment | Oracle documents a blank subtype as the default and Assessment as the value to select for an assessment template. |
| ConflictId | 0 | Preparing a new ZMM_TASK_TEMPLATE.csv template row and ConflictId is unset | Preserve an explicitly supplied integer; preserve the exported value for an existing template | QA observed JBO-27014 when ConflictId was blank, and an FSM create with 0 succeeded. Write literal CSV value 0; never convert numeric zero to an empty cell through a truthiness check. |
| source_target_diff_ok_flag | N | change_mode is import_task_csv and no value was supplied | No automatic override | Oracle documents N as the default revision-mismatch behavior; the skill must not bypass it merely to continue an import. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SALES_TASK_TEMPLATE.DEFAULTS | step | 2 | apply_default | defaulted->SALES_TASK_TEMPLATE.DEPENDENCY;not_applicable->SALES_TASK_TEMPLATE.DEPENDENCY;invalid->SALES_TASK_TEMPLATE.BLOCKED | SALES_TASK_TEMPLATE.VALIDATE | stop | Before resolving template, reference-data-set, task-detail, sales-stage, or CSV-package dependencies; never default template_set or Common Set. |
