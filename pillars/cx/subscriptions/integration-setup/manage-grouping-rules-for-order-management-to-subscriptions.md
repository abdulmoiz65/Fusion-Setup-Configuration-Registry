---
task_code: "CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS"
task_name: "Manage Grouping Rules for Order Management to Subscriptions"
parent_skill_id: "cx.subscriptions.integration-setup"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
dataloader_import_mode: "REST"
businessObjects:
  - "subscriptionGroupingRuleSets"
  - "subscriptionGroupingRuleSets_publishGroupingRuleSets"
  - "subscriptionGroupingRuleSets_updateOmOssAttrMap"
source_catalog: "knowledge/setup-task-catalog/effective/setupTasksAll.json"
---

# Manage Grouping Rules for Order Management to Subscriptions

## Setup Task Metadata

- Task name: `Manage Grouping Rules for Order Management to Subscriptions`
- Task code: `CUSTOM_MANAGE_GROUPING_RULES_FOR_ORDER_MANAGEMENT_TO_SUBSCRIPTIONS`
- Available: `Y`
- Export/import supported: `N`
- CSV export/import supported: `N`
- CSV export/import routing: `not supported`
- Data Loader import mode: `REST`
- Business Objects: `subscriptionGroupingRuleSets`, `subscriptionGroupingRuleSets_publishGroupingRuleSets`, `subscriptionGroupingRuleSets_updateOmOssAttrMap`

## Download Fusion Data Loader Sample

Use this workflow when `dataloader_import_mode: "REST"` and a Fusion Data Loader sample is needed for the task’s business objects.

1. Confirm that `subscriptionGroupingRuleSets`, `subscriptionGroupingRuleSets_publishGroupingRuleSets`, and `subscriptionGroupingRuleSets_updateOmOssAttrMap` are the exact registered Data Loader business objects.
2. Generate the default editable XLSX samples through `core.data-loader`:

   ```bash
   python3 core/data-loader/scripts/generate_sample_dat.py \
     "subscriptionGroupingRuleSets" \
     "subscriptionGroupingRuleSets_publishGroupingRuleSets" \
     "subscriptionGroupingRuleSets_updateOmOssAttrMap" \
     --output-dir "<project-artifact-directory>"
   ```

3. Keep each business object's generated workbook set together:
   - editable sample workbook
   - attribute-details workbook
   - key-fields workbook
4. Review the generated headers and key fields before preparing source data. The operation uses read-only Fusion metadata and does not upload or import data.
5. Use the generated editable workbooks as the starting point for the later Data Loader preparation and approval workflow.

## Usage

Use this metadata file to view and review grouping rule sets and to prepare, validate, and submit approved Data Loader REST source data for a grouping rule set under `Integration Setup`.

## Supported Scope

This task may list rule sets, retrieve a selected rule set, retrieve its SplittingRuleAttrs and rule-builder ConditionJson enclosures, retrieve child grouping rules, resolve their read-only attribute enclosures, and prepare Data Loader REST source data for `subscriptionGroupingRuleSets`, `subscriptionGroupingRuleSets_publishGroupingRuleSets`, and `subscriptionGroupingRuleSets_updateOmOssAttrMap`.

CSV export/import remains catalog-unsupported. For this task, setup-data import, publishing, and Order Management-to-Subscription attribute-map updates are through **Data Loader REST** for the registered objects listed above. Create, enable/disable, publish, map update, and other updates must use `core.data-loader` and complete its live-schema, immutable-preview, Task Hook, and explicit-approval gates before the first upload or initiation request.

## Read-Only Order Management to Subscription Attribute Map

When the Order Management to Subscription attribute map is requested, call `getOmOssAttrMap` only through `core.fusion-api.rest-api-client`:

```text
POST /crmRestApi/resources/11.13.18.05/subscriptionGroupingRuleSets/action/getOmOssAttrMap
Content-Type: application/vnd.oracle.adf.action+json
REST-Framework-Version: 9
{}
```

This is a read-semantic action. Render the required `result` string as the Order Management-to-Subscription mapping; do not create, modify, publish, or infer mappings. If the action returns no `result` or fails, stop and report the sanitized failure without automatic retry. The action contract is documented in [Get order management to subscription attribute mapping](https://docs.oracle.com/en/cloud/saas/sales/faaps/op-subscriptiongroupingrulesets-action-getomossattrmap-post.html).

## Import Setup Data Through Data Loader REST

Use this route only for an explicitly requested create or update of grouping-rule-set setup data.

1. Generate the live-metadata sample for `subscriptionGroupingRuleSets` using the workflow above. Treat the returned sample workbook, attribute-details workbook, and key-fields workbook as the source of truth for file layout, mandatory fields, key fields, child structures, and supported operations.
2. Build the source workbook from the validated sample. Preserve every required parent/child relationship; do not derive a Data Loader file from the REST JSON example below.
3. Route validation and preparation through `core.data-loader`. It must confirm the registered business object, live schema, file format, mapping, archive shape, and target environment before upload.
4. Create an immutable approval preview for the exact prepared archive. For this task, invoke the Data Loader Task Hook only after the final archive is prepared and immediately before upload.
5. Ask for and obtain explicit approval immediately before `core.data-loader` uploads or initiates the reviewed archive. Revalidate the archive checksum and approval envelope at execution time.
6. On a rejected schema, mapping, privilege, upload, initiation, or processing result, stop and preserve the applicable redacted diagnostic. Do not retry an upload or initiation without a new valid approval.

The Data Loader REST route is the only import and publishing route declared here. It does not authorize CSV task import or direct REST mutation.

### Data Loader Publish Field Rules

Use `subscriptionGroupingRuleSets_publishGroupingRuleSets` only for a publish request. The publish source has one row and must contain `Content-Type` set to `application/vnd.oracle.adf.action+json` and `REST-Framework-Version` set to `9`, with `RestAction` set to `POST`. Do not supply `GroupingRuleSetNumber`; its omission publishes the grouping rule sets in scope for the selected environment. Generate the current live sample, validate the source, create an immutable approval preview, and obtain explicit approval immediately before upload and initiation.

### Data Loader Order Management-to-Subscription Attribute Map Update Rules

Use `subscriptionGroupingRuleSets_updateOmOssAttrMap` only for an explicit update of the Order Management-to-Subscription attribute map. Generate the current live sample and use its exact headers, required values, and operation shape as the source of truth; do not derive an update source from the read-only `getOmOssAttrMap` response. Validate the immutable source and obtain explicit approval before upload and initiation.

### Data Loader Create Field Rules

For a new grouping rule set, start with `GroupingRuleSetNumber` as `GRPS-RS-<normalized-rule-set-name>`. Before using it, query `/crmRestApi/resources/latest/subscriptionGroupingRuleSets` for an exact matching `GroupingRuleSetNumber`. If it exists, try `_1`, then `_2`, and continue with the lowest unused numeric suffix. Use the resulting unique value on the parent sheet and every `ruleBuilderConditions` and `subscriptionGroupingRules` row. For example, `Test Aj 2` starts as `GRPS-RS-TESTAJ2`. Leave `ConditionNumber` and `GroupingRuleNumber` empty so Fusion can generate them. Also leave `GroupingRuleSetId`, `ConditionId`, `GroupingRuleId`, and every `ObjectVersionNumber` empty; Fusion generates the IDs and version values during creation. Do not reuse a value returned from another rule set or child record. Default `EnabledFlag` to `true` for both the new rule set and every new grouping rule unless the requester explicitly selects disabled; use `false` to disable.

Before preparing source data, also query `/crmRestApi/resources/latest/subscriptionGroupingRuleSets` for the requested parent `Rank`. If a rule set already uses that rank, stop before source generation, identify its Grouping Rule Set name and number to the requester, and ask for a different rank. Do not automatically change the requested rank or prepare an archive until the requester supplies a new one.

For a create source, include the generated `GroupingRuleSetNumber` on the `subscriptionGroupingRuleSets` parent sheet and every child row to link both child sections to their generated parent PUID. On each `ruleBuilderConditions` row, set `ReferenceEntityName` to `OSS_GROUPING_RULE_SETS`. Build child sections from the current live Data Loader template plus the confirmed relationship key.

## Enable or Disable a Grouping Rule Set

Treat enable or disable as a Data Loader update. First resolve the exact existing `GroupingRuleSetNumber`, then build a parent-only source with `RestAction` set to `PATCH`, `GroupingRuleSetNumber`, and `EnabledFlag`: use `true` to enable or `false` to disable. Do not include IDs, version fields, name, rank, attributes, selection data, or child sections. Complete the Data Loader validation, immutable-preview, Task Hook, and explicit-approval gates before upload; do not retry a failed upload or initiation without a new approval.

When the requester does not supply a grouping-rule name, generate it as `Rule_<rank>_<object>_<attribute>`, for example `Rule_1_subscriptions_BillToAccountId`.

## Default Display

When listing grouping rule sets without a specific rule-set request, show Grouping Rule Set, Number, Rank, and Status. Derive Status from `EnabledFlag` as `Enabled` or `Disabled`. Do not show Selection Condition unless the user explicitly requests it.

When showing one specific grouping rule set, show its name, number, rank, and status, then show a Segregation Rule section by default. Its Mandatory Attributes are BusinessUnitName, LegalEntityName, PrimaryPartyName, Currency, Freeze Price, Pricing system, Pricing Strategy, and Subscription Profile. Under Additional Attributes, resolve `SplittingRuleAttrs` and render each returned attribute as an Attribute entry; show `None defined` when it is empty. Then show `ruleBuilderConditions` by default. Resolve each condition’s `ConditionJson` enclosure and render each condition in the Selection Rule layout: Attribute, Operator, and Value. If the collection is empty, show `None defined`; if a ConditionJson enclosure cannot be parsed, show the redacted raw condition JSON for review. Then show child grouping rules in a table with Name, Rank, Selection Rule, and Status. Resolve the child `GroupingRuleAttrs` enclosure before rendering the Selection Rule value. Do not show Selection Condition unless the user explicitly requests it.

Resolve every object attribute through the active Fusion connection’s `/crmRestApi/intelligentCRM/objects/{objectName}/attributes` endpoint. Derive the host from the current connected Fusion environment; never hard-code an environment host. For **Grouping Rules** attributes (`GroupingRuleAttrs`), send HTTP header `attribute-consumer-code: GroupingRuleGrouping`. For **Segregation Rule** additional attributes (`SplittingRuleAttrs`), send HTTP header `attribute-consumer-code: GroupingRuleSplitting`. For Selection Rule attributes, use the endpoint without either of those context-specific headers unless a separate consumer code is supplied. Match the returned `name` to the stored API attribute name and render `title (name)` when a title is available; use `name` only if no title is returned. Use the resolved `name`, not the display title, in every create-payload JSON string.

When a user supplies an object `DisplayName`, first resolve its `RestResource` from `{{baseUrl}}/crmRestApi/resources/latest/objectMetadata?q=objectProperties.PropertyCode='GroupingRuleGroupingCriteria'`, where `{{baseUrl}}` is the active Fusion connection’s base URL. Send `REST-Framework-Version: 9`, match the exact `DisplayName`, store the returned `RestResource`, and use it as `{objectName}` for the object-specific attribute lookup. Do not hard-code an object resource, substitute the `intelligentCRM` metadata route, or infer a resource from a display name.

### Specific Rule-Set Detail Presentation Contract

For every named grouping-rule-set detail request, use this order and these labels:

1. Parent rule-set summary: Name, Number, Rank, Status.
2. **Segregation Rule** with **Mandatory Attributes**, then **Additional Attributes** from `SplittingRuleAttrs` as Attribute entries.
3. **Selection Rule** for each `ruleBuilderConditions` `ConditionJson`, with Attribute, Operator, and Value.
4. **Grouping Rules** with Name, Rank, Selection Rule, and Status.

This is a read-only review presentation. Do not substitute raw child metadata for these sections unless an enclosure cannot be parsed.

## REST Structure Reference

The following REST representation documents the related grouping-rule structure. It is not a Data Loader source format and must not be submitted directly. `GroupingRuleAttrs`, `SplittingRuleAttrs`, and `ConditionJson` are JSON strings, not nested JSON objects.

```json
{
  "subscriptionGroupingRules": [
    {
      "GroupingRuleName": "Rule1",
      "Rank": "1",
      "EnabledFlag": true,
      "GroupingRuleAttrs": "{\"subscriptions\":[\"BillToAccountId\"]}"
    }
  ],
  "SplittingRuleAttrs": "{\"subscriptions\":[\"BillToAccountId\"]}",
  "EnabledFlag": true,
  "GroupingRuleSetName": "Test Aj",
  "Rank": 15,
  "ruleBuilderConditions": [
    {
      "ConditionGroupType": "INCLUSION",
      "ConditionGroupName": "INCLUSION-GRP-0",
      "DisplaySequence": "1",
      "QualifiedRestObjectName": "subscriptions",
      "ConditionJson": "{\"rule\":{\"conditions\":{\"allOf\":[{\"attribute\":\"BillToAccountId\",\"operator\":\"EQUALS\",\"value\":1001}]}},\"objectName\":\"subscriptions\"}"
    }
  ]
}
```

For a create or update request, resolve a supplied object DisplayName to RestResource with the declared `{{baseUrl}}` objectMetadata lookup, then resolve each selected display title to its object-specific attribute `name`. Use the REST structure only to understand the logical relationship between Segregation Rule additional attributes, Selection Rule rows, and Grouping Rules. Map those values into the current live Data Loader sample's confirmed fields; omit generated PUID, ID, and version fields for a create. Do not infer an unlisted loader field or direct REST payload. Create the immutable Data Loader approval preview, then request explicit approval before `core.data-loader` uploads or initiates the archive.
