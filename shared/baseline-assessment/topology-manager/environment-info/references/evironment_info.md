# Environment Information API Reference

Source: supplied Topology Manager OpenAPI v3.0.1 contract.

| Operation | Method and path | Inputs | Contract behavior |
| --- | --- | --- | --- |
| Get environment information | `GET /api/fusion-common/topologymanager/v1/environmentInfo` | Target environment | Read-only operation using the Fusion Common OAuth scope. |

The response requires `releaseVersion`, `environmentName`, `environmentType`, `environmentSize`, and `breakGlassEnabled`. It may include `releaseName`, `lastShippedReleaseVersion`, `lastShippedReleaseName`, `customerName`, `podAttributes`, and `links`.

## Environment Version Details

Return this machine-readable object whenever environment version details are
requested, and include it in an unqualified environment-information response:

```json
{
  "environment_version_details": {
    "releaseVersion": "<current release version>",
    "releaseName": "<current release name when returned>",
    "lastShippedReleaseVersion": "<last shipped release version when returned>",
    "lastShippedReleaseName": "<last shipped release name when returned>"
  }
}
```

Do not synthesize a missing optional version field. The `releaseVersion` value
is required by the API contract.

## Upgrade Status

After `GET /api/fusion-common/topologymanager/v1/environmentInfo`, make this additional read-only BOSS call against the same target environment through `core.fusion-api.rest-api-client`:

```text
GET /api/boss/extraction/queries/ora/commonSetup/topologyManager/{apiVersion}/previousReleases
```

Use `fusion_common_scope` through `core.auth.fusion-oauth-authentication` for
the Environment Information API and `boss_scope` for this BOSS request. The
REST client keeps these scopes in separate local token caches. A non-empty BOSS
`items` collection means `Upgraded: true`; an empty or absent collection means
`Upgraded: false`.

## Field Selection

Normalize environment field labels case-insensitively across camelCase,
PascalCase, snake_case, kebab-case, spaces, and punctuation. Correct a synonym
or minor typo only when it has one supported environment-field meaning.

- `environment name` maps to `environmentName`.
- `environment type` maps to `environmentType`.
- `environment size` maps to `environmentSize`.
- `release` or `version` maps to `releaseVersion`.
- `environment version details`, `release details`, or `release history` maps
  to `environment_version_details`.
- `break-glass` maps to `breakGlassEnabled`.
- `upgraded` or `upgrade status` maps to `Upgraded`.

For an unqualified request, return `environmentName`, `environmentType`, `environmentSize`, `releaseVersion`, `releaseName`, `lastShippedReleaseVersion`, `lastShippedReleaseName`, `breakGlassEnabled`, `customerName`, and `Upgraded`; omit `podAttributes` and `links`. When the user names fields, return only supported requested fields. Redact sensitive infrastructure values from summaries and diagnostics.
