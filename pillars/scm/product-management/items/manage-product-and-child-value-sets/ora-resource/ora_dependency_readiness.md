# Manage Product and Child Value Sets Dependency Readiness

Oracle defines a child value set by first creating an independent value set,
adding its values, and then creating a Subset value set that references it.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Value-set definition | Establish the value set code, module, validation type, and value data type |
| 2 | Independent parent | For a child subset, create and populate one independent parent value set |
| 3 | Parent verification | Resolve the exact independent parent in the same supplied module |
| 4 | Child subset | Define the subset against the verified parent |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| vset_identity | Value-set identity and validation definition | Yes | Always | Satisfied | Normalized request | | A value set is defined by its code for an application module and its validation and data type | Provide the complete definition | ValueSetCode, Module, ValidationType, ValueDataType |
| vset_independent_parent | Independent parent value set and values | Yes | ValidationType is Subset | Verify | Product Management flexfield metadata | resolve_parent_independent_value_set | Oracle child-value-set guidance requires an independent value set with values before the subset | Provide the parent code and module; correct or populate the parent when it does not qualify | ParentIndependentValueSetCode, ParentIndependentValueSetModule, parent receipt |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | The normalized request contains the required definition | Continue |
| Verify | A subset parent must be confirmed from the documented metadata source | Read-only lookup only |
| Blocked | A required definition or qualifying parent is missing or ambiguous | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VSET.CHECK_DEPENDENCIES | decision | 30 | resolve_dependency | ready->VSET.ENFORCE_DESIGN;blocked->VSET.HANDLE_ERROR | VSET.RESOLVE_PARENT | stop | After parent resolution and before design enforcement |
