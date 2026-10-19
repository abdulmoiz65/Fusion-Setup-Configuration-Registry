# Value Set Value Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---:|---|---|
| 1 | Value-set metadata | Resolve the exact target and its MaximumLength through resolve_value_set |
| 2 | Segment usage context | Use established Structure Instance context when it proves Natural Account usage; otherwise accept an explicit standalone declaration |
| 3 | Verified FBDI package | Prepare a values-only 101-column package with no hierarchy member |
| 4 | Data Loader handoff | Hand the verified package to core/data-loader for preview, approval, import selection, execution, and outcome handling |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| value_set_metadata | Exact named value set | Yes | Before package generation | Lookup | Fusion parent Value Sets collection | resolve_value_set | MaximumLength is required for local value validation | Correct the code or access issue; never guess the target or length | ValueSetId, ValueSetCode, MaximumLength |
| segment_usage | Natural Account context | Yes | Before final candidate validation | Verify | Established Structure Instance context or explicit standalone declaration |  | AccountType requirements depend on this context | Supply or confirm the context when a Natural Account declaration is made | NaturalAccount evidence |
| package_contract | Verified values-only package | Yes | Before Data Loader handoff | Verify | Local prepared candidate |  | Data Loader receives a complete, valid FBDI package | Correct invalid rows or package shape before handoff | ZIP hash, row count, 101-column evidence |
| data_loader_handoff | Approved Data Loader route | Yes | Before live create/update | Blocked | core/data-loader |  | Data Loader owns import selection and execution | Obtain approval of its immutable preview | Target environment, approval evidence, returned outcome |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Required evidence is present and internally consistent | No |
| Lookup | resolve_value_set can supply metadata | Read-only lookup only |
| Blocked | Candidate, package, approval, or Data Loader evidence is missing | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---:|---|---|---|---|---|
| MVS.CLASSIFY | step | 3 | resolve_dependency | classified->MVS.VALIDATE_CLASSIFIED;invalid->MVS.FAILED | MVS.RESOLVE_VALUE_SET | stop | Resolved create/update candidate |
