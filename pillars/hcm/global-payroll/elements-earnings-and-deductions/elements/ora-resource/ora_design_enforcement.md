# Elements Design Enforcement

## Enforcement Order

| Sequence | Step | What Must Happen |
|---|---|---|
| 1 | Questionnaire selection | Resolve the LDG's legislation, then match that code and the selected classifications/category to the packaged questionnaire. |
| 2 | Question integrity | Use exactly the matched RuleCode and Rule sequence; collect user-approved responses. |
| 3 | HDL route | Prepare PayrollElementDetails plus one PayrollElementQuestionnaire row per question; submit only through the routed Data Loader workflow. |

## Design Rules

| Applies When | Severity | Required Lookup | Blocking Condition | Recommendation | Fix Allowed? |
|---|---|---|---|---|---|
| Selecting a questionnaire | Error | find_element_questionnaire | No unique questionnaire match after LDG resolution. | Explain the mismatch and obtain current target evidence; never borrow another template's questions. | Yes, with corrected input or catalog evidence. |
| Rendering questionnaire rows | Error | find_element_questionnaire | Missing, duplicate, extra or unconfirmed question response; altered RuleCode or Rule. | Display every selected question and confirm exactly one answer for each. | Yes, before preview. |
| Rendering the DAT | Error | | The compact supplied parent/child HDL layout is changed without live Data Loader validation. | Keep the supplied compact header and let core.data-loader check the final artifact against live metadata before upload. | Yes, before loader preflight. |
| Submitting an element creation | Error | | No active routed project Run Book, no approved Data Loader artifact, or an attempted direct REST create. | Use core.data-loader and its own preview and approval gate. | Yes, after routed prerequisites. |

## Design Lookup Requirements

| Resolver | When Required | Values Needed | Source File |
|---|---|---|---|
| find_ldg_by_exact_name | Before questionnaire selection | LegislativeDataGroupName;LegislativeDataGroupId;legislationCode | ora_reference_lookups.md |
| find_element_questionnaire | Before asking for responses | Ordered RuleCode;Rule | ora_reference_lookups.md |

The source document requires at least one element eligibility after an Oracle example earnings element is created. Eligibility is a follow-on setup item and is not inferred as a PayrollElementDetails child row here. Country-specific labels and questions must come from the selected current template; the supplied source has no universal localized label map.

## Localization Documentation

These public links were supplied in `Elements-HDL.md`. Select the document for the resolved legislation; a country page does not supply a universal HDL questionnaire.

| Legislation or area | Public document | Use |
|---|---|---|
| US | [Elements for the US](https://docs.oracle.com/en/cloud/saas/human-resources/fapus/elements-for-the-us.html) | US classifications and naming guidance. |
| Canada | [Options for Creating Pretax and Voluntary Deduction Elements](https://docs.oracle.com/en/cloud/saas/human-resources/fapcd/options-for-creating-pretax-and-voluntary-deduction-elements-for.html) | Canadian deduction options. |
| Canada | [Options for Creating Involuntary Deduction Elements](https://docs.oracle.com/en/cloud/saas/human-resources/facid/options-for-creating-involuntary-deduction-elements-for-canada.html) | Canadian involuntary deduction options. |
| UK | [Create Absence Elements](https://docs.oracle.com/en/cloud/saas/human-resources/fabca/create-absence-elements.html) | UK absence classifications and category behavior. |
| India | [How Do I Set Up Elements for India?](https://docs.oracle.com/en/cloud/saas/human-resources/fatei/how-do-i-set-up-elements-for-india.pdf) | India element setup. |
| Oman | [Elements and Element Templates](https://docs.oracle.com/en/cloud/saas/human-resources/gaagw/elements-and-element-templates-for-oman.html) | Oman template and licensing context. |
| Mexico | [Payroll Elements for CFDI](https://docs.oracle.com/en/cloud/saas/human-resources/faadm/payroll-elements-for-cfdi.html) | CFDI payroll element context. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| ELE.CHECK_DESIGN | decision | 7 | design_enforcement | passed->ELE.HDL_GATE;blocked->ELE.HANDLE_ERROR | ELE.VALIDATE_RESPONSES | stop | Require a questionnaire match for the resolved legislation and exact confirmed question rows; reserve live DAT metadata checks for core.data-loader. |
