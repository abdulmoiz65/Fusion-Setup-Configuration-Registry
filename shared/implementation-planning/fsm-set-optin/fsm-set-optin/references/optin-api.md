# FSM Set Optin API Reference

Use this reference before changing endpoints, payload fields, authentication
scopes, or safety behavior.

## Help Response

To set FSM opt-in status, collect:

- Fusion environment from `core/auth/fusionEnv.properties`.
- Target type: `offering`, `functional-area`, or `feature`.
- Target display name or short name/code.
- Action: `opt-in`/`enable`, `opt-out`/`disable`, or `set-choices`.
- `featureChoices` for explicit choices, or when a feature has multiple valid choices.
- Parent offering name/code when a functional area or feature is shared or ambiguous.

## OAuth Scopes

- Use `scope` from `fusionEnv.properties` for standard ADF REST lookups and
  `setupProcesses/action/refreshFeatureSelections`.
- Use `boss_scope` for BOSS extraction queries under `/api/boss`.
- Use `fusion_common_features_crud_scope` or `fusion_common_scope` when present
  for Fusion Common PATCH. If neither is present, derive:

```text
urn:opc:resource:fusion:{environment}:fusion-common/urn:oracle:internal:fusion-common:features:crud
```

Do not use Basic Auth for Fusion Common writes. Do not print bearer tokens,
refresh tokens, client secrets, token cache contents, cookies, passwords, or
Authorization headers.

## Read APIs

Resolve display names with the setup export-style lookup first:

```text
GET /fscmRestApi/resources/latest/features?fields=FeatureName,FeatureCode,FeatureType&q=FeatureType='<OFFERING|FUNCTIONAL_AREA|FEATURE>';FeatureName='<feature name>'
```

Then hydrate the short name through BOSS:

```text
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/searchOfferings?$filter=...
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/searchFunctionalAreas?$filter=...
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/searchFeatures?$filter=...
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/featureSelectedChoices?featureShortName=<featureShortName>
```

Parent and shared hierarchy:

```text
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/sharedHierarchy?sharedHierarchyFor=<shortName>
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/parentHierarchy?offeringName=<offeringShortName>&parentHierarchyFor=<shortName>
```

Disable safety:

```text
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/lockedChildren?featureShortName=<shortName>
GET /api/boss/extraction/queries/ora/commonSetup/features/v1/$en/sharedHierarchy?sharedHierarchyFor=<shortName>&excludeParentOffering=<offeringShortName>
```

## Write API

PATCH Fusion Common:

```text
PATCH /api/fusion-common/features/v1/features/{featureShortName}
Content-Type: application/json
```

Offering/root payload:

```json
{
  "selectedChoices": ["<choiceShortName>"],
  "caller": "REDWOOD",
  "category": "ROOT_NODE"
}
```

Functional area payload:

```json
{
  "selectedChoices": ["<choiceShortName>"],
  "caller": "REDWOOD",
  "category": null
}
```

Feature choices payload:

```json
{
  "selectedChoices": ["<choiceShortName>", "<choiceShortName>"],
  "caller": "REDWOOD"
}
```

## Refresh API

After a successful PATCH, refresh affected offering IDs:

```text
POST /fscmRestApi/resources/latest/setupProcesses/action/refreshFeatureSelections
Content-Type: application/vnd.oracle.adf.action+json
```

Body:

```json
{
  "additionalProperties": {
    "0": "<offeringId>"
  }
}
```

## Safety Rules

- Pin all three token contexts to the trusted profile's `restBaseUrl` origin.
  Validate overrides before login and every redirect/pagination destination
  before dispatch. See [destination-security.md](destination-security.md).
- Reject destination violations even with `--force`, explicit tokens, or
  `--dry-run`. Only same-origin read redirects are allowed; never replay writes
  automatically through a redirect.
- Stop when lookup is ambiguous and ask for the exact short name/code.
- Stop on locked children for disable requests unless `--force` is explicitly used.
- Stop when a shared functional area or feature is auto-enabled by another
  parent offering unless `--force` is explicitly used.
- Do not treat PATCH HTTP success alone as completion; run refresh and reread
  choices when practical.
