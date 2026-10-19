# Dependency Readiness

Source: developer-provided Fusion UI capture and the current repository EFF
deployment workflow. Deployment compiles an already-configured flexfield; it
does not transport setup data.

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | Configuration change or approved import | Complete the selected Item EFF change or its approved FSM import before deployment |
| 2 | Deployment approval | Obtain explicit approval immediately before the delegated deployment request |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| selected_eff_change | Selected EFF change or approved import | Yes | A deployment is requested | Verify | Deployment request and approved import or direct UI change evidence | | Deployment applies configured metadata and must not follow an incomplete import | Provide evidence that the selected change or import completed successfully | |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| MISSING | The selected change or completed import evidence is absent | No |
| READY | The selected change or approved import is confirmed complete | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| IEFF.CONFIRM_DEPLOYMENT_PREREQUISITES | step | 20 | resolve_dependency | ready->IEFF.APPROVAL_GATE;missing->RETURN_ISSUES | IEFF.VALIDATE_REQUEST | stop | The deployment request passed input validation |
