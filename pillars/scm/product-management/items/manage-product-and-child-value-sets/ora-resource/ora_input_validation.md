# Manage Product and Child Value Sets Input Validation

Validate each requested value set before any setup-data preview. These rules are
based on Oracle Fusion Cloud SCM, *Implementing Product Management*, "Define
Product Child Value Sets," and the current Product Management setup-task
documentation.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Value-set identity | ValueSetCode, Module or ModuleId | Block validation | Provide one value set code and the application module in which it will be used | Every value set request | |
| Validation definition | ValidationType, ValueDataType | Block validation | Provide one supported validation type and one supported value data type | Every value set request | |
| Child subset parent | IndependentValueSetCode, ParentIndependentValueSetCode, or ParentIndependentValueSetModule | Block validation | Provide the independent parent value set that supplies the subset values | ValidationType is Subset | resolve_parent_independent_value_set |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| ValidationType is Subset | Continue only when the selected parent is an exact independent value set in the supplied module | Correct the parent identity or create and populate the independent value set first | resolve_parent_independent_value_set |
| A child value set is requested for SKU variants | Continue only after the independent value set contains the variant values intended for the subset | Populate and verify the independent value set values before defining the subset | resolve_parent_independent_value_set |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| ValueSetCode and Module or ModuleId are nonblank after trim | Reject the request | Every value set request | |
| ValidationType is Format Only, Independent, Dependent, Subset, Table, INDEP, or SUBSET | Reject the request | Every value set request | |
| ValueDataType is Character, Number, Date, Date/Time, or VARCHAR2 | Reject the request | Every value set request | |
| A Subset request identifies one parent independent value set | Block the request | ValidationType is Subset | resolve_parent_independent_value_set |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VSET.VALIDATE_INPUT | step | 10 | validate_input | valid->VSET.RESOLVE_TASK;invalid->VSET.HANDLE_ERROR | none | stop | Before any dependency or design validation |
