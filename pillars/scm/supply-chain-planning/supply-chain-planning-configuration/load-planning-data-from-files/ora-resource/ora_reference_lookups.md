# Planning FBDI Template Resolution

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| resolve_planning_fbdi_template | Once during local preparation for the retained/requested members, never again during Task Hook or after approval | SKILL.md direct file route; selected source-system type; target documentation release | Current release of https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/faspf/import-templates-used-to-create-csv-files-for-oracle-supply-chain-planning.html and its linked FBDI guide | Published workbook and CTL URLs; source-system eligibility; requested tab metadata | Verify the named workbook pairing from SKILL.md rather than searching unrelated entities; obtain each needed workbook/CTL once per run and select the tab by CTL file prefix | Same-run compact contract, public URLs, retrieval time, release, source-system context and SHA-256 digests | Stop on changed pairing, unavailable linked file, unsupported source-system type, missing tab or schema drift; never use a stale cached layout |

## Direct Public Sources

| Family | Verified public source | Published workbook |
|---|---|---|
| Sourcing rules and assignments | https://docs.oracle.com/en/cloud/saas/supply-chain-and-manufacturing/26c/oefsc/supplychainplanningsourcingrules-3222.html | ScpSourcingImportTemplate.xlsm |
| ATP rules and assignments | Current-release FBDI guide linked from the Planning template catalog above | ScpATPRulesImportTemplate.xlsm |

26C links were checked during the 2026-10-01 refactor. At runtime use the
current applicable published release, not a frozen 26C schema. Workbooks/CTLs
are fresh run inputs; only the documented route is reusable across runs.
The catalog is used for eligibility/pairing verification, not broad discovery.

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Rules and assignments share a workbook | Fetch/parse it once with both requested CTLs; do not inspect unrelated tabs |
| User provides CSV or ZIP | Resolve contracts for retained members only; preserve their bytes during validation |
| Task Hook evaluates prepared evidence | Consume its recorded lookup result and hashes; do not download or parse again |
| Source contract changes during preparation | Re-extract affected contracts and prepare a new artifact before approval |
