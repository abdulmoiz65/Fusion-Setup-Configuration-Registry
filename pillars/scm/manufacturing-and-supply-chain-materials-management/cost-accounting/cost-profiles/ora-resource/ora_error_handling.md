# Cost Profiles Error Handling

Source: [Oracle Fusion Cloud SCM 26c: Set Up a Cost Profile](https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faims/set-up-a-cost-profile.html).

## Error Situations

| Situation | What Should Happen |
|---|---|
| A required cost-profile value is absent | Stop and request the missing value |
| A method-dependent policy is incompatible | Stop and correct the incompatible selection before preview |
| A live operation fails | Preserve redacted diagnostics and stop before retry |

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| Input validation | Identity, accounting, or valuation inputs are incomplete | Supply or correct the indicated value |
| Design policy | A documented compatibility condition fails | Change the incompatible configuration choice |
| Fusion API or process failed | An authorized later operation returns an error | Review diagnostics; do not replay blindly |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CP.HANDLE_ERROR | step | 31 | error_handler | handled->CP.RETURN_ISSUES | none | stop | Any validation or design failure |
| CP.RETURN_ISSUES | terminal | 40 | terminal | none | none | stop | A blocking issue was classified |
| CP.DONE | terminal | 50 | terminal | none | CP.ENFORCE_DESIGN | stop | All documented checks passed |
