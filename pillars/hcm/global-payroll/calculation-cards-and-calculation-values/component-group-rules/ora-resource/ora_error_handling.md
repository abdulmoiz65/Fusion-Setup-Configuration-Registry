# Error Handling

## Error Situations

| Situation | What Should Happen |
| --- | --- |
| A Component Group Rules request is received | End the current task as REDIRECTED and return the exact Payroll Components handoff to the invoking Implementation Router; do not process the request in this task. |
| The invoking workflow cannot consume the redirect handoff | Show the exact handoff and stop. Do not load or execute the Payroll Components SKILL.md from this task and do not fall back to the legacy route. |
| The requested legacy function may not be supported by Payroll Components | Preserve the normalized business objective and let a fresh Payroll Components run classify the function as supported, deferred, or unsupported. Do not claim feature parity. |

## Error Classifications

| Result Category | When Used | Next Action |
| --- | --- | --- |
| Redirected | Every request for this setup task | End the Component Group Rules run and have the outer Implementation Router start a fresh Payroll Components task run. |

## Disclosure Rules

| Gate | What Must Be Shown |
| --- | --- |
| Redirect identity | result=REDIRECTED; requested_task_code=PAY_MANAGE_DEDUCTION_GROUP_RULES; requested_task_name=Component Group Rules; target_task_code=SUPPLEMENTAL_PAYROLL_COMPONENTS; target_task_name=Payroll Components; target_skill_id=hcm.global-payroll.calculation-cards-and-calculation-values.payroll-components; router_skill_id=router.implementation-router; reuse_legacy_execution_state=false |
| Handoff state | Preserve the normalized implementation objective only. Do not carry legacy artifacts, approvals, resolved identifiers, CSV assumptions, task-node state, or retry state into the destination run. |
| Scope boundary | The target is a replacement route, not a one-to-one parity promise. The Payroll Components skill independently determines supported, deferred, and unsupported functionality. |
| Side effects | This task performed no Fusion API call, browser action, export, import, Data Loader operation, or other external mutation. |

## Refusal Rules

| Situation | What Must Not Happen |
| --- | --- |
| A request is redirected | Do not execute the legacy CSV export/import workflow, Data Loader, Fusion API, browser, or another external integration from this task. |
| A request is redirected | Do not directly load or execute the Payroll Components SKILL.md and do not encode a transition to a Payroll Components task node. |
| A request is redirected | Do not reuse legacy artifacts, approvals, identifiers, assumptions, task-node state, retry state, or an uncertain prior outcome. |
| A request is redirected | Do not claim that Payroll Components provides one-to-one feature parity with Component Group Rules. |
| A request is redirected | Do not redirect back to Component Group Rules after the fresh Payroll Components run begins. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CGR.REDIRECTED | terminal | 2 | terminal | none | CGR.REDIRECT | stop | Always |
