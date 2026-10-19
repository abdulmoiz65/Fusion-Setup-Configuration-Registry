# Manage Account Combinations Reference Lookups

This file owns the read-only Fusion lookup used by this task. A lookup failure is never evidence that a business value is absent.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_chart_of_accounts_from_candidate | A candidate needs COA metadata | Position 1 from a CSV or ZIP, or the COA identifier embedded in natural-language input | /fscmRestApi/resources/11.13.18.05/chartOfAccountsLOV?q=StructureInstanceCode='{COA identifier}', then Name='{COA identifier}' only for a zero exact code match from natural-language input | Name, StructureInstanceId, StructureInstanceNumber, StructureInstanceCode, EnabledFlag | For CSV or ZIP, require one enabled exact StructureInstanceCode match from position 1. For natural language, try exact StructureInstanceCode first; only when that returns zero exact matches, try exact Name. Require one enabled match; never fall back after ambiguity, auth, transport, paging, parsing, or client failure. | Chart of Accounts Code from StructureInstanceCode; StructureInstanceNumber; StructureInstanceId; enabled evidence | Zero after the applicable lookup sequence is not found; many is ambiguous; 401 or 403 is auth or authz; every other HTTP, paging, parsing, or client failure stops without treating the COA as missing |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| CSV or ZIP candidate | Read position 1 as the COA code and URL-encode the exact StructureInstanceCode q predicate. Do not fall back to Name for a malformed or missing CSV code. |
| Natural-language candidate | Extract the embedded COA identifier without asking the user whether it is a code or name. Query StructureInstanceCode first; use the exact Name predicate only after zero code matches. |
| Multiple pages are returned | Continue until hasMore is false before evaluating cardinality. |
| One enabled exact match | Map only StructureInstanceCode, StructureInstanceNumber, and StructureInstanceId needed by the documented task contract. |
| Authentication or transport failure | Preserve the failure class and sanitized request context; do not retry an import. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MAC-020-RESOLVE-COA | decision | 20 | reference_lookup | resolved->MAC-030-RESOLVE-DEPENDENCIES;unresolved->MAC-070-HANDLE-ERROR | MAC-010-VALIDATE-INPUT | stop | Candidate requires COA metadata for import handoff |
