# Maintenance Cloud Service Mapping Error Handling

## Scope

This resource owns Service Mapping blocker classification, disclosure, execution gating, and refusal behavior. It does not authorize Service Mapping update, publish, algorithm mutation, Maintenance interface import, scheduled-process submission, or process polling.

## Error Situations

| Situation | What Should Happen |
|---|---|
| Service Mapping artifact or lookup contract is missing | Report blocked with missing Service Mapping evidence; do not recommend source aliases as confirmed |
| Subscription coverage context is missing | Ask for active subscription, coverage product, covered level, and maintenance program template evidence |
| Target field is not documented | Show the target table and field name and restrict mapping to documented MNT_PROGRAMS_INT or MNT_WORK_REQUIREMENTS_INT fields |
| Target accepted value is unresolved | Return needs_decision with the exact field and required accepted-value evidence |
| Source candidate is ambiguous | Return alternatives with object, attribute, type, evidence, and decision request |
| Source alias lacks access or publication evidence | Return prerequisite_pending and identify the exposure, access, or publication gap |
| Handoff is incomplete | Return missing source-to-target pair, type check, publication prerequisite, unresolved decision, or caller continuation |
| Live update, publish, process submission, import, or transfer validation is requested | Refuse the operation and identify the missing supported workflow contract |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Missing phase, business requirement, current Service Mapping evidence, target field context, or handoff fields | Ask for the exact missing current input |
| Catalog mismatch | Requested task, folder, or task code differs from the selected nested skill | Correct routing without changing generated metadata |
| Documentation gap | Public Oracle docs describe context or target data model but not Service Mapping export, update, publish, or live lookup contract | Record the missing contract and keep the task incomplete |
| Needs decision | More than one source candidate or target interpretation remains viable | Ask the implementer to select a named candidate or provide the exact source |
| Prerequisite pending | Source is selected but exposure, service access, or publication is not verified | Complete the prerequisite through the supported Service Mapping workflow |
| Auth/authz | A documented lookup cannot be read because privilege is missing | Report environment, operation, and required privilege without retrying |
| Fusion API | A documented read-only lookup fails | Preserve sanitized status, request path, and next owner; no substitute route |
| Approval blocker | Approval is requested for update or publish but exact approved preview is absent or stale | Reapprove exact proposal after validation and design gates pass |
| Unsupported operation | User asks this task to perform live update, publish, import, ESS submission, polling, direct SQL, or direct table update | Return unsupported operation and missing workflow contract |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Every result | Task code, task name, rule phase, evaluated checks, not-applicable checks, unresolved live contracts, and safe next action |
| Source recommendation | Source object, source attribute, alias, data type, source evidence, alternatives, publication state, and target field |
| Handoff | Source-to-target pairs, type and length checks, coverage context, publication prerequisites, unresolved decisions, and companion Algorithms next action |
| Publication readiness | Target environment, source aliases, publication evidence, and explicitly unverified runtime transfer state |
| Registry readiness | Readiness covers authored task-node structure only; live lookup endpoints, update route, publication route, and process contracts remain independent gates |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Target table documentation is available | Do not treat target table fields as Subscription source aliases or as permission for direct table update |
| Local source recommendation exists | Do not claim Service Mapping is published or deployed without environment-matched evidence |
| dataloader_import_mode is REST but businessObject is empty | Do not infer a Data Loader REST business object or sample-generation route for this task |
| Subscription is active | Do not claim Maintenance transfer success without correlated scheduled-process and target result evidence |
| Lookup endpoint is TBD | Do not use browser navigation, ad hoc REST, SQL, or another tool to replace the missing resolver contract |
| User asks for live update or publish | Do not mutate Service Mapping configuration from this authoring task |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MNTSM.CHECK_EXECUTION_CONTRACT | decision | 50 | execution_gate | ready->MNTSM.EVALUATE_HANDOFF;blocked->MNTSM.REPORT_ISSUES;unsupported->MNTSM.RETURN_UNSUPPORTED | MNTSM.ENFORCE_DESIGN | stop | Gate exact supported scope for source analysis, handoff, publication checks, and unsupported-operation requests. |
| MNTSM.RETURN_RULE_RESULTS | terminal | 70 | terminal | none | MNTSM.EVALUATE_HANDOFF | stop | Return source-resolution and handoff findings for the current checkpoint; this is not proof of published Service Mapping or Maintenance Cloud transfer success. |
| MNTSM.REPORT_ISSUES | step | 80 | error_handler | reported->RETURN_ISSUES | none | stop | Classify blockers, missing contracts, failed evidence, unresolved source decisions, or unsupported requests and return the safe next action. |
| RETURN_ISSUES | terminal | 90 | terminal | none | none | stop | Return blocking findings without retrying lookups, publishing Service Mapping, mutating algorithms, or running scheduled processes. |
| MNTSM.RETURN_UNSUPPORTED | terminal | 100 | terminal | none | none | stop | Refuse unsupported live operations and identify the missing contract or owning workflow. |
