# Input Validation

Source: developer-provided Fusion UI capture of Deploy Item Extensible
Flexfields dated 2026-09-17 and the current repository EFF deployment
workflow. The UI supports searching by Name, Flexfield Code, and Module, then
selecting a result for deployment.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Deployment target | Flexfield Code and the selected UI result | Stop before deployment preflight | Provide the exact code selected from the Deploy Item Extensible Flexfields results | A deployment is requested | |
| Target environment | Confirmed nonproduction or approved Fusion environment | Stop before deployment preflight | Provide the exact target environment | A deployment is requested | |
| Deployment reason | Successful approved import or confirmed direct UI configuration change requiring redeployment | Stop before deployment preflight | Provide the completed change or import evidence | A deployment is requested | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Flexfield Code selection | Reject a request without an exact selected Flexfield Code; EGO_ITEM_EFF is an observed Item Extended Attributes result, not a default | A deployment is requested | |
| Target environment | Reject a request without a confirmed target Fusion environment | A deployment is requested | |
| Deployment reason | Reject a request unless it identifies a completed import or a direct UI change that requires redeployment | A deployment is requested | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IEFF.VALIDATE_REQUEST | step | 10 | validate_input | valid->IEFF.CONFIRM_DEPLOYMENT_PREREQUISITES;invalid->RETURN_ISSUES | none | stop | A Deploy Item Extensible Flexfields request is supplied |
