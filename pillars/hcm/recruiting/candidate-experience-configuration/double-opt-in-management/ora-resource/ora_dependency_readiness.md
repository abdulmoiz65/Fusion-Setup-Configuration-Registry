# Dependency Readiness

## Required Dependency Order

| Sequence | Dependency | What Must Happen |
|---|---|---|
| 1 | FSM task access | Confirm the user can open Double Opt In Management. |
| 2 | HCM Countries LOV | Select valid country values when Set Specific Regions is used. |

## Dependency Rules

| Dependency ID | Dependency | Mandatory | Applies When | Status | Value Source | Resolver | Why | User Guidance | Values to Fill |
|---|---|---|---|---|---|---|---|---|---|
| doi_task_access | Recruiting and Candidate Experience offering, Candidate Experience functional area, and Double Opt In Management task access | Yes | Before configuration | Verify | Oracle Help Center procedure and FSM access | | The source requires the user to open the FSM task | If access is unavailable, stop and route to the security owner | Access to the FSM task |
| doi_country_selection | HCM Countries LOV selection | Yes | Mode is LIST_OF_REGIONS | Verify | core.fusion-api.rest-api-client -> /hcmRestApi/resources/11.13.18.05/hcmCountriesLov | resolve_country_by_name | Country selection supplies the stored TerritoryCode | Select a valid country result in the UI; do not use it as a supported customer integration contract | TerritoryCode |

## Dependency Classification

| Result Category | When Used | Can Run Lookup/Create? |
|---|---|---|
| Satisfied | Task access is available and applicable country values are selected | No |
| Blocked | FSM task access is missing or a required regional country is not selected | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| DOI.CHECK_READINESS | decision | 10 | resolve_dependency | ready->DOI.RESOLVE_COUNTRY;blocked->DOI.HANDLE_ACCESS_ISSUE | none | stop | Before configuration |
