# Oracle Fusion HCM Performance Management: Request Feedback Template Best Practices

**Purpose:** This document is a reusable implementation reference for FSCR/Codex projects. Codex can use it when answering consultant prompts about **Feedback Templates** setup under Oracle Fusion Cloud HCM **Performance Management**. It covers both supported request-feedback template patterns:

1. **General Feedback Template**
2. **Performance Goal Feedback Template**

It also covers dependent setup such as questionnaires, profile options, security, notifications, Transaction Design Studio and Visual Builder Studio page behavior, lifecycle rules, migration, validation, and troubleshooting.

**Audience:** HCM Talent/Performance implementation consultants, solution architects, configurators, testers, and AI agents supporting implementation prompts.

**Last updated:** 2026-09-03

---

## 1. How Codex should use this document

When a consultant asks about request feedback templates, Codex should answer using this decision pattern:

```text
1. Identify whether the request is about:
   a. General requested feedback,
   b. Performance goal feedback,
   c. Participant feedback in a performance document, or
   d. Anytime feedback.

2. If it is about Feedback Templates setup:
   a. Confirm Workforce Development and Performance Management setup access.
   b. Confirm questionnaire dependencies.
   c. Confirm template type and lifecycle status.
   d. Confirm Redwood/profile/security/TDS dependencies.
   e. Provide setup steps, validation steps, and post-configuration tests.

3. If it is about feedback requests, not templates:
   a. Explain that the template is setup/configuration.
   b. Explain that feedback requests are transactional data.
   c. Route HDL/HSDL or REST discussion to FeedbackRequest, questionnaire, or feedback resources as appropriate.
```

Do **not** conflate these objects:

| Concept | What it is | Typical setup or runtime location | Notes |
|---|---|---|---|
| Feedback Template | Setup object that points to a questionnaire and controls which questionnaire is used for requested feedback | `My Client Groups > Performance > Setup Maintenance > Feedback Templates` | Primary scope of this guide |
| General requested feedback | Runtime feedback request about a person, not specific goals | Feedback Center, Request Feedback quick action, Touchpoints | Requires at least one active General Feedback template |
| Performance goal feedback | Runtime feedback request about one or more performance goals | Goals page or Touchpoints | Requires one active Performance Goal Feedback template and goal-feedback feature enablement |
| Participant feedback | Feedback inside a specific performance document process | Performance document / Manage Participant Feedback | Uses performance process flow, roles, sections, and questionnaires; separate from anytime requested-feedback templates |
| Anytime feedback | Unrequested feedback given to a person | Feedback Center / Give Feedback | Separate from Feedback Templates, although it may appear with requested feedback in downstream pages |

---

## 2. Source-basis summary

This guide is based on current Oracle Help Center and What's New guidance available as of the date above. The most important source points are:

- Feedback Templates require a questionnaire and must be Active to be available for creating feedback requests.
- The administrator route is `My Client Groups > Performance > Setup Maintenance > Feedback Templates`.
- If a Feedback Template is in use and Active, Oracle allows template name and description changes, but not questionnaire changes.
- An inactive template can't be used for new feedback requests.
- If a Feedback Template isn't in use, the questionnaire can be changed and the template can be deleted.
- For general feedback, organizations can have one or more active General Feedback templates.
- For feedback on goals, organizations must have one active Performance Goal Feedback template.
- In Redwood 26A, selecting one active goal-feedback template sets other goal-feedback templates inactive.
- Performance goal feedback from goals requires an active performance goal feedback template, goal drill-down mode, and the Request Feedback feature exposed by Transaction Design Studio.
- Redwood Request Feedback pages require `ORA_HCM_VBCS_PWA_ENABLED = Y` and `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED = Yes`.
- Goal-feedback support in Redwood also depends on `ORA_HRG_REQUEST_FEEDBACK_ENABLED = Yes` and, when used from Goals Center, Goals Center/Performance Documents Redwood enablement.
- Requested-feedback notifications are configured through Alerts Composer, and the reminder template is under `HRA_FEEDBACK_REQUESTED`.
- FeedbackRequest HDL/HSDL support is for feedback-request transaction data, not for configuring Feedback Templates.

See the **Source Links** appendix for direct Oracle URLs.

---

## 3. Scope and non-scope

### 3.1 In scope

This guide covers best practices for configuring, validating, migrating, and supporting:

- General Feedback Templates
- Performance Goal Feedback Templates
- Questionnaire templates and questionnaires used by Feedback Templates
- Question library considerations
- Feature profile options
- Security and role/privilege considerations
- TDS/VBS behavior for request feedback pages and goal feedback actions
- Notifications through Alerts Composer
- Integration and HDL/HSDL considerations for feedback requests
- Functional and regression test cases
- Diagnostics for common implementation issues

### 3.2 Out of scope

This guide does **not** define the full setup for:

- Performance document templates and process flows, except where they interact with requested feedback.
- Participant Feedback setup inside a performance document, except to separate it from requested feedback.
- Anytime Feedback setup, except where it shares Feedback Center or notification behavior.
- Full questionnaire implementation design beyond what is needed for Feedback Templates.
- Direct database update scripts, unsupported REST calls, or unsupported HDL objects.

---

## 4. Implementation object model

### 4.1 Setup object: Feedback Template

A Feedback Template is a Performance Management setup object that points to a questionnaire. It determines which questionnaire is presented when a user creates a requested-feedback transaction.

Recommended implementation attributes:

| Attribute | Best-practice treatment | Notes |
|---|---|---|
| Template Name | Required; make globally meaningful and stable | Use a naming convention because no public external-id contract is documented for this setup object |
| Description | Required by project standard even if optional in UI | Include purpose, audience, and template type |
| Status | Create or stage as Inactive where possible; activate only after validation | Active templates become selectable or used by runtime request-feedback flows |
| Template Type | Required | Use either General Feedback or Performance Goal Feedback |
| Questionnaire | Required | Must be active/usable and designed for requested-feedback use |
| Attributes to share | Required for Performance Goal Feedback templates where exposed | Controls which goal attributes are included in the request context |
| Lifecycle/use flag | Read and respect | In-use templates have restricted edit/delete behavior |

### 4.2 Runtime object: Feedback Request

A Feedback Request is transactional data created by employees, managers, HR specialists, Touchpoints, HDL/HSDL, or integrations. Do not model Feedback Requests as setup templates.

Oracle What's New for 24B documents HDL/HSDL support through the `FeedbackRequest` business object. It includes child objects `FeedbackRequestObjects` and `FeedbackResponse`. General feedback uses template code `ORA_GENERAL`; performance goal feedback uses `ORA_PERF_GOAL` and requires a performance goal associated with `FeedbackRequestObject` plus `RequestedForAssignmentId` populated.

### 4.3 Questionnaire dependency

A Feedback Template is only useful when its questionnaire is designed and available. The recommended dependency chain is:

```text
Question Library
  -> Questionnaire Template
     -> Questionnaire
        -> Feedback Template
           -> Runtime Feedback Request
```

Oracle questionnaire setup supports subscriber applications, folders, questionnaire templates, questionnaires, privacy, sections, randomization, required questions, and scoring where the subscriber supports it. For Performance Management, always confirm the subscriber/application value shown in the target tenant, because questionnaire LOV behavior can vary by page and feature.

---

## 5. Navigation and route selection

### 5.1 Primary administrator navigation

```text
My Client Groups
  > Performance
    > Setup Maintenance
      > Feedback Templates
```

This is the administrator route documented for managing Feedback Templates.

### 5.2 Related setup areas

| Dependency | Route or setup area | Why it matters |
|---|---|---|
| Questions | `Setup and Maintenance > Workforce Development > Questionnaires > Questions` or `My Client Groups > Performance > Questions` | Questions used in the questionnaire |
| Questionnaire Templates | `Setup and Maintenance > Workforce Development > Questionnaires > Questionnaire Templates` or `My Client Groups > Performance > Questionnaire Templates` | Required before creating questionnaires |
| Questionnaires | `Setup and Maintenance > Workforce Development > Questionnaires > Questionnaires` or `My Client Groups > Performance > Questionnaires` | Required before creating Feedback Templates |
| Profile Options | `Setup and Maintenance > Workforce Development > Manage Administrator Profile Values` | Controls Redwood, request feedback, goals, and notifications behavior |
| Alerts Composer | `Navigator > Tools > Alerts Composer` | Controls requested-feedback and reminder notifications |
| Transaction Design Studio | `My Client Groups > HCM Experience Design Studio > Transaction Design Studio` | Exposes or hides request-feedback actions and page attributes |
| Visual Builder Studio | VBS project for Redwood HCM pages | Exposes some Redwood-only buttons/properties such as AI Assist |
| Security Console | Security Console and HCM data security setup | Grants setup, request, view, REST, and Alerts Composer access |

### 5.3 Redwood route considerations

Oracle Redwood adoption documentation lists **Redwood Experience for Feedback Template** as a Redwood feature delivered for Talent/Performance setup pages. It also lists later features for Request Feedback Quick Action, Feedback Spotlight, Feedback Template control, and HR read-only Feedback Templates access.

Best practice:

```text
Do not assume the setup page is Redwood solely from the release number.
Confirm the page rendering, profile values, and available actions in the tenant.
Use the same functional route, but record whether the page opened in Redwood or responsive/classic UI.
```

For runtime requested-feedback pages, confirm these profile options where applicable:

| Profile option | Recommended value | Applies to |
|---|---:|---|
| `ORA_HCM_VBCS_PWA_ENABLED` | `Y` | Redwood HCM/VBCS pages |
| `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED` | `Yes` | Redwood Request Feedback pages and Feedback Spotlight integration |
| `ORA_HRT_ANYTIME_FEEDBACK_REDWOOD_ENABLED` | `Y`, if using Anytime Feedback Redwood pages | Feedback Spotlight page can be enabled through requested or anytime feedback Redwood profiles |
| `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` | `Yes`, when using Redwood Goals Center or Redwood performance documents | Required for Redwood Goals Center and performance documents |
| `ORA_HRG_REQUEST_FEEDBACK_ENABLED` | `Yes` | Enables request feedback for goals |
| `HRG_ENABLE_GOAL_DRILLDOWN_VIEW` | `Yes` | Required for goal detail/drill-down sections where performance-goal feedback is requested |

---

## 6. Template-type best practices

### 6.1 General Feedback Template

Use General Feedback templates for general requested feedback about a person, team interaction, behavior, project contribution, or other non-goal-specific feedback.

Oracle behavior to preserve:

- At least one active feedback template is required before users can create a requested-feedback transaction.
- For general feedback, more than one active General Feedback template can exist.
- If more than one active General Feedback template exists, the requester can select the questionnaire/template during request creation.
- If the selected questionnaire supports additional questions, the requester can add additional questions.
- Feedback may be shared depending on the requester role and page selections.

Best practices:

| Area | Recommendation |
|---|---|
| Naming | Prefix with `GEN_FB_` or use a business-friendly naming pattern such as `General Feedback - Project Retrospective` |
| Volume | Keep the number of active templates intentionally small; too many templates create user confusion |
| Questionnaire length | Use short questionnaires for anytime general feedback; avoid performance-document-sized forms |
| Additional questions | Enable only when the process expects requesters to tailor questions |
| Scoring | Avoid scoring unless a clear downstream report uses it; free-text feedback is often more useful |
| Sharing default | Align with privacy/legal policy; validate TDS page attributes for share checkboxes |
| Translation | Translate high-volume global templates and questionnaires before activation |
| Retirement | Inactivate old templates rather than deleting if they were used historically |

Recommended naming pattern:

```text
<scope> - <purpose> - <audience/region> - <version>
Examples:
General Feedback - Project Closeout - Global - v1
General Feedback - Collaboration Pulse - Sales - v2
```

### 6.2 Performance Goal Feedback Template

Use Performance Goal Feedback templates when users request feedback on one or more performance goals.

Oracle behavior to preserve:

- Users can request feedback for performance goals only when an active performance goal feedback template exists.
- Performance-goal feedback also requires administrator feature enablement for goals: drill-down mode and request-feedback exposure in Transaction Design Studio.
- Managers requesting goal feedback for team members must be able to update the performance goal.
- In Touchpoints, goal feedback uses the most recent/active performance goal feedback template automatically.
- Questions are repeated for each performance goal included in the request.
- Starting in Redwood 26A behavior, selecting a performance goal feedback template as active causes other goal-feedback templates to be set inactive.

Best practices:

| Area | Recommendation |
|---|---|
| Active count | Treat as exactly one active template per tenant/business design unless Oracle tenant behavior explicitly supports partitioning |
| Versioning | Create a new inactive version, validate, then activate it during a controlled change window |
| Question count | Keep the questionnaire short because every question is repeated for every selected goal |
| Goal attributes | Share enough goal context for useful feedback, but avoid oversharing sensitive/custom fields |
| Multi-goal requests | Test with one, several, and all goals; confirm question repetition and notifications |
| Private goals | Validate whether private goals can be selected and how feedback visibility is handled |
| Goal permissions | Test both employee self-request and manager team-member request |
| Rollout | Communicate that changing the active goal-feedback template affects new goal-feedback requests only |

Recommended naming pattern:

```text
Performance Goal Feedback - Global - FY27 - v1
Performance Goal Feedback - Sales - FY27 - v2
```

If the organization needs different goal-feedback questionnaires by region or business unit, first validate whether the tenant UI and runtime flow can distinguish those templates. Do not create multiple active performance-goal feedback templates without testing the active-template-selection behavior in the target release.

---

## 7. Questionnaire design standards

### 7.1 Questionnaire-template setup

Oracle questionnaires are created from questionnaire templates. Templates promote consistency and can enforce sections or questions that must appear in questionnaires. The questionnaire and template must use the same subscriber application.

Best practices:

```text
1. Create reusable questions first.
2. Create a questionnaire template for requested-feedback use.
3. Add sections and mandatory questions in the template only when every derived questionnaire must include them.
4. Create a questionnaire from the template.
5. Validate respondent experience in Preview.
6. Attach the questionnaire to a Feedback Template.
```

### 7.2 Subscriber and folder standards

Recommended folder strategy:

| Folder | Use |
|---|---|
| `Performance Requested Feedback` | General requested-feedback questionnaires |
| `Performance Goal Feedback` | Performance-goal feedback questionnaires |
| `Performance Participant Feedback` | Performance document participant feedback questionnaires |
| `Archive - Requested Feedback` | Inactive or superseded questionnaires/templates |

Subscriber best practice:

- Use the subscriber/application value exposed by the target tenant for the Feedback Template page.
- For performance-document participant feedback, Oracle documentation explicitly states that questionnaire templates should be assigned to **Performance 360** to make them available in performance documents.
- Do not assume a questionnaire built for performance documents is appropriate for requested feedback; design short, direct questionnaires for request-feedback flows.

### 7.3 Question standards

Recommended question design:

| Type | Best practice |
|---|---|
| Plain text / rich text | Use for qualitative feedback; use rich text if AI Assist is planned |
| Single choice | Use for simple sentiment or rating prompts |
| Multiple choice | Use sparingly; can be harder to interpret in performance feedback |
| Date / number | Use only when feedback captures factual milestone data |
| Scored responses | Use only with a defined reporting or analytics purpose |

Recommended general feedback question examples:

```text
1. What should this person continue doing?
2. What should this person consider improving?
3. What specific example supports your feedback?
```

Recommended performance goal feedback question examples:

```text
1. What progress have you observed on this goal?
2. What risks or blockers should the employee or manager consider?
3. What recommendation would help improve goal achievement?
```

### 7.4 Additional questions

Oracle allows requesters to add additional questions when the questionnaire template supports that capability. For participant feedback in performance documents, both the process-flow option and questionnaire setup can matter.

Best practices:

- For General Feedback, allow additional questions only for flexible coaching or project-feedback scenarios.
- For Performance Goal Feedback, allow additional questions only if managers/employees are trained; otherwise, the request can become inconsistent across goals.
- Include at least one required standard question so responses remain reportable.
- Test additional-question behavior in Redwood and responsive pages separately.

### 7.5 AI Assist considerations

Oracle's Redwood AI assistance for requested feedback requires Redwood Request Feedback pages and works only for questions with a **Rich Text Box** response type, not Plain Text Editor. The AI Assist button is not enabled by default and must be exposed through Visual Builder Studio. Oracle also notes data-center availability limits for generative AI features.

Best practices:

```text
IF AI Assist is required:
   verify tenant region eligibility;
   verify ORA_HCM_VBCS_PWA_ENABLED = Y;
   verify ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED = Yes;
   use Rich Text Box response type for questions;
   expose the AI Assist button in VBS;
   run legal/privacy review for AI-generated feedback.
ELSE:
   keep question response type based on normal user experience needs.
```

---

## 8. Profile-option dependency catalog

### 8.1 Required or commonly relevant profile options

| Profile option | Recommended value | Required for | Notes |
|---|---:|---|---|
| `ORA_HCM_VBCS_PWA_ENABLED` | `Y` | Redwood HCM pages | Foundation profile for VBCS/PWA Redwood pages |
| `ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED` | `Yes` | Redwood Request Feedback pages | Required for Redwood requested-feedback flows |
| `ORA_HRT_ANYTIME_FEEDBACK_REDWOOD_ENABLED` | `Y`, when Anytime Feedback Redwood pages are used | Redwood Feedback Spotlight page | Feedback Spotlight can be enabled by anytime or requested-feedback Redwood profile |
| `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` | `Yes`, when goal feedback is used from Redwood Goals Center | Redwood Goals Center and performance documents | Performance documents, check-ins, and Goals Center are tied together for Redwood |
| `ORA_HRG_REQUEST_FEEDBACK_ENABLED` | `Yes` | Request Feedback for Goals | Enables request-feedback capability for goals |
| `HRG_ENABLE_GOAL_DRILLDOWN_VIEW` | `Yes` | Goal feedback from goal details | Needed for goal drill-down/feedback sections |
| `HRA_PERF_AUTOSAVE_INTERVAL` | Enterprise standard | Performance document autosave, not directly template setup | Include in Performance Management profile preflight only if performance documents are involved |
| `BIP_EMAIL_NOTIFICATION_HCM` | Enterprise standard | Email notifications | Global HCM BI Publisher email notifications |
| `BIP_EMAIL_NOTIFICATION_HCM_TALENT` | Enterprise standard | Talent email notifications | Talent-level email notification control |
| `BIP_ONLINE_NOTIFICATION_HCM` | Enterprise standard | Worklist notifications | Global HCM worklist notifications |
| `BIP_ONLINE_NOTIFICATION_HCM_TALENT` | Create/set per enterprise standard if used | Talent worklist notifications | Oracle notes this may not be delivered and may need creation in some contexts |

### 8.2 Profile preflight algorithm

```text
For every Feedback Template implementation:
1. Read tenant release and UI mode.
2. Confirm the template setup page opens and available actions match the user's role.
3. If Redwood requested-feedback runtime is in scope:
      verify ORA_HCM_VBCS_PWA_ENABLED = Y;
      verify ORA_HRA_REQ_FEEDBACK_REDWOOD_ENABLED = Yes.
4. If performance-goal feedback is in scope:
      verify ORA_HRG_REQUEST_FEEDBACK_ENABLED = Yes;
      verify HRG_ENABLE_GOAL_DRILLDOWN_VIEW = Yes;
      verify ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED = Yes when Goals Center is Redwood.
5. If notifications are in scope:
      verify BI Publisher email/worklist profiles and Alerts Composer templates.
6. Report all profile gaps before creating or activating templates.
```

---

## 9. Security best practices

### 9.1 Setup security

For implementation setup, the user typically needs the Application Implementation Consultant role or a custom role with equivalent access to Performance Management setup tasks. Oracle's Performance Management implementation guide states that implementing Performance Management requires the `ORA_ASM_APPLICATION_IMPLEMENTATION_CONSULTANT_JOB` role.

Recommended setup roles/privileges:

| Capability | Security need |
|---|---|
| Access Workforce Development setup | Application Implementation Consultant or custom implementation role |
| Manage Feedback Templates setup page | Performance setup administration privileges in the customer's role model |
| Manage Questions, Questionnaire Templates, Questionnaires | Questionnaire/Profile/Performance setup privileges |
| Configure profile options | Manage Administrator Profile Values access |
| Configure Alerts Composer | `HRC_ACCESS_ALERTS_COMPOSER_PRIV` |
| Configure TDS | HCM Experience Design Studio / TDS administration access |
| Configure VBS page properties | Visual Builder Studio access for Redwood HCM pages |
| View employee/manager runtime behavior | Representative Employee, Line Manager, HR Specialist roles with correct data security |

### 9.2 Runtime security

Runtime users need feature and data access. Oracle security references show these capabilities across employee, manager, and integration roles:

| Runtime capability | Common security object or privilege area |
|---|---|
| Employee requests feedback for self | `Request Feedback` on Performance Feedback Request |
| Manager requests feedback for reports | `Request Feedback` with person/assignment security profile access |
| User views requested feedback | `View Requested Feedback` on Performance Feedback Request |
| REST request-feedback integration | `Use REST Service - Feedback Requests by Worker or Manager` |
| REST read-only feedback-request integration | `Use REST Service - Feedback Requests Read Only` |
| Runtime template LOV/read access | `Use REST Service - Feedback Templates List of Values` and/or `Use REST Service - Feedback Templates Read Only` |
| Goal-feedback request | Goal-management view/update privileges plus request-feedback feature/profile/TDS settings |
| Touchpoints request feedback | `Access Touchpoints by Worker` or `Access Touchpoints by Manager`, as applicable |

### 9.3 HR read-only setup access

Oracle 25D What's New introduces read-only access behavior for the Feedback Templates setup page for HR analyst users. If a user has both create/edit privileges and the read-only privilege, create/edit takes precedence.

Best practice:

```text
1. Separate configurator and read-only analyst roles.
2. Do not mix read-only and create/edit privileges unless intentional.
3. Test the Feedback Templates page with both roles.
4. Document the expected access matrix in the FSCR.
```

### 9.4 Data security

Requested-feedback visibility depends on person and assignment security, requester/provider relationships, share settings, and role. Always test with real representative scenarios:

| Scenario | Test actors |
|---|---|
| Employee requests feedback for self | Employee, feedback provider, employee's manager |
| Manager requests feedback for direct report | Manager, employee, provider |
| Manager requests feedback for indirect report | Manager with security profile access, employee, provider |
| HR requests feedback for worker | HR Specialist with person/assignment access, employee, provider |
| Feedback not shared with manager | Employee, manager, HR if HR has special access |
| Terminated employee after request | Requester and manager visibility after termination |

---

## 10. Lookup and value-set best practices

### 10.1 Template type values

Do not create or modify template-type lookup values for the two delivered setup patterns. Use the values supplied by Oracle:

- General Feedback
- Performance Goal Feedback

For HDL feedback-request transactions, Oracle documents template codes:

- `ORA_GENERAL` for general feedback
- `ORA_PERF_GOAL` for performance goal feedback

These HDL codes are for **FeedbackRequest transaction loading**, not for configuring the Feedback Templates setup page.

### 10.2 Question and questionnaire lookups

Questionnaires may use folders, categories, sections, response types, scoring values, rating choices, or customer-defined classifications. Use lookup/value-set configuration only when required by the questionnaire design.

Best practices:

| Area | Recommendation |
|---|---|
| Response choices | Standardize answer labels and scoring before creating questionnaires |
| Categories | Use categories to group questions by purpose, not by template version |
| Value sets | Use value sets for DFFs or validated questionnaire metadata only when needed |
| Translations | Translate lookup meanings and questionnaire content together |
| Migration | Migrate lookup/value-set dependencies before questionnaires and templates |

### 10.3 Do not over-customize

Avoid creating custom lookups for:

- Template type labels
- Status labels
- Core request-feedback lifecycle statuses
- Delivered feedback-request transaction types

Customizing delivered semantics creates reporting and upgrade risk.

---

## 11. Flexfield best practices

### 11.1 Performance Management DFF scope

Oracle documents these Performance Management descriptive flexfields:

| DFF code | Description |
|---|---|
| `HRA_DOC_TYPES_B` | Additional fields for Performance Document Types |
| `HRA_TMPL_DEFNS_B` | Additional fields for Performance Templates |
| `HRA_EVALUATIONS` | Additional fields for evaluation in a performance document |
| `HRA_SECTION_DEFNS_B` | Additional fields for Performance Template Sections |
| `HRA_TMPL_SECTIONS` | Additional fields for section details on a Performance Template |
| `HRA_EVAL_ITEMS` | Not in use |
| `HRA_EVAL_RATINGS` | Not in use |

Oracle's public Performance Management DFF list doesn't identify a dedicated Feedback Template DFF. Therefore:

```text
Do not promise or design a Feedback Template DFF unless the target tenant exposes one.
Use DFFs on related performance objects only when a documented DFF exists.
```

### 11.2 DFF dependency rules

When DFFs are part of a broader Performance Management implementation:

1. Define lookup codes and value sets first.
2. Configure DFF contexts and segments.
3. Deploy flexfields.
4. Verify Redwood rendering and TDS/VBS support.
5. Include DFF values in migration/test scripts.
6. Confirm reports and extracts use the intended DFF fields.

### 11.3 Request-feedback data capture

If the business asks to capture additional metadata with requested feedback, first determine where that data belongs:

| Need | Recommended location |
|---|---|
| Ask feedback provider a question | Questionnaire question |
| Capture setup classification of the template | Template naming convention or, if available, setup metadata |
| Capture employee/manager runtime context | FeedbackRequest transaction data or reporting dimensions |
| Capture performance-document attributes | Performance Management DFFs on documented performance objects |
| Capture goal attributes | Goal Management DFFs on goal/goal plan, if in scope |

---

## 12. Transaction Design Studio and Visual Builder Studio

### 12.1 TDS requirements for general requested feedback

Oracle documents that the Select Peers and Select Direct Reports buttons are hidden by default in Create Feedback Request. Administrators can make them visible using Transaction Design Studio. Oracle also documents that the Share feedback with me checkbox is visible by default and can be hidden through TDS.

Recommended TDS checks:

| Page/region | Attribute | Default or behavior | Best practice |
|---|---|---|---|
| Feedback action / Who do you want to ask | Select Peers | Hidden by default | Expose only if peer selection is part of process |
| Feedback action / Who do you want to ask | Select Direct Reports | Hidden by default; only meaningful when recipient is a manager | Expose only for manager/team feedback use cases |
| Feedback sharing | Share feedback with me | Visible by default | Hide only after privacy/legal review |
| Feedback sharing | Share feedback with manager/employee | Role-dependent | Validate for self, manager, and HR scenarios |

### 12.2 TDS requirements for performance goal feedback

To request feedback from the Goals page, Oracle documents that administrators must enable:

- Drill-down mode
- Feedback requests in Transaction Design Studio
- For managers, ability to update the performance goal

Recommended TDS checks:

```text
1. Confirm Request Feedback action is visible on goal detail or selected-goals action menu.
2. Confirm Feedback section is visible in goal drill-down/details.
3. Confirm employee can request feedback for own eligible goals.
4. Confirm manager can request feedback only when the manager can update the team member's goal.
5. Confirm HR Specialist behavior if HR-requested goal feedback is in scope.
```

### 12.3 VBS requirements

Use Visual Builder Studio for Redwood-only page properties and UI extensions. Examples from Oracle What's New include:

- AI Assist button visibility for requested feedback
- Redwood Request Feedback enhancements such as peer/team provider selection
- New page properties for sharing requested feedback
- Feedback Center/Spotlight page properties

Best practice:

```text
Do not implement VBS changes as a hidden prerequisite.
Document every VBS change in the FSCR with:
- page name;
- rule/property name;
- default behavior;
- new behavior;
- business owner approval;
- test scenarios.
```

---

## 13. Notifications and reminders

### 13.1 Alerts Composer setup

Oracle documents that HR specialists can configure check-in and requested-feedback notifications using Alerts Composer. The user must have `HRC_ACCESS_ALERTS_COMPOSER_PRIV`.

Navigation:

```text
Navigator
  > Tools
    > Alerts Composer
```

Search keywords:

```text
feedback
check-in
HRA_FEEDBACK_REQUESTED
```

### 13.2 Requested-feedback notifications

Requested feedback involves notifications to:

- Feedback providers when a request is sent
- Feedback providers when the due date nears, if reminder template is enabled
- Requester when feedback is completed or revised
- Manager when completed or revised feedback is shared with them
- Feedback provider when a thank-you note is sent, if the relevant template is enabled

### 13.3 Reminder setup

Oracle documents this reminder setup:

```text
1. Go to Alerts Composer.
2. Search for HRA_FEEDBACK_REQUESTED.
3. Open the alert.
4. On Templates, enable Requested feedback reminder.
5. Save and close.
```

### 13.4 Best practices

| Area | Recommendation |
|---|---|
| Template enablement | Explicitly document which requested-feedback templates are enabled or disabled |
| Due-date reminders | Enable reminders only if due dates are used consistently |
| Thank-you note | Enable only after confirming business value; Oracle notes the thank-you note is visible in email/worklist but isn't saved in the application |
| Matrix managers | Review 25D/26A+ What's New behavior for matrix manager notifications when feedback is shared |
| Testing | Test email and worklist notifications separately |
| Environment migration | Alerts Composer changes often require environment-specific validation |

---

## 14. General Feedback Template setup workflow

### 14.1 Input contract for implementation automation

```yaml
operation: create_or_update
object_type: feedback_template
template_type: general_feedback

feedback_template:
  name: "General Feedback - Project Closeout - Global - v1"
  description: "Used to request post-project feedback from peers or collaborators."
  status: "Inactive"
  questionnaire_name: "QNR - General Feedback - Project Closeout - v1"

controls:
  activate_after_validation: false
  allow_questionnaire_change_if_in_use: false
  allow_delete: false
  require_notification_validation: true
  require_runtime_test: true
```

### 14.2 Create workflow

```text
1. Run common preflight:
   - Workforce Development enabled.
   - Performance Management setup accessible.
   - User has setup privileges.
   - Target route opens Feedback Templates page.

2. Validate questionnaire:
   - Questionnaire exists.
   - Questionnaire belongs to the correct subscriber/application context.
   - Questionnaire is active or otherwise selectable.
   - Required questions, sections, and additional-question behavior match design.
   - Translations are complete if global rollout is planned.

3. Search existing templates:
   - Exact template name.
   - Template type = General Feedback.
   - Questionnaire match.

4. Create template:
   - Name.
   - Description.
   - Status = Inactive for staged validation where possible.
   - Template Type = General Feedback.
   - Questionnaire = approved questionnaire.

5. Save and re-open.

6. Validate list page:
   - Template appears.
   - Status correct.
   - In-use indicator not set.

7. Activate only when approved.

8. Run runtime validation:
   - Request Feedback page opens.
   - General template appears in questionnaire/template selector.
   - Additional questions behavior is correct.
   - Share checkboxes behave as designed.
   - Notifications are sent as configured.
```

### 14.3 Update workflow

```text
IF template is Active and in use:
   permit name and description update only.
   block questionnaire change.

IF template is not in use:
   permit questionnaire change when explicitly requested.
   validate questionnaire before saving.

IF status is changed to Inactive:
   warn that no new feedback requests can use the template.
   existing feedback requests remain historical data.

IF deletion requested:
   allow only when not in use and destructive actions are explicitly permitted.
```

### 14.4 Validation scenarios

| Scenario | Expected result |
|---|---|
| One active General Feedback template exists | Request Feedback can be created |
| Multiple active General Feedback templates exist | User can choose among templates/questionnaires |
| No active General Feedback template exists | General feedback request can't proceed |
| Template inactive | Not available for new feedback request |
| Template in use, questionnaire change attempted | Blocked |
| Template not in use, questionnaire change attempted | Allowed after validation |
| Questionnaire allows additional questions | Additional Questions region available |
| Questionnaire doesn't allow additional questions | Additional Questions region unavailable |
| Select Peers hidden by TDS | Button not visible |
| Select Peers exposed by TDS | Button visible and functional |
| Requested feedback reminder enabled | Reminder notification sent near due date |

---

## 15. Performance Goal Feedback Template setup workflow

### 15.1 Input contract for implementation automation

```yaml
operation: create_or_update
object_type: feedback_template
template_type: performance_goal_feedback

feedback_template:
  name: "Performance Goal Feedback - Global - FY27 - v1"
  description: "Standard questionnaire for requesting feedback on performance goals."
  status: "Inactive"
  questionnaire_name: "QNR - Performance Goal Feedback - Global - v1"
  attributes_to_share:
    - goal_name
    - goal_description
    - success_criteria
    - target_completion_date
    - goal_status

controls:
  activate_after_validation: false
  enforce_single_active_goal_feedback_template: true
  allow_inactivate_existing_active_goal_template: false
  require_goal_runtime_test: true
  require_touchpoints_test: false
```

### 15.2 Create workflow

```text
1. Run common preflight.

2. Confirm goal-feedback feature dependencies:
   - ORA_HRG_REQUEST_FEEDBACK_ENABLED = Yes.
   - HRG_ENABLE_GOAL_DRILLDOWN_VIEW = Yes.
   - Request Feedback action/section exposed in TDS.
   - Redwood Goals Center profiles are enabled if using Redwood Goals Center.

3. Validate questionnaire:
   - Questionnaire exists.
   - Questionnaire is short enough for per-goal repetition.
   - Additional-question behavior is intentional.
   - Rich Text Box response type used if AI Assist is required.

4. Search existing Performance Goal Feedback templates.

5. If another active goal-feedback template exists:
   - In 26A+ Redwood behavior, activating the new one may inactivate all others.
   - Treat as consequential change.
   - Require explicit approval before activation.

6. Create new template inactive.

7. Configure attributes to share in the feedback request.

8. Save and re-open.

9. Activate only when approved.

10. Run goal-feedback runtime validation:
   - Employee can select one eligible goal and request feedback.
   - Employee can select multiple eligible goals and request feedback.
   - Manager can request feedback for a team member only when manager can update the goal.
   - Feedback provider receives separate expected notifications when multiple goals are included.
   - Questions repeat correctly per selected goal.
```

### 15.3 Activation workflow for goal-feedback templates

```text
IF requested status = Active:
   search all active Performance Goal Feedback templates.
   IF another active template exists:
      show current active template details;
      warn that activating this template may inactivate the other templates;
      require explicit approval.
   activate the new template.
   re-query all Performance Goal Feedback templates.
   confirm only intended template remains active.
```

### 15.4 Update workflow

```text
IF active and in use:
   allow only name/description updates.
   block questionnaire changes.

IF changing attributes to share:
   classify as consequential because providers will see different goal context.
   validate with one-goal and multi-goal request.

IF replacing questionnaire:
   create new version when possible rather than changing current template.
   activate new version only after regression tests.

IF inactivating active goal-feedback template:
   warn that users can't request goal feedback unless another active goal-feedback template exists.
```

### 15.5 Validation scenarios

| Scenario | Expected result |
|---|---|
| No active Performance Goal Feedback template | Goal feedback request unavailable |
| One active Performance Goal Feedback template | Goal feedback request available if profiles/TDS/security also pass |
| Activate a second goal template in 26A+ Redwood | Other goal-feedback templates are set inactive or tenant prevents multiple active, depending release behavior |
| Goal feedback profile disabled | Request Feedback for goals hidden/unavailable |
| Goal drill-down disabled | Feedback section/action unavailable |
| TDS hides request feedback | Request Feedback action unavailable |
| Manager lacks goal update access | Manager can't request goal feedback for team member |
| Multiple goals selected | Questions repeated per goal and notifications validated |
| Private goal selected | Validate privacy and visibility behavior before rollout |
| Touchpoints goal feedback used | Active performance goal feedback template used automatically |

---

## 16. Cross-feature behavior

### 16.1 Feedback Center

Feedback Center lets users view requested feedback they have received, requested, or given depending on role/security. Completed feedback can be viewed or printed. Share settings determine whether manager/employee can see the feedback.

Best practices:

- Include Feedback Center in UAT even if the setup task is only Feedback Templates.
- Validate visibility separately for requester, feedback recipient, provider, manager, and HR specialist.
- Validate print behavior if feedback records are used for performance reviews or audit.
- Validate the behavior when a worker is terminated after feedback is requested.

### 16.2 Touchpoints

Touchpoints supports requesting general feedback and feedback on performance goals. Oracle documents that:

- For general feedback, one or more active general feedback templates can exist.
- For goal feedback, one active performance goal feedback template is required.
- General feedback allows template/questionnaire selection when more than one general template exists.
- For goal feedback, questions from the active/recent performance-goal feedback template are automatically included.
- Feedback requested on goals contributes to Average Team Interaction analytics.

Best practices:

- Test Touchpoints only after Feedback Templates are active.
- Test manager and employee flows separately.
- Validate whether feedback appears in Touchpoints timeline only when shared.
- Validate notification volume because providers receive separate notifications for each performance goal included.

### 16.3 Performance documents

Requested feedback can appear in performance documents depending on template setup and newer Redwood/AI summary settings. This is separate from Participant Feedback inside the performance-document process.

Best practices:

- Distinguish requested feedback from participant feedback in design documents.
- If requested feedback should be included in performance evaluations, validate performance template settings.
- If AI-generated feedback summaries are used in performance documents, validate the related performance template settings and Redwood profile prerequisites.
- Do not replace participant feedback setup with requested-feedback templates; the process-flow and performance-template dependencies are different.

### 16.4 Participant feedback distinction

Participant Feedback is configured through performance roles, questionnaire sections, process flows, and performance templates. Managers and workers can select participants and request feedback depending on process-flow options. The questionnaires used in participant feedback are associated with roles in the performance template.

Use this separation rule:

```text
If the feedback is inside a performance document and tied to participant roles/process flow,
route to Participant Feedback setup.

If the feedback is requested anytime through Feedback Center, Request Feedback, Touchpoints,
or goal details, route to Feedback Templates setup.
```

---

## 17. REST, HDL, HSDL, and migration guidance

### 17.1 Feedback Templates setup automation

Oracle documentation in scope for this guide describes Feedback Templates as an administrator setup page. It does not provide a clearly documented public write REST contract for creating Feedback Templates. Treat Feedback Template configuration as UI/FSM setup unless a tenant-specific, documented, supported API is confirmed.

Best practice:

```text
For Feedback Templates:
   Prefer UI-guided or UI-automated setup.
   Do not invent POST/PATCH endpoints.
   Do not use FeedbackRequest HDL to configure Feedback Templates.
```

### 17.2 Questionnaire REST support

Oracle REST documentation includes resources for:

- `questions` with GET/POST/PATCH/DELETE
- `questionnaires` with GET/POST/PATCH/DELETE
- `questionnaireParticipants` for General Surveys responses
- `questionnaireTemplates` GET/read operations
- questionnaire LOV resources

Use REST for questionnaire/question setup only when the subscriber and API support the intended use case. Still validate the questionnaire in the Feedback Template page before activation.

### 17.3 FeedbackRequest HDL/HSDL support

Oracle 24B What's New documents `FeedbackRequest` HDL/HSDL support for creating or updating feedback requests. Use it for runtime transaction loads, not template setup.

Implementation caution:

| Feedback request type | HDL code | Required consideration |
|---|---|---|
| General | `ORA_GENERAL` | Template and questionnaire setup must already support general feedback |
| Performance goal | `ORA_PERF_GOAL` | Include performance goal in `FeedbackRequestObject` and populate `RequestedForAssignmentId` |

### 17.4 Migration strategy

Recommended migration order:

```text
1. Profile options and security roles.
2. Lookups/value sets used by questionnaire or DFF dependencies.
3. Questions.
4. Questionnaire templates.
5. Questionnaires.
6. Feedback Templates as Inactive.
7. TDS/VBS page-property changes.
8. Alerts Composer templates.
9. Activation of General Feedback templates.
10. Activation of the single intended Performance Goal Feedback template.
11. Runtime smoke tests.
```

### 17.5 Environment comparison checklist

For each environment, compare:

| Area | Compare |
|---|---|
| Template setup | Name, description, type, status, questionnaire, in-use status |
| Questionnaires | Subscriber, version, status, sections, questions, required flags, additional-question behavior |
| Profiles | Redwood, request feedback, goals, drill-down, notification profiles |
| TDS | Page attributes for Request Feedback, Feedback action, goal feedback |
| VBS | Page properties, AI Assist visibility, custom extensions |
| Alerts | Enabled alerts/templates, recipients, reminder template |
| Security | Setup roles, runtime roles, REST privileges, data roles/security profiles |
| Translations | Template/questionnaire/questions/lookup meanings |
| Functional tests | Request, provider response, completion, sharing, print, notification |

---

## 18. Idempotency and configuration management

### 18.1 Idempotency key

No public external-id field is documented for Feedback Templates in the sources used for this guide. Use this composite key:

```text
Template Type + Exact Template Name
```

Recommended duplicate detection:

```text
1. Search exact template name.
2. Filter by template type.
3. If multiple rows are found, block and request cleanup.
4. Compare questionnaire and status.
5. Apply only safe updates.
```

### 18.2 Naming convention

Recommended enterprise naming standards:

| Template type | Pattern | Example |
|---|---|---|
| General Feedback | `General Feedback - <Purpose> - <Population> - v<N>` | `General Feedback - Project Closeout - Global - v1` |
| Performance Goal Feedback | `Performance Goal Feedback - <Population> - <Cycle/Year> - v<N>` | `Performance Goal Feedback - Global - FY27 - v1` |
| Questionnaire | `QNR - <Template Purpose> - <Population> - v<N>` | `QNR - Performance Goal Feedback - Global - v1` |
| Questionnaire Template | `QTMPL - <Purpose> - v<N>` | `QTMPL - Requested Feedback - v1` |
| Questions | `Q - <Domain> - <Short Text>` | `Q - Goal Feedback - Progress Observed` |

### 18.3 Versioning

Use new template/questionnaire versions when:

- Changing the questionnaire used by an active template.
- Changing question wording materially.
- Changing required questions.
- Changing additional-question capability.
- Changing performance-goal attributes shared in request.
- Changing from plain-text to rich-text for AI Assist.

Do not overwrite active production configurations without a change window and regression test evidence.

### 18.4 Lifecycle controls

| Action | Default control |
|---|---|
| Create | Allowed after dependency validation |
| Activate General Template | Allowed after runtime smoke test |
| Activate Performance Goal Template | Requires explicit approval because only one active goal-feedback template should be used |
| Inactivate | Allowed after impact warning |
| Change questionnaire | Blocked if in use; version instead |
| Delete | Blocked unless not in use and destructive action explicitly approved |
| Edit name/description | Allowed for active/in-use templates |

---

## 19. Common preflight checklist

Use this before any implementation change:

```text
[ ] Confirm target release and Redwood adoption state.
[ ] Confirm Workforce Development offering is enabled.
[ ] Confirm Performance Management is implemented or in implementation scope.
[ ] Confirm setup user has required setup privileges.
[ ] Confirm questionnaire setup route is accessible.
[ ] Confirm Feedback Templates page is accessible.
[ ] Confirm profile options needed for requested-feedback runtime behavior.
[ ] Confirm security roles/data security for employee, manager, HR, and provider personas.
[ ] Confirm TDS page attributes for request feedback and sharing options.
[ ] Confirm VBS page properties if Redwood customization is required.
[ ] Confirm Alerts Composer access and templates.
[ ] Confirm template naming/versioning standard.
[ ] Confirm migration and rollback plan.
```

---

## 20. Implementation outputs for FSCR

For each template, capture:

```yaml
feedback_template:
  template_type: general_feedback | performance_goal_feedback
  name: ""
  description: ""
  status: inactive | active
  questionnaire_name: ""
  questionnaire_subscriber: ""
  questionnaire_version: ""
  additional_questions_allowed: true | false | unknown
  attributes_to_share: []
  in_use: true | false | unknown
  created_by: ""
  migration_method: ui | ui_automation | manual | other

runtime_dependencies:
  redwood_request_feedback_enabled: true | false
  goals_feedback_enabled: true | false | not_applicable
  goal_drilldown_enabled: true | false | not_applicable
  tds_request_feedback_visible: true | false | unknown
  vbs_customizations: []
  notifications_enabled: []

security:
  setup_role: ""
  employee_test_user: ""
  manager_test_user: ""
  hr_test_user: ""
  provider_test_user: ""
  data_security_notes: ""

validation:
  setup_verified: true | false
  runtime_request_created: true | false
  response_submitted: true | false
  sharing_verified: true | false
  notifications_verified: true | false
  feedback_center_verified: true | false
  touchpoints_verified: true | false | not_applicable
  goals_verified: true | false | not_applicable
```

---

## 21. Test strategy

### 21.1 General Feedback test cases

| ID | Test | Expected result |
|---|---|---|
| GF-001 | Create inactive General Feedback template with valid questionnaire | Template saved and visible in list |
| GF-002 | Activate template | Template becomes available for general feedback requests |
| GF-003 | Create second active General Feedback template | User can choose questionnaire/template at runtime |
| GF-004 | Attempt request with no active General Feedback template | Request is blocked or no questionnaire selectable |
| GF-005 | Additional questions enabled | Additional Questions section is visible |
| GF-006 | Additional questions disabled | Additional Questions section is hidden/unavailable |
| GF-007 | Select Peers hidden by TDS | Button not visible |
| GF-008 | Select Peers exposed by TDS | Button visible and users can select peers |
| GF-009 | Select Direct Reports exposed for non-manager recipient | Button behavior aligns with Oracle rule; not useful if recipient has no direct reports |
| GF-010 | Share feedback with me hidden by TDS | Checkbox not visible |
| GF-011 | Request due date reminder | Reminder notification sent when alert template enabled |
| GF-012 | Completed feedback | Requester/recipient can view according to sharing/security |
| GF-013 | Print completed feedback | Print output includes expected responses/comments |
| GF-014 | Inactivate used template | No new requests use it; historical feedback remains |
| GF-015 | Delete in-use template | Blocked |

### 21.2 Performance Goal Feedback test cases

| ID | Test | Expected result |
|---|---|---|
| PGF-001 | Create inactive Performance Goal Feedback template | Template saved and visible |
| PGF-002 | Activate with no other active goal template | Template active |
| PGF-003 | Activate when another goal template active | Existing active template is inactivated or activation is blocked/warned according to tenant behavior |
| PGF-004 | Disable `ORA_HRG_REQUEST_FEEDBACK_ENABLED` | Goal Request Feedback action unavailable |
| PGF-005 | Disable goal drill-down | Goal feedback section/action unavailable |
| PGF-006 | Hide Request Feedback in TDS | Goal Request Feedback action unavailable |
| PGF-007 | Employee requests feedback for one goal | Request sent and provider sees goal context |
| PGF-008 | Employee requests feedback for multiple goals | Questions repeat for each goal |
| PGF-009 | Manager requests feedback for report's goal with update access | Request sent |
| PGF-010 | Manager lacks goal update access | Request unavailable or blocked |
| PGF-011 | Provider notification for multi-goal request | Notification count matches Oracle behavior |
| PGF-012 | Private goal feedback | Visibility and sharing match policy |
| PGF-013 | Touchpoints goal feedback | Active performance goal feedback template used automatically |
| PGF-014 | Change attributes to share | Provider sees new goal context only for new requests |
| PGF-015 | Inactivate only active goal template | Goal feedback requests unavailable until another active template exists |

### 21.3 Security test cases

| ID | Test | Expected result |
|---|---|---|
| SEC-001 | Setup configurator opens Feedback Templates | Create/edit actions visible |
| SEC-002 | HR analyst read-only user opens Feedback Templates | Page read-only |
| SEC-003 | User with both read-only and create/edit privileges | Create/edit privileges take precedence |
| SEC-004 | Employee can request feedback for self | Request succeeds if profiles/templates exist |
| SEC-005 | Manager can request feedback for direct report | Request succeeds within security profile |
| SEC-006 | HR specialist requests feedback for worker | Request succeeds within person/assignment security profile |
| SEC-007 | Provider receives request but lacks unrelated worker data | Provider can respond only to request context |
| SEC-008 | Integration user calls feedback-request REST | Allowed only with required REST privileges and data security |

### 21.4 Regression after quarterly update

Run these after every quarterly update or Redwood profile change:

```text
[ ] Feedback Templates page opens.
[ ] Create/Edit/Add buttons appear for configurators.
[ ] Read-only page is read-only for HR analyst role.
[ ] General Feedback request can be created.
[ ] Performance Goal Feedback request can be created.
[ ] TDS page attributes still apply.
[ ] VBS page properties still apply.
[ ] Notifications still fire.
[ ] Existing active goal-feedback template remains intended active template.
[ ] Feedback Center visibility is unchanged.
[ ] Touchpoints request-feedback flow is unchanged, if used.
```

---

## 22. Troubleshooting guide

### 22.1 User can't create a general feedback request

Check in this order:

```text
1. Is at least one active General Feedback template available?
2. Is the questionnaire active/selectable?
3. Does the user have Request Feedback privilege?
4. Does the user have person/assignment security access for the feedback recipient?
5. Is Redwood Request Feedback enabled if using Redwood page?
6. Are required TDS page attributes hidden?
7. Is the page being reached through an expected navigation route?
8. Are there errors in browser console or REST calls?
```

### 22.2 User can't request feedback for goals

Check in this order:

```text
1. Is there exactly one intended active Performance Goal Feedback template?
2. Is ORA_HRG_REQUEST_FEEDBACK_ENABLED = Yes?
3. Is goal drill-down mode enabled?
4. Is Request Feedback exposed by TDS on the goal page?
5. Is Goals Center Redwood profile state consistent with the page used?
6. Does the requester have view/update access to the goal?
7. Is the goal in a plan/status where feedback request is allowed?
8. Is the selected goal private, HR-assigned, completed, locked, or pending approval?
9. Does the questionnaire have valid questions and no setup errors?
```

### 22.3 Questionnaire not available in Feedback Template page

Check:

```text
1. Questionnaire subscriber/application context.
2. Questionnaire status and effective dates.
3. Questionnaire template status.
4. User setup privileges for questionnaires.
5. Folder/search filters.
6. Whether the questionnaire was created for participant feedback only.
7. Whether translations or required sections are incomplete.
```

### 22.4 Can't change questionnaire on a template

Expected when:

- The template is active and in use.
- The page indicates the template is used by existing feedback requests.

Best response:

```text
Create a new version of the questionnaire and template.
Activate the new template after testing.
Inactivate the old template.
Do not delete the old template unless it is not in use.
```

### 22.5 Notifications not sent

Check:

```text
1. Alerts Composer templates enabled.
2. HRA_FEEDBACK_REQUESTED alert and Requested feedback reminder template.
3. BIP/email/worklist notification profile options.
4. User email/worklist preferences.
5. Share settings; some notifications depend on feedback being shared.
6. Provider/requester/manager recipients.
7. ESS/background notification processing.
8. Environment email delivery restrictions in non-production.
```

### 22.6 Performance goal feedback template activation changed other templates

This aligns with the 26A Redwood behavior that lets administrators specify which goal-feedback template is active and sets other goal templates inactive.

Best response:

```text
1. Re-query all Performance Goal Feedback templates.
2. Confirm intended active template.
3. Document which templates were inactivated.
4. Re-run goal feedback runtime test.
5. Communicate the active-template change to administrators.
```

---

## 23. Consultant-answer patterns for FSCR/Codex

### 23.1 When asked “How do I set up a general feedback template?”

Codex should answer:

```text
Use My Client Groups > Performance > Setup Maintenance > Feedback Templates.
Before creating the template, create or verify the questionnaire, questionnaire template, questions, security, profiles, TDS, and notifications.
Create the Feedback Template with Template Type = General Feedback, attach the questionnaire, save inactive if staging, then activate after a runtime request-feedback test.
Multiple active general templates are allowed, but keep the list short.
```

### 23.2 When asked “How do I set up feedback for performance goals?”

Codex should answer:

```text
Create a Performance Goal Feedback template in Feedback Templates, but first verify goal-feedback dependencies:
- active questionnaire;
- ORA_HRG_REQUEST_FEEDBACK_ENABLED = Yes;
- goal drill-down mode enabled;
- Request Feedback exposed in TDS;
- goal requester has goal update access where required;
- Redwood Goals Center profiles if using Redwood.
Treat the active goal-feedback template as singular. In 26A+ Redwood behavior, activating one goal-feedback template sets others inactive.
```

### 23.3 When asked “Can we change the questionnaire?”

Codex should answer:

```text
Only if the template is not in use. If the template is active and in use, Oracle allows name and description edits but not questionnaire changes. Best practice is to create a new questionnaire/template version, activate it after testing, and inactivate the old template.
```

### 23.4 When asked “Can we load feedback templates through HDL?”

Codex should answer:

```text
Do not use FeedbackRequest HDL to configure Feedback Templates. FeedbackRequest HDL/HSDL creates or updates runtime feedback requests. General feedback uses ORA_GENERAL and performance goal feedback uses ORA_PERF_GOAL. Feedback Templates setup should be performed through the supported setup UI unless a tenant-specific supported API is confirmed.
```

### 23.5 When asked “What security is needed?”

Codex should answer:

```text
There are two layers: setup security and runtime security.
Setup needs Performance Management setup privileges, questionnaire setup privileges, profile-option access, and optionally Alerts Composer/TDS/VBS access. Runtime needs Request Feedback and View Requested Feedback privileges, person/assignment data security, and for integrations REST privileges such as Feedback Requests by Worker or Manager and Feedback Requests Read Only. For goal feedback, the requester also needs goal view/update access depending on role and scenario.
```

---

## 24. Do and don't checklist

### Do

- Do create questionnaires before Feedback Templates.
- Do test questionnaire preview before activation.
- Do use one active Performance Goal Feedback template unless the tenant has explicitly validated different behavior.
- Do keep goal-feedback questionnaires short because questions repeat for each selected goal.
- Do verify `ORA_HRG_REQUEST_FEEDBACK_ENABLED`, drill-down mode, and TDS for goal feedback.
- Do separate General Feedback from Participant Feedback and Anytime Feedback in design documents.
- Do use Alerts Composer to enable or disable requested-feedback notifications.
- Do version templates and questionnaires rather than editing active/in-use configurations.
- Do validate runtime flows with employee, manager, HR, and provider personas.
- Do record page route, UI mode, profile values, and security role used for each test.

### Don't

- Don't create custom template-type lookup values.
- Don't use FeedbackRequest HDL to configure setup templates.
- Don't hard-code questionnaire IDs across environments.
- Don't activate a new Performance Goal Feedback template without checking the current active one.
- Don't change questionnaire on an active/in-use Feedback Template.
- Don't delete templates unless they are not in use and deletion is approved.
- Don't assume Redwood behavior solely from release number; verify profile values and page behavior.
- Don't expose peer/direct-report selector buttons without business approval.
- Don't enable AI Assist without region, privacy, and Rich Text Box response-type checks.

---

## 25. Source Links

Oracle Help Center and What's New sources used for this guide:

1. Feedback Templates: https://docs.oracle.com/en/cloud/saas/talent-management/faupm/feedback-templates.html
2. Requested Feedback: https://docs.oracle.com/en/cloud/saas/talent-management/faupm/requested-feedback.html
3. Create a Feedback Request: https://docs.oracle.com/en/cloud/saas/talent-management/faupm/create-a-feedback-request.html
4. Request Feedback Using Touchpoints: https://docs.oracle.com/en/cloud/saas/human-resources/fauat/request-feedback-in-touchpoints.html
5. Request Feedback for Your Performance Goals: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/request-feedback-for-your-performance-goals.html
6. Request Feedback for Your Team Member's Performance Goals: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/request-feedback-for-your-team-member-s-performance-goals.html
7. How can I create a feedback template for performance goals?: https://docs.oracle.com/en/cloud/saas/talent-management/fagcq/how-can-i-create-a-feedback-template-for-performance-goals.html
8. Redwood: Control The Feedback Template Used for Requesting Feedback On An Employees Goals: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26a/tama-26a/26A-talent-mgmt-wn-f41981.htm
9. Redwood Experience for Feedback Spotlight for Worker: https://docs.oracle.com/en/cloud/saas/readiness/hcm/24a/tama-24a/24A-talent-mgmt-wn-f31181.htm
10. Redwood Experience for Request Feedback Enhancements: https://docs.oracle.com/en/cloud/saas/readiness/hcm/24a/rtama/24A-talent-mgmt-wn-f31182.htm
11. AI Assistance for Requested Feedback: https://docs.oracle.com/en/cloud/saas/readiness/hcm/24a/tama-24a/24A-talent-mgmt-wn-f31189.htm
12. Redwood: HR Read-Only Access to Feedback Templates Setup Page: https://docs.oracle.com/en/cloud/saas/readiness/hcm/25d/tama-25d/25D-talent-mgmt-wn-f40656.htm
13. Data Loader Support for Feedback Requests: https://docs.oracle.com/en/cloud/saas/readiness/hcm/24b/tama-24b/24B-talent-mgmt-wn-f32076.htm
14. Setup Tasks for Implementing Performance Management: https://docs.oracle.com/en/cloud/saas/talent-management/faipm/setup-tasks-for-implementing-performance-management.html
15. Overview of Implementing Performance Management: https://docs.oracle.com/en/cloud/saas/talent-management/faipm/overview-of-implementing-performance-management.html
16. Questionnaires: https://docs.oracle.com/en/cloud/saas/talent-management/faupm/questionnaires.html
17. How Performance Documents Work with Questionnaires: https://docs.oracle.com/en/cloud/saas/talent-management/faupm/how-performance-documents-work-with-questionnaires.html
18. Participant Feedback Task Options: https://docs.oracle.com/en/cloud/saas/talent-management/faupm/participant-feedback-task-options.html
19. Profile Options for Redwood Goals Center: https://docs.oracle.com/en/cloud/saas/talent-management/faigc/profile-options-for-redwood-goals-center.html
20. Performance Management Profile Options: https://docs.oracle.com/en/cloud/saas/talent-management/faipm/performance-management-profile-options.html
21. Descriptive Flexfields for Performance Management: https://docs.oracle.com/en/cloud/saas/talent-management/faipm/descriptive-flexfields-for-performance-management.html
22. Configure Notifications for Check-Ins and Requested Feedback: https://docs.oracle.com/en/cloud/saas/talent-management/faipm/configure-notifications-for-check-ins-and-requested-feedback.html
23. Configure Notifications for Requested Feedback Reminders: https://docs.oracle.com/en/cloud/saas/talent-management/25a/faipm/configure-notifications-for-requested-feedback-reminders.html
24. View or Print Requested Feedback: https://docs.oracle.com/en/cloud/saas/talent-management/faupm/view-or-print-requested-feedback.html
25. REST API for Oracle Fusion Cloud HCM - Questions: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-questions.html
26. REST API for Oracle Fusion Cloud HCM - Questionnaires: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-questionnaires.html
27. REST API for Oracle Fusion Cloud HCM - Questionnaire Templates: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-questionnaire-templates.html
28. REST API for Oracle Fusion Cloud HCM - Questionnaire Participants: https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-questionnaire-participant.html
29. Human Capital Management features using Redwood: https://docs.oracle.com/en/cloud/saas/readiness/redwood-adoption/raoac/rw-hcm.html
30. Employee role security reference: https://docs.oracle.com/en/cloud/saas/human-resources/oawpm/Employee_job_roles.html
31. Line Manager role security reference: https://docs.oracle.com/en/cloud/saas/human-resources/oawpm/Line_Manager_job_roles.html
32. Human Capital Management Integration Specialist role security reference: https://docs.oracle.com/en/cloud/saas/human-resources/oawpm/Human_Capital_Management_Integration_Specialist_job_roles.html

---

## 26. Quick reference: one-page implementation summary

```text
Feedback Templates are Performance Management setup objects.
Route: My Client Groups > Performance > Setup Maintenance > Feedback Templates.

General Feedback:
- One or more active templates are allowed.
- Runtime users can select a questionnaire when multiple templates exist.
- Requires at least one active template for general requested feedback.

Performance Goal Feedback:
- Treat as one active template.
- 26A Redwood behavior lets admins specify the active goal-feedback template and sets others inactive.
- Requires ORA_HRG_REQUEST_FEEDBACK_ENABLED = Yes.
- Requires goal drill-down and TDS Request Feedback visibility.
- Managers need goal update access to request feedback for team-member goals.

Questionnaires:
- Create questions -> questionnaire template -> questionnaire -> feedback template.
- Use the correct subscriber/application context.
- Allow additional questions only when intended.
- Use Rich Text Box if AI Assist is required.

Security:
- Setup: implementation/performance setup, questionnaire setup, profile, TDS/VBS, Alerts Composer.
- Runtime: Request Feedback, View Requested Feedback, data security, REST privileges if applicable.

Notifications:
- Configure in Alerts Composer.
- Use HRA_FEEDBACK_REQUESTED for requested-feedback reminders.

Lifecycle:
- Active and in-use: name/description can be changed; questionnaire can't.
- Inactive: unavailable for new requests.
- Not in use: questionnaire can be changed and template can be deleted.
- Prefer versioning and inactivation over destructive edits.
```
