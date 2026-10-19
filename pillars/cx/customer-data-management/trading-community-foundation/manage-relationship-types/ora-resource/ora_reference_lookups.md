# Reference Lookups

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_relationship_type_by_exact_name | A validated Relationship Type is supplied | Relationship Type | TBD — the authorized Oracle guide documents the Manage Relationship Types page search, not a read-only Fusion API request | Relationship Type | Search the Manage Relationship Types page by the supplied exact relationship type name and select the matching result; the documented example is Employment | Selected relationship type for Edit Relationship Type page | TBD — the source does not document no-match or multiple-match behavior; stop and request a documented resolution before continuing |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A relationship type is being edited | The authorized guide instructs the user to enter the Relationship Type in the Search region, click Search, select the result, and open Edit Relationship Type. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRT.FIND-RELATIONSHIP-TYPE | decision | 20 | reference_lookup | selected->MRT.DONE-DOCUMENTED-FLOW;lookup_contract_tbd->MRT.HANDLE-LOOKUP-CONTRACT-GAP | MRT.VALIDATE-DOCUMENTED-INPUT | stop | A validated relationship type is supplied |
