# Manage Tax Fields reference lookups

Evidence: SRC-CS-EO, SRC-CS-FSM-AM, SRC-CS-SETUP-FSM-AM, DOC-REST-BU, DOC-REST-TERRITORY and SRC-CS-LOOKUP-PVO in references/evidence.md. BU and territory REST contracts are documented and were exercised in the dated campaign summarized in references/evidence.md; availability and access must be checked for each target run. Behavior validation uses the source-proven FSM entity validator; a separate public REST equivalent is not required (BUILDER-FSM-VALIDATION). This is import-time validation, not a claim that target values were already read.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_tax_business_unit | BU reference validation | BuName and authenticated target environment | /fscmRestApi/resources/11.13.18.05/finBusinessUnitsLOV | BusinessUnitId,BusinessUnitName,ActiveFlag | Use q with safely quoted and URL-encoded exact BusinessUnitName; traverse every result page, then require one case-sensitive name match with ActiveFlag=true; do not send the returned ID across environments | Validated target BU name and ID for preflight; FSM resolves OrgId internally | Zero matches or inactive BU: input issue; multiple exact matches: ambiguity issue; missing attributes or unreadable response: contract issue; 401/403: auth/authz failure |
| resolve_tax_territory | Country-specific rule; skip only explicit OTHER | TerritoryCode | /fscmRestApi/resources/11.13.18.05/territoriesLOV | TerritoryCode | Use documented PrimaryKey finder with safely encoded TerritoryCode; require exactly one case-sensitive match after pagination | Validated territory code | Zero matches: invalid territory; multiple matches: ambiguity issue; missing attributes: contract issue; 401/403: auth/authz failure |
| resolve_tax_behaviors | Local code check before packaging; target validation during separately approved FSM import | Each of the six explicit Enable*Code values | FSM import validation through VatFieldEO.ExmLookupPVO; internal evidence only, not a separately callable endpoint | LookupCode with LookupType=EXM_FIELD_BEHAVIOUR and EnabledFlag=Y | Local allowlist DISABLED, ENABLED, REQUIRED; entity ListValidationBean tests membership in the enabled lookup view during import | Preserve the exact supplied code; no ID or meaning mapping | No enabled membership: FND_CMN_INVALID_ATTRB_API_SRV2; multiple rows are membership matches, not a first-row selection; capture import errors and reconcile partial outcomes |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Incomplete resolver | Retain TBD and block readiness; do not fabricate an endpoint or label supplied input as locally authoritative |
| Documented REST lookup | Use core.fusion-api.rest-api-client only when selected by the active workflow, with REST-Framework-Version: 9 and onlyData=true; a documented path alone does not authorize probing or establish target access |
| BU enterprise context | Use the same target authentication context for preflight and FSM import. The REST ID is diagnostic only; FSM independently resolves BuName plus tenant enterprise. Any mismatch or uncertain identity blocks the candidate |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| TAX.LOOKUPS | step | 2 | reference_lookup | success->TAX.DEPENDENCIES;failure->TAX.ISSUES | TAX.INPUT | stop | create or update |
