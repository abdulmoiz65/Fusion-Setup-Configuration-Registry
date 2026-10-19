# Error Handling

Source: developer-provided Fusion UI capture and the current repository EFF
deployment workflow. The UI exposes Deployment Status, Deployment Error
Message, and Deployment Date for the selected flexfield result.

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required deployment target, environment, or reason is missing | Return the missing detail and stop before requesting deployment. |
| The selected configuration change or import is incomplete | Stop; do not deploy the selected flexfield. |
| Explicit approval is missing immediately before deployment | Stop and request approval for the exact environment and selected flexfield. |
| Deployment Status is unsuccessful or Deployment Error Message is populated | Return the safe status and error details and stop before retry. |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required target, environment, reason, or approval is absent | Provide the missing detail or approval and restart validation. |
| PRECONDITION_FAILED | The selected change or import is not complete | Complete or verify the prerequisite before requesting deployment. |
| DEPLOYMENT_FAILED | The UI or delegated workflow reports a non-successful deployment result | Review the safe diagnostic and obtain explicit approval before any retry. |

## Disclosure Rules

| Gate | What Must Be Shown |
|---|---|
| Deployment outcome is reviewed | Selected Flexfield Code, target environment, Deployment Status, Deployment Date when available, and sanitized Deployment Error Message when available. |
| Approval is requested | Exact target environment, selected Flexfield Code, intended deployment effect, and the delegated deployment operation. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Approval is absent | Do not submit or retry deployment. |
| Deployment failed or status is uncertain | Do not retry deployment automatically. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IEFF.APPROVAL_GATE | step | 30 | execution_gate | approved->IEFF.READY_TO_DELEGATE;missing->RETURN_ISSUES | IEFF.CONFIRM_DEPLOYMENT_PREREQUISITES | stop | The selected EFF is ready for deployment and the delegated deployment request is about to be made |
| RETURN_ISSUES | terminal | 40 | terminal | none | none | stop | Input, prerequisite, approval, or deployment-outcome checks identify an issue |
| IEFF.READY_TO_DELEGATE | terminal | 50 | terminal | none | IEFF.APPROVAL_GATE | stop | Explicit approval is current for the exact selected flexfield and environment |
