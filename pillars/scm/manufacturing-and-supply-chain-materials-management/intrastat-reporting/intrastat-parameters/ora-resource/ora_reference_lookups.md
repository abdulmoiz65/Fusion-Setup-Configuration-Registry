# Intrastat Parameters Reference Lookups


## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_intrastat_exclude_arrivals | ExcludesArrivalToName or ExcludeArrivalsTo is nonblank | ExcludesArrivalToName, ExcludeArrivalsTo | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_JMF_EXCL_DISPATCH_ARRIVAL'&fields=LookupCode,Meaning&onlyData=true | LookupCode, Meaning | Trim outer whitespace and require exactly one case-insensitive exact match: ExcludesArrivalToName to Meaning and ExcludeArrivalsTo to LookupCode. When both are supplied, both must identify the same single row. | ExcludeArrivalsTo: returned LookupCode, preserving its exact system spelling | Block Data Loader handoff on zero matches, multiple matches, or conflicting supplied code and meaning. Never guess, fuzzy-match, or select the first candidate. |
| resolve_intrastat_exclude_dispatches | ExcludesDispatchFromName or ExcludeDispatchesFrom is nonblank | ExcludesDispatchFromName, ExcludeDispatchesFrom | /fscmRestApi/resources/11.13.18.05/standardLookupsLOV?q=LookupType='ORA_JMF_EXCL_DISPATCH_ARRIVAL'&fields=LookupCode,Meaning&onlyData=true | LookupCode, Meaning | Trim outer whitespace and require exactly one case-insensitive exact match: ExcludesDispatchFromName to Meaning and ExcludeDispatchesFrom to LookupCode. When both are supplied, both must identify the same single row. | ExcludeDispatchesFrom: returned LookupCode, preserving its exact system spelling | Block Data Loader handoff on zero matches, multiple matches, or conflicting supplied code and meaning. Never guess, fuzzy-match, or select the first candidate. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| One or both exclusion field pairs are supplied | Evaluate each applicable resolver independently for each source row. No LRU, country, calendar, or other parent context is required. |
| Both values in a field pair are blank or absent | Skip that resolver and preserve blanks; do not introduce a default. |
| A declared lookup is needed | Use a read-only GET through the active workflow's core.fusion-api.rest-api-client after its environment, identity, privilege, and authentication checks. Do not initiate lookup calls merely by reading this resource. |
| Results span multiple pages | Consume all relevant result pages before declaring an exact match unique. An incomplete result set blocks resolution. |
| A code or meaning is supplied | Match against its respective returned attribute. Apply exact comparison after trimming and case normalization; the UI's contains-search behavior is not an automatic selection rule. |
| Lookup fails or a pair cannot be resolved | Stop before Data Loader handoff and report the source row, affected field, and failure without credentials. Preserve successful results for diagnosis; do not release a partially resolved row or overwrite conflicting inputs. |
| All applicable resolvers succeed | Return resolved exclusion codes to the invoking Data Loader workflow. Lookup success does not authorize or execute a Fusion mutation. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| INTRASTAT_PARAMETERS.RESOLVE_EXCLUSIONS | decision | 10 | reference_lookup | resolved->INTRASTAT_PARAMETERS.RETURN_SUCCESS;not_required->INTRASTAT_PARAMETERS.RETURN_SUCCESS;blocked->INTRASTAT_PARAMETERS.RETURN_ISSUES;failure->INTRASTAT_PARAMETERS.RETURN_ISSUES | INTRASTAT_PARAMETERS.NORMALIZE_UI_LABELS | stop | Evaluate both declared exclusion resolvers for each source row; skip each blank pair and return not_required when neither pair is supplied. |
