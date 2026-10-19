# Maintenance Cloud Algorithm Error Handling

## Scope

This resource owns task-specific blocker classification, safe disclosure, execution gates, and refusal behavior. It does not authorize live algorithm mutation, Maintenance interface import, scheduled-process submission, or process polling.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Algorithm mutation or import contract is missing | Report blocked with missing execution contract; do not create an algorithm artifact or run a live operation |
| Required subscription coverage evidence is missing | Ask for the active subscription, coverage product, covered levels, and maintenance program template evidence |
| Service Mapping handoff is missing or ambiguous | Return the source alias, type, access, or publication question to the caller before algorithm proposal |
| Target field is undocumented or unsupported | Show the affected target field and restrict the proposal to documented MNT_PROGRAMS_INT or MNT_WORK_REQUIREMENTS_INT fields |
| Enumerated target value is unresolved | Stop before proposal approval and request release-matched accepted values |
| Scheduled process evidence is incomplete | Report transfer validation incomplete; do not rerun, retry, or poll any process from this task |
| Oracle process or interface row result is supplied as failed | Preserve supplied request ID, batch, header, program, requirement, status, error text, and safe next action |
| Algorithm XML generation is requested before exact Groovy approval | Return the complete Groovy proposal for approval first; do not create or update `Algorithm_BO.xml` in the same step as first-time draft generation |
| Approval is absent, stale, or broader than the current proposal | Block artifact creation or live change and request approval for the exact current proposal |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing phase, algorithm artifact, source handoff, target mapping, approval, or process evidence | Ask for the exact missing current input |
| Catalog mismatch | Requested task, folder, or task code differs from the selected nested skill | Correct routing without changing generated metadata |
| Documentation gap | Public Oracle docs describe context or target data model but not executable mutation, lookup, or import contract | Record the missing contract and keep the task incomplete |
| Auth/authz | A documented lookup or process cannot be read due to missing privilege | Report the environment, operation, and required privilege without retrying |
| Fusion API | A documented read-only lookup fails | Preserve sanitized status, request path, and next owner; no substitute route |
| Process timeout | A supplied scheduled process request does not finish in the expected window | Preserve request ID, last status, elapsed wait, and next-check owner |
| Process failed | A supplied scheduled process or interface result reports errors | Preserve partial result and errors; request supported diagnostic log workflow |
| Approval blocker | Approval is missing, stale, ambiguous, or not scoped to the current artifact and target | Reapprove the exact proposal after current validation passes |
| Unsupported operation | User asks this task to run live mutation, import, ESS submission, polling, direct SQL, or direct table update | Return unsupported operation and missing contract |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Every result | Task code, task name, rule phase, evaluated checks, not-applicable checks, unresolved live contracts, and safe next action |
| Draft proposal | Source aliases, target interface fields, data type and length checks, row linkage strategy, unresolved accepted values, and remaining execution gaps |
| Approval gate | Exact target environment, current source fingerprints, proposal version, approved target fields, and explicitly excluded live actions |
| Transfer validation | The three scheduled process names, request identifiers, batch or header identifiers, target Maintenance evidence, and any errors or warnings supplied |
| Registry readiness | Readiness covers only authored task-node structure; runtime lookup endpoints, mutation route, approval, and process contracts remain independent gates |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Table documentation is available | Do not treat table documentation as permission for direct SQL, direct REST mutation, or automatic import |
| dataloader_import_mode is REST but businessObject is empty | Do not infer a Data Loader REST business object or sample-generation route for this task |
| Subscription is active | Do not claim Maintenance Cloud integration success without correlated scheduled-process and target result evidence |
| User asks to run a scheduled process | Do not run, rerun, poll, or retry the process from this authoring task |
| Lookup endpoint is TBD | Do not use browser navigation, ad hoc REST, SQL, or another tool to replace the missing resolver contract |
| Approval is broad or stale | Do not apply it to a changed proposal, a different environment, or an unlisted target field |
| Groovy has not been explicitly approved | Do not generate or update `Algorithm_BO.xml`; provide the Groovy proposal and wait for approval of that exact draft |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTALG.CHECK_EXECUTION_CONTRACT | decision | 50 | execution_gate | ready->MNTALG.RETURN_RULE_RESULTS;blocked->MNTALG.REPORT_ISSUES;unsupported->MNTALG.RETURN_UNSUPPORTED | MNTALG.ENFORCE_DESIGN | stop | Gate exact algorithm mutation, artifact creation, approval, live execution, process validation, and unsupported-operation requests. |
| MNTALG.RETURN_RULE_RESULTS | terminal | 60 | terminal | none | MNTALG.CHECK_EXECUTION_CONTRACT | stop | Return validation and design findings for the current checkpoint; this is not proof of deployed algorithm or Maintenance Cloud transfer success. |
| MNTALG.REPORT_ISSUES | step | 70 | error_handler | reported->RETURN_ISSUES | none | stop | Classify blockers, missing contracts, failed evidence, or unsupported requests and return the safe next action. |
| RETURN_ISSUES | terminal | 80 | terminal | none | none | stop | Return blocking findings without retrying lookups, imports, mutations, or scheduled processes. |
| MNTALG.RETURN_UNSUPPORTED | terminal | 90 | terminal | none | none | stop | Refuse unsupported live operations and identify the missing contract or owning workflow. |
