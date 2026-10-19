# Elements Reference Lookups

## Source and Scope

Source: developer-provided `Elements-HDL.md` (2026-10-01) and its explicitly named local `ora_pay_ele_questionairre.json` example. These resources prepare Payroll Element Details for HDL; they do not submit a load. The local catalog has only one legislation/classification/category combination. Run the read-only LDG GET through `core.fusion-api.rest-api-client` using its standard Fusion REST adapter and `core/auth/fusionEnv.properties`.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| find_ldg_by_exact_name | An LDG name is supplied before questionnaire selection. | Supplied LDG name; target environment identity. | GET /hcmRestApi/resources/11.13.18.05/legislativeDataGroupsLOV with finder=findByWord;SearchTerms=&lt;URL-encoded LDG name&gt;,FilterAttributes=Name; fields=Name,LegislativeDataGroupId,LegislationCode; limit, offset, onlyData=true. | Name,LegislativeDataGroupId,LegislationCode | Collect all result pages, then require exactly one returned Name equal to the supplied LDG name; a word-search candidate is insufficient. | Name -> LegislativeDataGroupName; LegislativeDataGroupId -> LegislativeDataGroupId; LegislationCode -> legislationCode | Zero exact matches: invalid LDG. More than one: ambiguity. Stop without inferring legislation. |

The public contract is [Oracle REST API: Get all legislative data groups](https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-legislativedatagroupslov-get.html). The source document's tenant-specific `/rest/rv:...` URL is an example, not a reusable execution path. Authentication, client selection, pagination size, and privilege checks are owned by the active project workflow.

## Local Lookups

| Resolver | Runs When | Source Values | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|
| find_element_questionnaire | A unique LDG response has supplied legislationCode and the user selected classifications and category. | Local questionnaire catalog below, transcribed from the developer-named ora_pay_ele_questionairre.json; resolved legislationCode; user primary classification; optional secondary classification; category. | Match legislationCode, primaryClassificationName, secondaryClassificationName (empty when omitted), and category exactly. Require one matching catalog combination and preserve question order. The catalog has no LDG key, so do not claim narrower LDG-specific evidence. | Ordered RuleCode, Rule, and example Response for display only; confirmed user Response for HDL | Zero matches: explain the unsupported combination and request current target template data. Multiple matches: stop with ambiguity. Never treat example Response as confirmation. |

## Questionnaire Catalog

| LegislationCode | PrimaryClassificationName | SecondaryClassificationName | Category | Order | RuleCode | Rule | Example Response |
|---|---|---|---|---|---|---|---|
| US | Information | empty | Standard | 1 | SpecCurrency | Input Currency | US Dollar |
| US | Information | empty | Standard | 2 | Availability Rule | Should every person eligible for the element automatically receive it? | No |
| US | Information | empty | Standard | 3 | Hire Process | What is the earliest entry date for this element? | First Standard Earning Date |
| US | Information | empty | Standard | 4 | Terminate Process | What is the latest entry date for this element? | Final Close |
| US | Information | empty | Standard | 5 | Processing Level | At which employment level should this element be attached? | Assignment level |
| US | Information | empty | Standard | 6 | Processing Asg Level | Do you want the element to be processed at Payroll Assignment level? | Yes |
| US | Information | empty | Standard | 7 | Recurring Or NonRecurring | Does this element recur each payroll period, or does it require explicit entry? | Recurring |
| US | Information | empty | Standard | 8 | Multiple Entries | Can a person have more than one entry of this element in a payroll period? | No |
| US | Information | empty | Standard | 9 | CalculationRuleBasic | What is the calculation rule? | Flat amount |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| LDG result pagination | Keep the same tenant, finder, fields, and filters on each page. Stop on an incomplete or inconsistent collection; do not assert uniqueness from a partial result. |
| Catalog authority | Use this packaged questionnaire only after the LDG legislation and exact classification/category combination match. Do not import questions from another legislation or template. Fusion's element-template processing remains the final semantic validation of responses. |
| Unknown classification or answer LOV | The source gives no public resolver for classification, category, template ID, rule value ID, or allowed responses. Preserve confirmed values and let the routed Data Loader and Fusion validation report unsupported values; do not infer another HCM endpoint. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ELE.RESOLVE_LDG | decision | 4 | reference_lookup | unique->ELE.FIND_QUESTIONNAIRE;missing->ELE.HANDLE_ERROR;ambiguous->ELE.HANDLE_ERROR;failed->ELE.HANDLE_ERROR | ELE.CHECK_DEPENDENCIES | stop | Run find_ldg_by_exact_name through the routed read-only lookup step; retain one exact LDG, ID and legislation. |
| ELE.FIND_QUESTIONNAIRE | decision | 5 | reference_lookup | unique->ELE.VALIDATE_RESPONSES;missing->ELE.HANDLE_ERROR;ambiguous->ELE.HANDLE_ERROR | ELE.RESOLVE_LDG | stop | Run find_element_questionnaire and show every matching question in order for user answer and confirmation. |
