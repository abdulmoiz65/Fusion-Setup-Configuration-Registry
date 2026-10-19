# Picking Rules Reference Lookups

This resource applies to REST-friendly input only. FSM `ORA_INV_RULE.csv`
priority fields are passed through unchanged; do not use this lookup to
transform an FSM package.

## Source Evidence

| Source | Used For |
|---|---|
| Redwood Picking Rules priority LOV chains | Lookup type, selected-value exclusion, and requested fields |
| Developer-provided read-only fndStaticLookups response | Environment-relative CRM REST route and Meaning-to-LookupCode response mapping |

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_picking_rule_priority | A REST Priority1Sort, Priority2Sort, Priority3Sort, or Priority4Sort display Meaning is supplied, or a display Meaning and LookupCode require reconciliation | Supplied priority display Meaning, priority ordinal, and other selected priority LookupCodes | /crmRestApi/rest/rv:f3f69466-6462-4caa-9b31-00bbec23ed02/en/11.13.18.05:9/fndStaticLookups?fields=LookupType,LookupCode,Meaning&onlyData=true&q=LookupType='INV_PICK_RULE_ALLOC_PRIORITY' | LookupType, LookupCode, Meaning | Read-only GET. Trim and compare Meaning case-insensitively for an exact match. Require exactly one returned row. Exclude LookupCodes already selected in the other priority fields. If both a display Meaning and LookupCode are supplied, require the code to equal the resolved LookupCode. Never fuzzy-match or select the first row. | Priority1Sort, Priority2Sort, Priority3Sort, Priority4Sort: LookupCode | Stop Data Loader handoff for zero or multiple exact matches, a read failure, a code duplicated in priority context, or conflicting supplied display value and code. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A REST priority display Meaning resolves exactly once | Preserve Meaning as sanitized lookup evidence and fill only the returned LookupCode in the matching priority field |
| A REST priority field is supplied as canonical LookupCode only | Preserve the supplied canonical code; no display-value lookup is sent |
| An FSM priority field is supplied | Preserve the supplied value without issuing a lookup or transforming the FSM package |
| A priority display Meaning resolves to zero or multiple rows | Stop before Data Loader handoff and report the affected field and supplied display value |
| The lookup request fails | Classify the failure through ora_error_handling.md; do not infer a priority value or retry a mutation |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PICKRULES.RESOLVE_PRIORITY | decision | 30 | reference_lookup | resolved->PICKRULES.REST_DATALOADER_HANDOFF;not_applicable->PICKRULES.REST_DATALOADER_HANDOFF;failed->PICKRULES.RETURN_ISSUES | PICKRULES.CHECK_DEPENDENCIES | stop | REST requests only, after dependency readiness and before Data Loader handoff. Display Meanings resolve; supplied LookupCodes are not applicable. |
