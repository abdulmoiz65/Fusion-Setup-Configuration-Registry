# Setup Tasks by Feature BOSS Endpoint

Use this reference to retrieve setup tasks for a selected Oracle Fusion
offering and functional area.

## Endpoint

```text
GET /api/boss/extraction/queries/ora/commonSetup/tasks/v1/$en/tasksByFeature?featureShortName=<functional-area-code>&offeringShortName=<offering-code>
```

## Parameters

| Parameter | Required | Source | Description |
|---|---:|---|---|
| `featureShortName` | Yes | `functional_area_scope` | Selected functional-area short code. |
| `offeringShortName` | Yes | `offering_scope` | Selected offering short code. |

Use short codes resolved by `router.project-objective-classifier`, not display
names. The offering and functional area must be an unambiguous parent-child
pair before invocation.

## Invocation

Run the BOSS client from the repository root. Quote the endpoint because its
locale path segment contains `$en`.

```bash
python3 core/fusion-api/rest-api-client/scripts/boss-rest_client.py \
  '/api/boss/extraction/queries/ora/commonSetup/tasks/v1/$en/tasksByFeature' \
  --query featureShortName=ORA_DOO_ORDER_FULLFILLMENT \
  --query offeringShortName=DOO_ORCHESTRATION
```

Add pagination only when required by the response contract, for example
`--query '$limit=50'`. Use the BOSS client's `--output` option to retain
diagnostics in the active project workspace or an approved temporary location.

## Authentication and Failure Handling

- The BOSS client obtains OAuth credentials with `boss_scope` and uses the
  `.fusionaim_boss_token.json` cache by default.
- Do not use the default Fusion `scope` token for this `/api/boss` endpoint.
- The client refreshes authentication once after a `401` or `403`; do not
  retry other failures automatically.
- Treat missing scope codes, ambiguous offering-functional-area matches, and
  empty task results as input or catalog validation outcomes. Record the
  scope codes, request identifier when available, and response status.

## Consumer: Task Dependency Resolver

`shared.implementation-planning.task-dependency-resolver` invokes this
endpoint once for every valid offering/functional-area pair in the
`offering_scope` and `functional_area_scope` outputs of
`router.project-objective-classifier`. It consolidates returned setup tasks,
removes duplicate task identities, and uses the result to construct
`setup_task_sequence`. Order the tasks by the API response's
`displaySequence` attribute, which determines their execution sequence.
Record dependency relationships separately when they are available; do not
infer them from the raw response order.
