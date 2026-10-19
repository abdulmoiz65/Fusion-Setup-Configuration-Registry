# Fusion BOSS REST API Instructions

Use this instruction file for Oracle Fusion BOSS REST endpoints under:

```text
/api/boss
```

Do not use the standard Fusion REST script for these endpoints. BOSS endpoints
require the `boss_scope` OAuth scope.

## Script

Run from the repository root:

```bash
python3 core/fusion-api/rest-api-client/scripts/boss-rest_client.py \
  /api/boss/extraction/queries/ora/commonSetup/features/v1/availableSetupFunctionalAreasByOffering \
  --query parentShortName=DOO_ORCHESTRATION
```

## OAuth Scope and Cache

The script uses the `boss_scope` property from:

```text
core/auth/fusionEnv.properties
```

Default BOSS token cache:

```text
.fusionaim_boss_token.json
```

Keep BOSS tokens in this separate cache unless the caller explicitly supplies
`--token-cache`.

## Endpoint Rules

- Endpoints must start with `/api/boss`.
- Relative endpoints are joined to `restBaseUrl`.
- Query parameters must be passed with repeated `--query key=value` options.
- Quote arguments that contain shell-sensitive `$` characters, such as `$en` or
  `$limit`.
- The client retries once after a 401 or 403 by forcing OAuth login with
  `boss_scope`.

## Examples

Retrieve available setup functional areas for an offering short code:

```bash
python3 core/fusion-api/rest-api-client/scripts/boss-rest_client.py \
  /api/boss/extraction/queries/ora/commonSetup/features/v1/availableSetupFunctionalAreasByOffering \
  --query parentShortName=DOO_ORCHESTRATION
```

Retrieve setup tasks for a functional area and offering:

```bash
python3 core/fusion-api/rest-api-client/scripts/boss-rest_client.py \
  '/api/boss/extraction/queries/ora/commonSetup/tasks/v1/$en/tasksByFeature' \
  --query featureShortName=ORA_DOO_ORDER_FULLFILLMENT \
  --query offeringShortName=DOO_ORCHESTRATION \
  --query '$limit=50'
```

Write the full JSON response to a file:

```bash
python3 core/fusion-api/rest-api-client/scripts/boss-rest_client.py \
  '/api/boss/extraction/queries/ora/commonSetup/tasks/v1/$en/tasksByFeature' \
  --query featureShortName=ORA_DOO_ORDER_FULLFILLMENT \
  --query offeringShortName=DOO_ORCHESTRATION \
  --query '$limit=50' \
  --output /private/tmp/tasksByFeature_DOO_ORCHESTRATION.json
```
