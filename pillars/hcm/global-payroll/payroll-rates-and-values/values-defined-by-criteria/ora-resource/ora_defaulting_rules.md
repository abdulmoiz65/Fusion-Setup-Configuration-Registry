# Values Defined by Criteria HDL Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| RetrievalDateType | Effective Date | The user does not supply a retrieval date type and target metadata supports the documented default | Yes | verify_values_defined_by_criteria_metadata |
| Default criterion and value | Include one fallback branch | The business owner has not explicitly accepted a tested non-default design | Yes, only with documented business-owner decision and representative-condition test evidence | verify_hierarchy_design |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| VALUE_BY_CRITERIA.APPLY_DEFAULTS | decision | 40 | apply_default | applied->VALUE_BY_CRITERIA.DESIGN_GATE;not_applicable->VALUE_BY_CRITERIA.DESIGN_GATE;blocked->VALUE_BY_CRITERIA.HANDLE_DESIGN_BLOCKER | VALUE_BY_CRITERIA.RESOLVE_REFERENCES | stop | Apply only the documented retrieval-date and resilient fallback defaults after target evidence is available. |
