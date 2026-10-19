# Configure Public Worker Access Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| IsEnterpriseLevelFlag | true only for the single enterprise configuration | New enterprise-mode configuration | Yes | |
| SecureByUserDefinedFilterFlag | false | Advanced filters are not selected | Yes | |
| IncludeFutureAssignmentFlag | false | New configuration | Yes | |
| SecureByLegalEmployer | N | Own legal employer scenario | No | |
| SecureByUserLegalEmployer | Y | Own legal employer scenario | No | |
| Static legal-employer criterion | N and no legalEmployers criterion | Own legal employer scenario | No | |
| SecureByUserBusinessUnitFlag | true | Own business unit scenario | No | |
| Static business-unit criterion | N and no businessUnits criterion | Own business unit scenario | No | |
| Advanced filter mode | UserDefinedFilter and UserDefinedExpression are null | Advanced filters are not selected | No | |
| Parent criterion flags | N | A matching criterion is not used | Yes | |
| Assignment status Criteria | ORA_SEC_CRIT_ASGN_STATUS | assignmentStatuses criterion is used | No | |
| Business unit Criteria | ORA_SEC_CRIT_BU | businessUnits criterion is used | No | |
| Department Criteria | ORA_SEC_CRIT_DEPT | departments criterion is used | No | |
| Grade Criteria | ORA_SEC_CRIT_GRD | grades criterion is used | No | |
| Job Criteria | ORA_SEC_CRIT_JOB | jobs criterion is used | No | |
| Legal employer Criteria | ORA_SEC_CRIT_LE | legalEmployers criterion is used | No | |
| Person type Criteria | ORA_SEC_CRIT_PT | personTypes criterion is used | No | |
| Person Criteria | ORA_SEC_CRIT_PER | persons criterion is used | No | |
| Criterion Scope | N | No criterion is used | Yes | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PWA.APPLY_DEFAULTS | step | 5 | apply_default | defaulted->PWA.ENFORCE_DESIGN | PWA.RESOLVE_REFERENCES | stop | Resolved package values require documented defaults |
