# Manage Opportunity Revenue Categories Defaulting Rules

The Common Features standard-lookup contract defaults EnabledFlag to Y when a
new lookup code omits it. This skill
models Disable as an update that sets EnabledFlag to N; it never maps Disable
to DELETE.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
| --- | --- | --- | --- | --- |
| LookupType | MOO_REVN_CATEGORY | Every SingleLookup request; every package row must already carry this exact value | No |  |
| EnabledFlag | Y | A SingleLookup Create request omits EnabledFlag | No |  |
| EnabledFlag | N | A SingleLookup Disable request omits EnabledFlag | No |  |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.REVENUE_CATEGORY.DEFAULT | step | 2 | apply_default | applied->OPP.REVENUE_CATEGORY.VERIFY_TYPE;not_applicable->OPP.REVENUE_CATEGORY.VERIFY_TYPE | OPP.REVENUE_CATEGORY.VALIDATE | stop | Before verifying the fixed MOO_REVN_CATEGORY parent lookup type |
