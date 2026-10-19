# Input Validation

Source: the generated Import Price Lists setup-task skill and its declared
FBDI Data Loader workflow.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Task identity | Task code CUSTOM_IMPORT_PRICE_LISTS and task name Import Price Lists | Block task validation | Select the generated Import Price Lists nested task skill and rebuild the task context | Always | |
| FBDI import artifact | One exact local ZIP selected for this import request | Block Data Loader preview | Supply the ZIP to core.data-loader for source review and immutable-artifact validation | When an upload or import is requested | |
| Target environment | One explicit Fusion environment selected for the request | Block Data Loader preview | Select the intended target environment before building the preview | When an upload or import is requested | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| Data Loader source review or Task Hook validation has not passed | Blocked | Complete the missing core.data-loader validation stage before approval or upload | |
| The exact ZIP and target environment have passed the applicable Data Loader validation stages | Ready | Build the immutable Data Loader preview | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Import mode | Reject a route other than FBDI for this task | Always | |
| Generic setup-task CSV route | Reject routing based only on CSV export or import support because the catalog flag is N | Always | |
| Artifact identity | Reject approval or upload when the ZIP differs from the artifact validated in the preview | Before approval or upload | |
| Task context identity | Reject a task context whose code, name, or skill path does not identify this nested task | Before Task Hook validation | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PLB_VALIDATE_INPUT | step | 1 | validate_input | valid->PLB_RETURN_READY;invalid->PLB_RETURN_ISSUES | none | stop | Always |
