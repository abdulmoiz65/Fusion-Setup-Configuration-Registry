# Reference Lookups

Before executing any REST lookup below, apply the
[REST version and query compatibility preflight](../../../references/rest-query-compatibility.md)
and the REST request compatibility rule in Lookup Execution Rules. Existing
matching, classification precedence and workflow gates continue to apply.

## Project Numbering Method

CSV columns: PJF_PROJECT_UNIT.csv.UserDefinedProjectNumCode

| Lookup Code | Meaning |
|---|---|
| AUTOMATIC | Automatic |
| MANUAL | Manual |

Authority: System-seeded standard lookup data. The finite set has no supported add, delete, or maintenance path for this task.

Validation: resolve a supplied code, meaning, description, translation, or ordinary natural-language phrase to exactly one row and write its Lookup Code. Reject zero or multiple resolutions.

## Manual Project Numbering Method Type

CSV columns: PJF_PROJECT_UNIT.csv.ManualProjectNumType

| Lookup Code | Meaning |
|---|---|
| ALPHANUMERIC | Alphanumeric |
| NUMERIC | Numeric |

Authority: System-seeded standard lookup data reconciled with the PJF_LOOKUPS view. The finite set has no supported add, delete, or maintenance path for this task.

Validation: resolve a supplied code, meaning, description, translation, or ordinary natural-language phrase to exactly one row and write its Lookup Code. Reject zero or multiple resolutions.

## Commitment Inclusion and Status

CSV columns: PJF_REPORTING_SETUP.csv.CommitmentStatusExtr; PJF_REPORTING_SETUP.csv.CommitmentStatusReq; PJF_REPORTING_SETUP.csv.CommitmentStatusPo; PJF_REPORTING_SETUP.csv.CommitmentStatusSupinv

| Lookup Code | Meaning |
|---|---|
| A | All |
| N | Not included (unchecked) |
| R | Approved |

Authority: System-seeded standard lookup data supplies A and R; task UI and entity validation supply N as the persisted unchecked sentinel. The composite finite set has no supported add, delete, or maintenance path for this task.

Validation: resolve a supplied code, meaning, description, translation, or ordinary natural-language phrase to exactly one row and write its Lookup Code. Resolve an exclusion, no, not-included, or unchecked intent to N. Reject zero or multiple resolutions.

## Planning Amount Allocation Basis

CSV columns: PJF_REPORTING_SETUP.csv.PlanamtAllocMethod

| Lookup Code | Meaning |
|---|---|
| D | Daily proration |
| E | Period end date |
| S | Period start date |

Authority: System-seeded standard lookup data reconciled with the Fusion lookup data. This task field accepts only this finite set and has no supported add, delete, or maintenance path.

Validation: resolve a supplied code, meaning, description, translation, or ordinary natural-language phrase to exactly one row and write its Lookup Code. Reject zero or multiple resolutions.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| find_project_unit_options | Every write, validation, or import | ProjectUnitId, Organization, or name/code plus fresh Performance Reporting Setup, Project Automatic Numbering, and Project Unit Implementation exports | Exact project-unit identity; join implementation, numbering, reporting, and relationship rows for the same project unit | ProjectUnitId, identity, Exists flags, current general properties, current relationships, current reporting values, current numbering determinant | Allow creation only for a missing option/determinant row under one existing classified project unit; block zero or multiple project-unit matches |
| resolve_project_business_units | Related business units are supplied or removed | Exact BusinessUnitName and, for removal, relationship-usage evidence | Additions retain each valid name for Fusion FSM import validation; removals require deletable and unused evidence | BusinessUnitName, FusionValidationDeferred, IsDeletable, ProjectOrTemplateUse | Block blank/duplicate names and nondeletable removals; report Fusion's returned error for rejected additions |
| verify_project_unit_options_scope | Before validation completes | Offering PJF_PROJ_MNG, functional area ORA_PJF_PROJ_ORG, task PJF_MANAGE_PROJECT_UNITS, target environment | Exact catalog-code and target-environment match | Verified offering, functional area, task, target environment | Block missing or mismatched scope |
| verify_project_unit_options_package | Before import preview | Runtime template, generated package, numbering feature status, allowed reporting basis metadata | Require same-task implementation, numbering, reporting, and relationship contracts with unchanged headers; keep set assignments outside the package | Verified files, headers, row counts, checksum, feature status, allowed basis values | Block missing/changed contracts, mixed tasks, unknown feature status, or unsupported reporting values |

## Live Lookups

Currency validation uses a fresh response from the selected target environment, never a shared static currency list or another customer's export. For a newly selected currency, require enabled status and validity on the requested effective date (default: the target environment's current date). These selection checks implement the requested target-specific validation; the general-properties entity accessor itself declares currency existence validation without an additional view criterion. Do not infer a CurrencyFlag filter from an unrelated HCM caller.

Currency REST authority: [Oracle Common Features REST — Get all currencies](https://docs.oracle.com/en/cloud/saas/applications-common/26c/farca/op-http-servername-fscmrestapi-resources-11.13.18.05-currencieslov-get.html).

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_project_currency | DefaultProjCurrCode is supplied for creation or change | Currency code, name, description, translation, or ordinary business wording; target environment and effective date | GET /fscmRestApi/resources/11.13.18.05/currenciesLOV?onlyData=true&q=EnabledFlag='Y'&limit=500. Default: fetch the enabled collection without fields or a code/name predicate. Optional exact-code query and client invocation are defined in Currency REST Execution below. | Full response; require CurrencyCode, Name, Description, EnabledFlag, StartDateActive, EndDateActive, CurrencyFlag | Resolve user wording against the complete returned collection to exactly one distinct CurrencyCode; preserve the returned code. Require EnabledFlag=Y and a date inside the inclusive start/end interval, treating null boundaries as unbounded. Reuse the collection within this validation run for the same target and identity. Follow pagination before deciding absence or uniqueness. | PJF_PROJECT_UNIT.csv.DefaultProjCurrCode = returned CurrencyCode; target, effective date, and eligibility evidence | Block no eligible match, ambiguity, missing required response fields, incomplete pagination, or service/authentication failure. Do not fall back to the pasted dump, an ISO-only list, or another environment. |
| resolve_reference_set | Default Set is supplied or general properties are created | Default set name by default, or an explicitly labeled set code; current target and authenticated identity | GET /fscmRestApi/resources/11.13.18.05/setIdSetsLOV?onlyData=true&limit=500 | Full response; require SetCode and SetName, retain Description when present | Fetch the full collection once per validation run/target/identity and reuse it for every CSV row. Treat ordinary user text as an exact SetName. Use exact SetCode only when the caller explicitly labels it as a set code. Do not apply SetCodeFinder or name/description q to the shared collection. Complete pagination before deciding absence or uniqueness | PJF_PROJECT_UNIT.csv.SetCode = canonical returned SetCode; retain SetName, Description, and resolution basis as evidence | Block proven no-match or ambiguity and unavailable/incomplete required lookup under this task's existing policy; never substitute Enterprise Set. A separate reference-data-set export is not required for this lookup |

## Set REST Execution

At the declared set reference-lookup step, use core.fusion-api.rest-api-client with the selected target configuration:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/setIdSetsLOV \
  --method GET \
  --query onlyData=true \
  --query limit=500 \
  --header "REST-Framework-Version=${workflow_rest_framework_version:?resolve from the selected core workflow}"
```

This is GET-all membership validation, with no finder, q, or fields projection. SetCodeFinder selects an individual code; it is unnecessary once the complete collection is available. Resolve each row locally against the retrieved dynamic collection; do not hardcode its values or reuse another customer's list. Ordinary input is matched to SetName only. An exact SetCode is used only when the input is explicitly labeled as a set code. This prevents a value that appears in one row's SetName and another row's SetCode from silently selecting the wrong set. Refresh on a new validation run, target/identity change, or known set change. No per-row GET is needed.

If hasMore=true, repeat with the same parameters plus offset equal to returned offset + returned limit. Honor the server's returned limit even if it caps 500. Accumulate and deduplicate by SetCode until hasMore=false; conflicting records for one code, missing required fields, failed pages, or nonadvancing pagination do not establish complete membership. Follow this task's existing failure policy. Read-only verification on cptcwxaqy returned HTTP 200, 304 unique SetCodes, limit=500, hasMore=false; the set matched the earlier complete 13-page unfiltered scan.

## Currency REST Execution

At the declared currency reference-lookup step, use core.fusion-api.rest-api-client and its standard Fusion REST instructions. Run the existing client from the repository root with the selected target environment configuration:

```bash
python3 core/fusion-api/rest-api-client/scripts/fusion_rest_client.py \
  /fscmRestApi/resources/11.13.18.05/currenciesLOV \
  --method GET \
  --query onlyData=true \
  --query "q=EnabledFlag='Y'" \
  --query limit=500 \
  --header "REST-Framework-Version=${workflow_rest_framework_version:?resolve from the selected core workflow}"
```

Do not send fields or an effective-date query parameter. Resolve codes, names, descriptions, translations, and unambiguous user wording from the response; evaluate effective dates locally. Fetch once and reuse the completed result within the same validation run, target, and authenticated identity. Refresh on a new run or a known target currency change; do not maintain a static cross-customer currency list.

The client sends one page per invocation. If hasMore is true, request the next page with the same parameters plus offset equal to the returned offset plus the returned limit. Use the server's returned limit rather than assuming it honored 500. Accumulate and deduplicate rows by CurrencyCode until hasMore is false. A failed page, invalid pagination metadata, or a nonadvancing offset blocks validation; a partial collection must not establish absence or uniqueness.

An exact-code lookup is optional when one canonical code is already known and the full collection has not been fetched. Replace the q argument with "q=EnabledFlag='Y' and CurrencyCode='{CurrencyCode}'", retaining onlyData=true and limit=500 and omitting fields. Escape literals for the query language and let the client encode query parameters. Do not interpolate raw user wording into shell commands. No additional request is needed when the collection already contains the requested code.

## Lookup Execution Rules

| Situation | What happens |
|---|---|
| REST request compatibility | Before a workflow-selected request, determine framework applicability and the effective REST framework version from the selected core client or workflow. Use compatible query syntax and verify that the outgoing header agrees; never pin an independent pillar version. Apply the linked offering preflight, preserve finder separators and literal values, and stop the affected request on an unresolved version or header/query conflict. |
| `PJF_REPORTING_SETUP.csv` has exactly one complete row for the project unit | Preserve it when no reporting change is requested, or validate the requested replacement values. |
| `PJF_REPORTING_SETUP.csv` has no row for the project unit | Treat Task 2 as incomplete. Resolve explicit intent, clarify ambiguity, and apply the UI defaults from ora_defaulting_rules.md to omitted fields; show all values and their origins in the existing approval preview, build the missing row from the fresh target template, import it once through `core.data-loader`, and verify it with a new task export before downstream Project Plan Type or Project Template work. |
| A working seeded project unit supplies candidate reporting values | Show those values only as an explicit parity proposal. Do not silently default or claim compatibility until the customer approves them and the target readback succeeds. |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Current option export is missing | Stop create/update preview; do not infer target state from the supplied sample package |
| Set membership needs validation | Use resolve_reference_set and its completed current-target REST collection; no separate reference-data-set export prerequisite. If the required REST lookup is unavailable or incomplete, report that lookup failure under this task's existing policy |
| Related-business-unit list is omitted | Preserve current relationships; omission is not deletion |
| Fusion rejects a related-business-unit addition | Preserve Fusion's error against the immutable package and do not retry automatically |
| Enhanced-numbering feature status is unknown | Do not apply hidden-region defaults or decide which numbering surface owns the setup |
| Set assignment fields are supplied | Stop and route them to the separately scoped setup task and contract |
| A live write API is requested | Use the FSM task contract because no exact writable public API for the composite option surface is declared |

## Related Business Unit Validation

At resolve_project_business_units, call `scripts/validate_related_business_units.py:validate_related_business_units` with the complete requested exact-name list. For additions, it validates only distinct nonblank names and returns `FusionValidationDeferred=true`; the approved FSM import validates Project Accounting eligibility. For removals, it still requires fresh target-bound usage/deletability evidence. The helper performs no external calls or file writes.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| PUOPT.FIND_PROJECT_UNIT | step | 2 | reference_lookup | resolved->PUOPT.APPLY_DEFAULTS;failure->PUOPT.RETURN_ISSUES | PUOPT.VALIDATE_INPUT | stop | Resolve the project unit and all current same-task option rows through find_project_unit_options; also run resolve_project_currency when DefaultProjCurrCode is supplied for creation or change |
| PUOPT.RESOLVE_SET | step | 4 | reference_lookup | resolved->PUOPT.RESOLVE_BUSINESS_UNITS;not_required->PUOPT.RESOLVE_BUSINESS_UNITS;failure->PUOPT.RETURN_ISSUES | PUOPT.APPLY_DEFAULTS | stop | Resolve a supplied or required default reference set |
