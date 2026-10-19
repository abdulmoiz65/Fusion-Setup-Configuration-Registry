---
skill_id: "cx.subscriptions.integration-setup.manage-algorithms-for-subscriptions-to-accounts-receivables"
name: "Manage Algorithms for Subscriptions to Accounts Receivables Advisory"
description: "Primary workflow for Subscriptions-to-Accounts-Receivables Algorithm_BO.xml review and Groovy drafting. Routes Service Mapping matters to its companion skill and resumes after its result; never deploys or imports Fusion changes."
layer: "pillar"
pillar: "CX"
offering: "Subscriptions"
functional_area: "Integration Setup"
functional_area_code: "CUSTOM_INTEGRATION_SETUP"
task_code: "CUSTOM_MANAGE_ALGORITHMS_FOR_SUBSCRIPTIONS_TO_ACCOUNTS_RECEIVABLES"
task_name: "Manage Algorithms for Subscriptions to Accounts Receivables"
parent_skill_id: "cx.subscriptions.integration-setup"
available_flag: "Y"
export_import_supported_flag: "N"
csv_export_import_supported_flag: "N"
type: "advisory"
execution_mode: "advisory"
owner_team: "CX subscriptions pillar team"
version: "0.1.16"
inputs:
  - "business_requirement"
  - "algorithm_bo_xml"
  - "service_mapping_source_xml"
  - "implementation_project_context"
outputs:
  - "service_mapping_assessment"
  - "service_mapping_configuration_handoff"
  - "groovy_proposal"
  - "algorithm_import_xml"
  - "validation_result"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-accounts-receivables"
token_usage_tracking:
  enabled: true
  granularity: "per_skill_run"
  artifact_type: "token_usage_record"
  default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
  estimation_method: "chars/4 estimate unless exact tokenizer or API accounting is available"
  required_fields:
    - "activity_start_time"
    - "skill_id"
    - "task"
    - "trigger"
    - "artifacts_written"
    - "files_read"
    - "estimated_input_tokens"
    - "estimated_output_tokens"
    - "estimated_total_tokens"
    - "estimation_method"
    - "notes"
---

# Manage Algorithms for Subscriptions to Accounts Receivables

## Purpose

Review the Subscription Management and Accounts Receivable integration algorithm, coordinate Service Mapping source validation, draft Groovy, and create an approved local Algorithm_BO.xml import artifact without deploying Fusion changes.

## Ownership and companion routing

This is the primary workflow. It owns Algorithm_BO.xml validation, version selection, action-expression review, Groovy drafting, Receivables output logic, and the local import artifact after explicit Groovy approval.

For any Service Mapping question—source entities, custom attributes, describe metadata, source XML, view-object mappings, service access, or publication—invoke `cx.subscriptions.integration-setup.manage-service-mappings-for-subscriptions-to-accounts-receivables`. Pass the business rule and known target and scope. When it returns, resume this workflow automatically using its confirmed sources, alternatives, assumptions, and prerequisites. Do not require the implementer to invoke this skill again.

## Mandatory inputs and export guidance

Run this mandatory preflight before every advisory, mapping, Groovy, validation, source-resolution, target-resolution, or use-case request. Require the current `Algorithm_BO.xml` and current Service Mapping source XML in the same request; the Service Mapping filename may vary. If either XML is missing, stop immediately and ask the implementer to attach both current exports. Validate that `Algorithm_BO.xml` is for `Subscription Management and Account Receivables Integration`, read every version, and reject the request unless the absolute highest `VersionNum` has `ActiveFlag=Y`; do not continue with an older active version. Validate that the Service Mapping source XML has `contextName="ARInterface"`; if it does not, stop and request the copied Subscription AR Integration source XML. Do not use chat cache, prior project artifacts, remembered file paths, or assumptions to pass this preflight.

When a customer use case involves general Subscription Management behavior, such as subscription lifecycle, products, pricing, billing, or Order Management-created subscriptions, read [Subscription Management General Reference](references/ora_subscription_management_general_reference.md) before an external documentation lookup. Use it for business context only; it does not replace current Receivables target, DFF, runtime, or Service Mapping source confirmation.

After preflight passes, classify the prompt using the Input Type 1-5 table in [Use-Case Resolution](references/ora_use_case_resolution.md) before drafting or blocking. If a use case omits a Subscriptions source entity or attribute, or a Receivables target column, follow that reference. If an attribute or business term is stated without a source object, do not default it to `Subscription`, `BillLines`, `Products`, `Charges`, `ProductAssociations`, or any other alias. Inspect the current `Algorithm_BO.xml` and Service Mapping XML for existing candidates. For Type 5 use cases with no source object, read the general Subscription reference first, then use current official Oracle documentation or web sources only if the generic reference does not identify a likely object and attribute. Based on that analysis, require the Service Mapping companion to run permitted environment describe checks across every relevant Subscriptions AR source family: subscriptions, subscriptionProducts, billLines, charges, and coveredLevels/ProductAssociations. Use the general Subscription reference and external documentation as discovery context only; they cannot replace describe validation or implementer acceptance. Present the recommended functional match, evidence, alternatives, assumptions, and any target or context limitations. When multiple described or exposed candidates have the same or similar business label across source families, resolve the functional owner before drafting: prefer the object explicitly named by the implementer, otherwise prefer the object whose business responsibility owns the term; treat copied, denormalized, or convenience attributes in another object as alternatives that require explicit acceptance. Do not choose a different object merely to avoid optional-cardinality access. An existing algorithm or documentation can suggest a candidate, but cannot alone confirm a new source alias, RA target, `AttributeContext`, or `FlexContext`; require an implementer decision naming the accepted candidate before drafting Groovy.

When the business scenario supplies source values but no Receivables target columns, use a target-suggestion pass before blocking. First compare the value's business meaning and data type against documented Standard columns in `RA_INTERFACE_LINES_ALL`; recommend a Standard target only when the documented column meaning is a direct functional match and the current interface contract supports Standard inserts for it. Derive the source data type from the current Service Mapping XML `attributeType` when the source is exposed, or from the companion describe result when describe identified the source; do not choose a DFF column family from the attribute label alone. If no Standard column fits, suggest candidate DFF targets from the appropriate confirmed family and scope: line-visible values normally use `TransactionLineDff`, transaction-level values normally use `TransactionInterfaceHeaderDff`, and `TransactionInterfaceLineDff` is considered only when the implementer or current contract specifically points to that family and the reservation rule passes. For DFF suggestions, pick the physical column family by the confirmed/described source type (`ATTRIBUTE<n>` for string/varchar/character and Boolean-as-code values, `ATTRIBUTE_DATE<n>` for date/datetime values, `ATTRIBUTE_NUMBER<n>` for number/integer/long/decimal values; header DFF uses the matching `HEADER_` family). A source whose name ends in `Id` must be recommended to `ATTRIBUTE_NUMBER<n>` only when XML or describe confirms a numeric type; if it is a varchar/display identifier, use `ATTRIBUTE<n>`. Scan the active algorithm and current Service Mapping XML for already-used slots in the same type family/context, and suggest the first available slot starting at 1 or the next slot after the highest used slot when gaps cannot be safely proven. Mark every such target as a recommendation, not a confirmation, and require implementer acceptance plus deployed DFF/context confirmation before Groovy.

Review the attached `Algorithm_BO.xml` and current Service Mapping source XML in the same run before drafting. The companion result is mandatory before Groovy uses a source that is absent from the supplied Service Mapping XML. The companion must identify the business object from the requirement, use its describe to find candidates, and obtain implementer confirmation; draft Groovy only from the returned confirmed source. If the companion cannot run describe because the runtime environment connection, authentication, privileges, or describe endpoint is unavailable, stop before source recommendation or Groovy drafting. Tell the implementer describe is not working, report the observed failure category, and ask whether to fix the runtime environment connection and rerun describe or proceed only with named, unconfirmed assumptions for review.

Require a source-resolution record for every business source used by Groovy. First, pass matching attributes already exposed in the current Service Mapping XML to the implementer and ask whether each is intended. For every missing source, require the companion to run the matching read-only describe and show the relevant candidate names, types, and mapping implications. If describe cannot be completed, do not silently replace it with assumptions. Stop, say describe is unavailable, and ask the implementer to choose either runtime connection remediation and a rerun of describe, or a review-only path using explicitly named assumptions that remain unconfirmed until accepted. The implementer may select a shown candidate, provide an exact source name, or explicitly say to use a named recommended default. A default is valid only when the companion identifies the exact candidate and the implementer accepts it; it never authorizes inventing an alias, view-object attribute, type, or flex context. Do not draft Groovy while any required source lacks this recorded decision.

For every implementation request in this skill, require the business requirement, current `Algorithm_BO.xml`, and current Service Mapping source XML as attachments or explicit file inputs in the same request. If either XML is absent from the current inputs, stop and ask the implementer to attach both current exports; do not proceed from chat cache, prior project artifacts, remembered paths, or default assumptions. The Service Mapping source filename is unrestricted because it is a copied source export. Validate that its transform context is `contextName="ARInterface"`; if the source is missing or the context differs, stop and request a valid source before reviewing, describing, or drafting Groovy.

When asked how to obtain Algorithm_BO.xml, instruct the implementer to select **Subscription Management and Account Receivables Integration** in **Subscriptions Setup > Dynamic Matrix Configuration > Manage Algorithms** without opening it, choose **Actions > Export Selected**, unzip the export, and attach `Algorithm_BO.xml`.

Validate that the export is for `Subscription Management and Account Receivables Integration`. Read all versions and their `ActiveFlag` values. Only proceed when the absolute highest `VersionNum` has `ActiveFlag=Y`. If the absolute highest version is not `Y`, inform the implementer that the highest version is not in In Progress state and stop the advisory, Groovy, and XML-edit path.

## Existing action handling

Ignore `//` and `/* ... */` comments while determining whether active Groovy exists. If the selected action has only the delivered block-comment sample and no active Groovy, remove that sample before adding new logic. If it contains active Groovy, ask whether to replace it or add new logic above it, and ask whether formatting is allowed.

If asked to copy Groovy from another version, copy it to the highest eligible version. Ask whether it may be formatted. If not, retain it unchanged and append new documented logic after it.

Before drafting, read every `contain(...).cardinality(...)` declaration on the selected action. For each alias with cardinality `ZeroOrOne`, generated Groovy must use null-safe navigation (`<alias>?.<attribute>`) on every direct dereference in conditions, expressions, and `ARInterface.insert` values. An explicit non-null guard may still be added for business clarity, but it does not permit later direct `<alias>.<attribute>` dereferences. The only allowed exception is to assign a null-safe value to a local variable inside or before the guard and use that local variable afterward. Direct property access is permitted only for an alias whose cardinality is confirmed as `One` or for a local variable derived from a null-safe optional alias. Derive aliases and required handling from the selected action; do not hardcode entity names. If source resolution selected an optional functional owner, use that selected alias consistently in conditions and values with null-safe handling; do not switch to another same-name candidate from a required or primary object unless the implementer explicitly accepts that object as the source. If cardinality metadata is absent or ambiguous, stop and request it.

## Mandatory Groovy layout

Keep these sections in every selected action expression, with one blank line beneath each section comment even when it contains no Groovy:

```groovy
/* Groovy applicable for both invoice and credit memo lines */

/* Groovy applicable for invoice lines */

/* Groovy applicable for only credit memo lines */
```

Place each `ARInterface.insert([ ... ])` in its applicable section. Immediately precede every insertion with exactly one concise one-line `/* ... */` comment that describes that insertion only.

Before using `TransactionType` in any normal AR mapping, resolve the transaction class expression from the current Service Mapping XML mapping where `viewObjectAttribute="TransactionClass"`. Use the exposed alias and attribute name from that mapping, not a guessed name. For example, if `BillLines.TransactionType_Custom` maps to `TransactionClass`, use `TransactionType: BillLines.TransactionType_Custom`. If the same insert applies to both invoice and credit memo lines, place one insert in the both-scope section with `TransactionType` set to the resolved expression and no `if` guard. If an insert is invoice-only or credit-memo-only, guard it with `if` / `else if` using the resolved expression, for example `<resolved_transaction_class_alias> == 'INV'` or `== 'CM'`. Do not duplicate the same both-scope insert as separate hardcoded `TransactionType: 'INV'` and `TransactionType: 'CM'` blocks.

Use only a documented `ARInterface.insert` contract. For a normal AR target mapping, use the confirmed target name, value, context, optional DFF flex context, and confirmed transaction scope. For a confirmed skip-line control, use `AttributeName: 'SkipBillLines'`, `AttributeValue: 'true'`, `AttributeContext: 'SubscriptionsSetup'`, and a confirmed `TransactionType`. Resolve the transaction class expression from the current Service Mapping XML, just as for normal mappings. If the skip applies to both invoice and credit memo lines, set `TransactionType` to the resolved transaction-class expression, for example `BillLines.TransactionType_Custom`, with no `INV`/`CM` split. If the skip is invoice-only or credit-memo-only, use a mutually exclusive guard from the resolved transaction-class expression and set the matching transaction type. Do not add `FlexContext` or map metadata such as `XsiType` or `AttributeType`, and do not substitute a Bill Lines property write or silent omission for the confirmed skip control. All source aliases, target names, flex contexts, conditions, and transaction scopes remain request-specific and must be confirmed from the current inputs.

Resolve every Receivables target from the public Oracle `RA_INTERFACE_LINES_ALL` reference before drafting. Read [RA Interface Lines Target Reference](references/ora_ra_interface_lines_all_reference.md) whenever selecting an AR target. Use attached mapping documents only as supplemental business-mapping evidence. Do not infer `AttributeContext` or `FlexContext` from a table column name; require the current Subscriptions AR interface contract or deployed Receivables DFF configuration to confirm them. Resolve the DFF family and segment index `<n>` from the current RA catalog. Use `TransactionLineDff` when the contract identifies the regular line-DFF pattern `ATTRIBUTE<n>`, `ATTRIBUTE_DATE<n>`, or `ATTRIBUTE_NUMBER<n>`. Use `TransactionInterfaceLineDff` only when the contract identifies `INTERFACE_LINE_ATTRIBUTE<n>` and `<n>` is not internally reserved for the confirmed origin and flex context: for a subscription created in Subscription Management, reject `n` in `1..4`; for a subscription created from Order Management, reject `n` in `1..8`. If the target is reserved, stop and request a different deployed target; do not substitute an attribute or change context. Resolve header, reference-line, link-to-line, additional-reference, and any other DFF family independently from its physical RA pattern and confirmed interface context. Apply the Standard-target rule only when the target is confirmed as Standard.

For `TransactionInterfaceHeaderDff` targets, treat the RA table column and the `ARInterface.insert` `AttributeName` as related but different names. Confirm the physical header DFF column in `RA_INTERFACE_LINES_ALL`, then remove only the leading `HEADER_` prefix for the insert `AttributeName`: `HEADER_ATTRIBUTE5` maps to `AttributeName: 'ATTRIBUTE5'`, `HEADER_ATTRIBUTE_DATE1` maps to `AttributeName: 'ATTRIBUTE_DATE1'`, and `HEADER_ATTRIBUTE_NUMBER1` maps to `AttributeName: 'ATTRIBUTE_NUMBER1'`. Keep `AttributeContext: 'TransactionInterfaceHeaderDff'` and the confirmed deployed transaction-header DFF `FlexContext`. Do not use `HEADER_ATTRIBUTE*` as the `AttributeName` for `TransactionInterfaceHeaderDff` inserts unless a current interface contract explicitly overrides this rule.

For Groovy language constructs, runtime helpers, and excluded APIs, read [Groovy Function Guidance](references/ora_groovy_function_guidance.md) before drafting nontrivial expressions. For every confirmed Receivables target whose physical RA catalog data type is `DATE`, use `AttributeValue: toDate(<date_expression>)`; keep any requested date arithmetic inside `<date_expression>`. When the entire confirmed date expression is `now()`, use `AttributeValue: now()` directly and do not wrap it in `toDate(...)`. Apply only runtime helpers that are confirmed for the target algorithm. Use `def` only for a value reused by multiple expressions or a conditional calculation whose name materially improves readability. Inline a source alias, literal, or other value used only once in its `ARInterface.insert` or condition. Ask before replacing any standard Receivables mapping already populated by delivered logic.

## Groovy review and XML artifact

Present the complete proposed Groovy directly in the chat response for review. Persist the same proposal under the implementation project for traceability, but do not require the implementer to open an artifact to review it. The approval request must identify the exact chat-visible Groovy.

Wait for explicit approval of that exact Groovy before creating or modifying a local `Algorithm_BO.xml`. Preserve implementer-supplied Groovy unless the implementer approves a stated correction. After approval, change only the highest `ActiveFlag` `Y` version, set `CustomizationFlag` to true when required, retain unrelated versions and actions, and create a syntactically valid local file named exactly `Algorithm_BO.xml`. Before handoff, extract the changed action expression and compare it with the approved Groovy; stop if they differ beyond line endings. After creating the local artifact, obtain the companion's Service Mapping configuration handoff and persist it under the project. It must list the confirmed sources, selected aliases, required entity-to-view-object mappings, types, access, publication prerequisites, and any configuration the implementer still must perform. Also provide a mapping table with source object, source attribute, Service Mapping alias, target `RA_INTERFACE_LINES_ALL` column, `ARInterface.insert` `AttributeName`, `AttributeContext`, `FlexContext`, transaction scope, and whether each value was confirmed or assumed as a named recommendation. Do not edit the exported Service Mapping XML.

Tell the implementer to ZIP `Algorithm_BO.xml` alone at the archive root and use **Actions > Import** in the same Manage Algorithms page. Do not create the ZIP, import it, publish, or execute Fusion runtime testing.

## Runtime handoff

Before manual testing, require the companion workflow to confirm any required Service Mapping sources are exposed and published. Then provide manual test guidance only.
