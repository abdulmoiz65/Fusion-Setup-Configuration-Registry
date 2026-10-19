---
name: promo-code-feature
description: Return Oracle Fusion promotion-code solution bundles and their features. Use when the user asks for promoCode_feature, promotion-code features, or a promotion-code-to-feature CSV export.
---

# Promo Code Feature

Return the columns `PRODUCT`, `SOLUTION_BUNDLE_NAME`,
`SOLUTION_BUNDLE_CODE`, `FEATURE_NAME`, and `FEATURE_CODE`, in that order.

Use read-only BOSS OAuth with `boss_scope` in `core/auth/fusionEnv.properties`
and the `.fusionaim_boss_token.json` cache. Never use the default `scope` token
or expose credentials.

| Purpose | Method and endpoint |
|---|---|
| Enumerate promotion codes | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/searchPromotionCodes` |
| Read a promotion code's feature associations | `GET /api/boss/extraction/queries/ora/commonSetup/features/v1/promotionCodeAssociatedFeatures?promotionCodeShortName={promotionCodeShortName}` |

Pass `$limit` and `$offset` on collections. Return only 25 rows by default.
Generate a CSV only when the user explicitly requests the full list.
Pass `--verbose` for progress updates after promotion-code retrieval, each
feature-association request, and CSV creation.

```bash
python3 core/fusion-api/fsm-rest-client/scripts/promo-code-feature.py \
  --properties core/auth/fusionEnv.properties --preview-limit 25

python3 core/fusion-api/fsm-rest-client/scripts/promo-code-feature.py \
  --properties core/auth/fusionEnv.properties --all --project-id <project_id>
```

Use `--output <path>` for an explicit local CSV path. Include the CSV path, row
count, API-call count, and errors in the full-export response.
