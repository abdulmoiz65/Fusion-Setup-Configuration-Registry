# Oracle Fusion HCM Goal Management Implementation Best Practices

**Audience:** FSCR project contributors, Codex agents, Oracle HCM functional consultants, solution architects, and implementation reviewers.

**Scope:** Workforce Development implementation guidance for these four configuration objects and their dependent setup:

1. Review Periods
2. Performance Goal Plans, including regular and Primary Goal Plan behavior
3. Performance Library Goals
4. Development Library Goals

**Dependent setup covered:** Workforce Development offering setup, Career Development feature choices, Redwood routing, profile options, lookups, value sets, descriptive flexfields, security, approvals, notifications, Transaction Design Studio, Visual Builder Studio page rules, Profile Management target outcomes, HCM Data Loader, REST, diagnostics, migration, testing, and consultant-answering guardrails.

**Document status:** Best-practice reference, not a replacement for tenant-specific validation. Last source check: 2026-09-02.

**Baseline used:** The earlier `oracle_fusion_hcm_goal_management_fsm_setup.html` blueprint for Review Periods, Goal Plans, and Performance Library Goals, plus current Oracle implementation and readiness documentation listed in [Source references](#25-source-references).

---

## 1. How Codex must use this file

This file is designed to be used as a durable reference inside an FSCR project. When a consultant asks about Goal Management implementation, Codex should use this document to structure the answer, but it must not pretend to know tenant-specific configuration that was not provided.

### 1.1 Required consultant-answering pattern

For any Goal Management prompt, answer in this order:

1. **Classify the request** as Review Period, Goal Plan, Performance Library Goal, Development Library Goal, or dependent setup.
2. **State assumptions** such as tenant release, Redwood status, and whether the request is design-only, setup guidance, migration, or troubleshooting.
3. **Select the route**: Setup and Maintenance, My Client Groups > Goals, My Client Groups > Career Development, REST, HDL, or a mixed approach.
4. **List prerequisites**: profile options, feature choices, security, lookups, DFF, content sections, and dependent objects.
5. **Give implementation steps** in safe order: create inactive, validate, activate, then assign or expose.
6. **Give validation rules**: idempotency key, status, dates, document-type alignment, population, visibility, and copied-goal behavior.
7. **Call out risk controls**: no duplicate objects, no destructive deletes without proof of nonuse, no hard-coded IDs, no automatic assignment process submission.
8. **Return evidence expectations**: object name, external ID, Oracle ID, status, route used, process request ID when applicable, and post-save verification.

### 1.2 Codex must not do these things

- Do not say the FSM Goal Plans task is always valid. In current Oracle guidance it depends on Redwood Goals Center and the redesigned setup pages.
- Do not treat Performance Library Goals and Development Library Goals as the same setup object. They share reusable-goal concepts and REST/content-item patterns, but they are administered from different functional contexts and use different category semantics.
- Do not hard-code lookup codes, status codes, content item IDs, business unit IDs, department IDs, legal employer IDs, job family IDs, or REST hash keys. Resolve them in the target tenant.
- Do not create Goal Plans or Library Goals as active by default in implementation guidance. Use inactive staging unless the prompt explicitly asks for immediate activation and all validations are complete.
- Do not run Goal Plan assignment, mass assignment, or mass share merely because configuration was created.
- Do not call an assignment rerun a synchronization. Oracle behavior is additive for many Goal Plan scenarios.
- Do not recommend deleting Review Periods, assigned Goal Plans, or Library Goals unless nonuse is proven and the UI/API route supports deletion.
- Do not promise that changes to a Library Goal will update already copied worker goals. Copied library goals are independent copies.
- Do not invent Development Goal feature-profile codes when Oracle exposes those settings as Career Development feature choices.
- Do not store credentials, tokens, tenant URLs with secrets, or user-specific security data in the FSCR reference.

### 1.3 Minimum prompt details Codex should request or assume

When missing, Codex should either ask for these inputs or state conservative assumptions:

| Area | Needed detail |
|---|---|
| Tenant mode | Release/update, Redwood Goals Center enabled or not, VBS customizations in scope |
| Object | Review Period, Goal Plan, Performance Library Goal, Development Library Goal, or dependent setup |
| Operation | Design, create, update, activate, inactivate, delete, migrate, verify, troubleshoot |
| Idempotency | Review Period name, Goal Plan external ID, Library Goal external ID |
| Dates | Review Period dates, Goal Plan active dates, goal-setting dates, target completion dates |
| Population | Eligibility profiles, included workers, hierarchy scope, excluded workers |
| Integrations | Performance Document Type, Performance Template, Talent Review, Check-In, Profile Management, Learning |
| Governance | Naming standard, approval policy, deletion policy, change ticket, testing evidence |

---

## 2. Source-of-truth hierarchy

Use this hierarchy when Oracle documentation appears to conflict or when multiple UI generations exist.

1. **Target tenant behavior wins.** The tenant release, enabled profile options, opt-ins, feature choices, roles, and Redwood page customizations determine the actual setup path.
2. **Current Oracle readiness / What's New pages clarify new behavior.** For example, 26B introduces redesigned Goals configuration pages from Setup and Maintenance when Redwood Goals Center is enabled.
3. **Current implementation guides define stable setup rules.** Use them for profiles, lookups, Review Periods, Goal Plans, Library Goals, DFF, notifications, and diagnostics.
4. **REST and HDL docs define payload and migration contracts.** Use describe/metadata/LOV resources to resolve tenant-specific codes and IDs.
5. **The FSCR best-practice layer adds safety controls.** Examples: inactive staging, explicit assignment approval, idempotency, no destructive action without proof, and evidence capture.

### 2.1 Handling Redwood versus non-Redwood documentation conflict

Current Oracle docs contain both:

- A cumulative Goal Plans topic cautioning consultants to use **My Client Groups > Goals** and not the old FSM Goal Plans task.
- A 26B readiness topic stating that when **Redwood Goals Center** is enabled, the **Goal Plans**, **Goal Library**, and **Review Periods** tasks in **Setup and Maintenance** open redesigned Redwood configuration pages.

Best practice:

```text
IF ORA_HCM_VBCS_PWA_ENABLED = Y
AND ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED = Yes
AND the tenant opens the redesigned setup page from FSM
THEN use Setup and Maintenance for Goal Plans, Goal Library, and Review Periods.
ELSE use My Client Groups > Goals for Goal Plans and Performance Goal Library,
     and use Setup and Maintenance or the application admin page for Review Periods.
```

For Development Library Goals, use **My Client Groups > Career Development > Development Goal Library** unless the target tenant's redesigned Goal Library page explicitly supports the required Development Library Goal flow.

---

## 3. Core implementation principles

### 3.1 Design before configuration

Do not begin with field entry. Goal Management setup affects goal visibility, performance document integration, approval behavior, manager/worker access, mass processes, and downstream analytics. Always design these first:

- Business cycle and Review Period naming.
- Whether the customer uses regular Goal Plans, a Primary Goal Plan, or Goal Plan Sets.
- Performance Document Type and Performance Template alignment.
- Whether Performance Library Goals and Development Library Goals are global or restricted by workforce structures.
- Which roles can create, edit, cancel, delete, copy, share, align, and mass assign goals.
- Whether target outcomes update Enhanced Talent Profiles.
- Whether HDL/REST migration will be used.
- Evidence required for audit and cutover sign-off.

### 3.2 Use inactive staging

Best practice is to create these objects as **Inactive** first:

- Goal Plans
- Performance Library Goals
- Development Library Goals

Then validate fields, child records, visibility, integrations, and security before activation.

Review Periods can be created Active or Inactive depending on deployment sequence, but keep future-dated cycles inactive until associated Goal Plans, Performance Templates, and communications are ready.

### 3.3 Make every setup operation idempotent

| Object | Preferred idempotency key | Fallback |
|---|---|---|
| Review Period | Unique Review Period name | None; name must be unique |
| Goal Plan | `GoalPlanExternalId` | Exact name + dates + Review Period |
| Performance Library Goal | `GoalExternalId` + Type = Performance | Exact name + type |
| Development Library Goal | `GoalExternalId` + Type = Development | Exact name + type |

Best practice is to require an external ID for all Goal Plans and Library Goals even when the UI can generate one. This makes FSCR, REST, HDL, and migration behavior repeatable.

### 3.4 Resolve metadata in the tenant

Never assume that labels, lookup codes, or IDs are identical across pods. Resolve these values at runtime or during build validation:

- Review Period ID
- Business Unit ID
- Department ID
- Legal Employer ID
- Job Family ID
- Job ID
- Goal type code
- Active/inactive status code
- Performance category code
- Development category code
- Goal subtype code
- Priority code
- Level code
- Visibility/Available To code
- Goal access level code
- HR-assigned goal deletion/cancellation code
- Content section and content item identifiers for target outcomes

### 3.5 Separate configuration from assignment

Goal Plan creation and Goal Plan assignment are separate. A regular Goal Plan does not automatically assign itself to workers. Assignment requires the scheduled process for assigning goal plans. Keep this as an explicit change step with population evidence.

### 3.6 Preserve auditability

Every configuration action should produce an evidence record:

```yaml
object_type: goal_plan
operation: create
route_used: fsm_redwood | my_client_groups_goals | rest | hdl
release_assumption: 26B
redwood_profiles_verified: true
object_name: FY2027 Corporate Goal Plan
external_id: GP_FY27_CORP
oracle_id: 300000000000000
status_after_save: Inactive
created_or_updated_by: implementation_user
change_ticket: CHG-12345
validations:
  - review_period_active
  - document_type_date_envelope_valid
  - weighting_total_valid
  - eligibility_expression_valid
warnings: []
```

---

## 4. Recommended end-to-end setup sequence

Use this order for a new Goal Management implementation or a new annual cycle.

```text
1. Confirm Workforce Development offering and prerequisite HCM/Talent base setup.
2. Confirm tenant release and Redwood Goals Center profile options.
3. Confirm Career Development feature choices if Development Library Goals are in scope.
4. Configure security roles, data roles, and read-only/edit administration separation.
5. Configure lookups and value sets.
6. Configure descriptive flexfields and deploy them.
7. Configure profile options and feature choices.
8. Configure target-outcome prerequisites in Profile Management.
9. Configure notifications, approvals, TDS, VBS page rules, and guided journeys.
10. Create or verify Review Periods.
11. Create Performance Library Goals as inactive.
12. Create Development Library Goals as inactive.
13. Validate library-goal visibility, restrictions, tasks, measurements, outcomes, and translations.
14. Activate approved Library Goals.
15. Create regular Goal Plans as inactive or configure Primary Goal Plan deliberately.
16. Associate Review Period and Performance Document Types.
17. Add plan goals or library goals.
18. Configure eligibility profiles, included workers, and excluded workers.
19. Validate weights, goal counts, access settings, and document integration.
20. Activate Goal Plans.
21. Submit assignment processes only after explicit approval.
22. Monitor scheduled process results.
23. Verify worker goal plans, copied goals, performance document population, and security visibility.
24. Run diagnostics and capture implementation evidence.
```

---

## 5. Navigation and route-selection best practices

### 5.1 Redwood setup-page route

When Redwood Goals Center is enabled, the following Setup and Maintenance tasks open redesigned Redwood setup pages:

- Goal Plans
- Goal Library
- Review Periods

Required profile values:

| Profile option | Required value |
|---|---|
| `ORA_HCM_VBCS_PWA_ENABLED` | `Y` |
| `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` | `Yes` |

The second profile controls Redwood Performance Documents, Check-Ins, and Goals Center together; they cannot be enabled independently.

### 5.2 Non-Redwood or fallback route

| Object | Preferred route when Redwood FSM page is unavailable |
|---|---|
| Review Periods | Setup and Maintenance > Workforce Development > Define Worker Goal Setting > Review Periods, or My Client Groups > Goals/Performance > Review Periods |
| Goal Plans | My Client Groups > Goals > Goal Plans |
| Performance Library Goals | My Client Groups > Goals > Performance Goal Library |
| Development Library Goals | My Client Groups > Career Development > Development Goal Library |
| Performance goal scheduled processes | My Client Groups > Goals > Scheduled Processes for Performance Goals, or Tools > Scheduled Processes |
| Development goal scheduled processes | My Client Groups > Career Development > Scheduled Processes for Development Goals, or Tools > Scheduled Processes |

### 5.3 Scheduled process page route

In 26B, Oracle redesigned scheduled process pages for:

- Scheduled Processes for Performance Goals
- Scheduled Processes for Development Goals
- Scheduled Processes for Goals

The redesigned pages do not support advanced schedule process options yet. If advanced options are needed, use the standard Scheduled Processes work area.

To view the combined scheduled-process page, set:

```text
ORA_HRG_ENABLE_GOAL_ADMIN_PAGES_CONSOLIDATION = Yes
```

### 5.4 Route verification

Codex should instruct consultants to verify the actual page, not just the navigation label. Evidence should include:

- Page title
- Object type selected
- Visible fields or actions
- Redwood or non-Redwood experience
- Whether actions such as Add, Edit, Delete, Activate, Inactivate, and Schedule are enabled

---

## 6. Offering, opt-in, and functional-area setup

### 6.1 Workforce Development

Goal Management is part of the **Workforce Development** offering. Oracle identifies **Define Worker Goal Setting** as the task area for worker-goal setup objects such as lookups, value sets, descriptive flexfields, profile option values, notification settings, Goal Library, Review Periods, and Goal Plans.

Best practices:

- Confirm the implementation user has access to Workforce Development.
- Confirm HCM Base or Talent Management Base prerequisites are complete.
- Keep setup in a controlled implementation sandbox before production.
- Do not mix annual-cycle setup with structural redesign unless approved.
- Maintain a configuration register for profiles, lookups, DFF, TDS, VBS, and approvals.

### 6.2 Career Development feature choices

Development Library Goals are controlled by Career Development features under the Workforce Development offering. Review feature choices before configuring Development Library Goals:

| Career Development feature choice | Best-practice use |
|---|---|
| Career Development Notifications | Enable when development-goal notifications are part of the process design |
| Completed Goal Edit Option | Define whether completed development goals can be edited |
| Goal Library | Must be enabled to use Development Goal Library |
| Restrict Library Goal | Enable only when library-goal visibility must follow workforce structures |
| Development Goal Tasks | Enable only when task tracking is required |
| Target Outcomes | Enable only with Enhanced Talent Profile readiness and content-section governance |
| Development Intents | Enable when development goals must connect to current/future role intent |
| Development Goals Sharing | Enable when sharing is required and privacy controls are understood |
| Development Goal Drill Down Page | Required for detail sections such as tasks, measurements, and target outcomes |
| Development Goal Measurement | Set according to whether measurements are disabled, single, or multiple |
| Cancel Development Goals Assigned by HR | Enable only if worker/manager cancellation of HR-assigned goals is permitted |
| Delete Development Goals Assigned by HR | Enable only if deletion of HR-assigned development goals is permitted |
| Development Goal Learning | Enable only when Learning integration is designed |

Do not map these feature choices to invented profile option codes unless the target tenant or Oracle documentation explicitly exposes them.

---

## 7. Security best practices

### 7.1 Implementation access

Oracle states that implementing Goal Management requires application implementation consultant privileges. The HCM Application Administrator role has broad Workforce Development setup access and includes goal-related privileges such as managing performance goal setup and library goals.

Best practices:

- Use broad implementation roles only during build and controlled testing.
- For production operations, create least-privilege custom roles.
- Separate setup administration from HR operational administration.
- Separate read-only HR specialist access from edit-capable HR specialist access.
- Test with at least four personas: implementer, HR specialist, line manager, employee.

### 7.2 Edit versus read-only administration

For Redwood Goals Center, Oracle supports read-only administrative access for HR specialists. The recommended pattern is:

- Copy the delivered HR specialist role.
- Remove edit aggregate privileges such as:
  - `ORA_HRG_MANAGE_PERFORMANCE_GOAL_BY_HR`
  - `ORA_HRG_MANAGE_DEVELOPMENT_GOAL_BY_HR`
- Add view aggregate privileges such as:
  - `ORA_HRG_VIEW_PERFORMANCE_GOAL_BY_HR`
  - `ORA_HRG_VIEW_DEVELOPMENT_GOAL_BY_HR`
- Grant the custom role to HR specialists who should view but not modify goal objects.

### 7.3 Privilege areas to validate

| Capability | Security to validate |
|---|---|
| Configure Goal Management setup | Application Implementation Consultant or HCM Application Administrator style setup privileges |
| Manage Performance Goal setup | Manage Performance Goal Setup |
| Manage Performance Library Goals | Manage Performance Goal in Goal Library |
| Manage Development Library Goals | Manage Development Goal in Goal Library |
| Manage worker performance goals by HR | Manage Performance Goal by HR |
| Manage worker development goals by HR | Manage Development Goal by HR |
| View-only goal administration | View Performance Goal by HR, View Development Goal by HR |
| Configure TDS LOV/search fields | `HRC_ACCESS_HCM_TRANSACTION_CONFIGURATOR_PRIV` |
| Submit goal scheduled processes | Process-submission privileges and goal batch process privileges |
| Use REST LOVs | REST LOV privileges for Review Periods, Performance Goals, Library Goals, Worker Assignments, and Workforce Structures as needed |
| Target outcomes | Profile Content Section Access and Talent Profile data access |

### 7.4 Data-security checks

Goal setup often saves successfully but appears wrong because of data security. Validate:

- Person security profile for HR specialists.
- Assignment security profile for workers included in a goal plan.
- Manager hierarchy data for line managers.
- Business unit, department, legal employer, job, and job family security.
- Talent Profile content-section access for target outcomes.
- Whether HR specialists are using administrator pages where some restrictions do not apply.

---

## 8. Profile options and feature controls

### 8.1 Redwood and administration profiles

| Profile option | Recommended value or use |
|---|---|
| `ORA_HCM_VBCS_PWA_ENABLED` | `Y` for Redwood pages |
| `ORA_HRA_PERFORMANCE_DOCUMENTS_AND_GOALS_REDWOOD_ENABLED` | `Yes` to enable Redwood Performance Documents, Check-Ins, and Goals Center together |
| `ORA_HRG_ENABLE_GOAL_ADMIN_PAGES_CONSOLIDATION` | `Yes` only if the combined Scheduled Processes for Goals page is desired |
| `ORA_PER_NUDGE_CONFIGURATION_REDWOOD_ENABLED` | `Y` when using Redwood nudge configuration for goal-setting deadline reminders |

### 8.2 Current Goal Management profiles

| Profile option | Best-practice guidance |
|---|---|
| `HRG_USE_GOAL_MANAGEMENT` | Confirm its effective value when Goal Management availability is in scope; do not change it without an approved feature decision |
| `HRG_ALLOW_DECIMALS_IN_WEIGHTS` | Confirm before allowing decimal goal weights |
| `HRG_COMPLETED_GOAL_EDIT_OPTIONS` | Decide early; affects completed-goal lifecycle governance |
| `ORA_HRG_DEFAULT_GOAL_SORT_OPTION` | Align with performance document expectations when synchronization is enabled |
| `HRG_LOV_SEARCH_SHAREDGOALS_STARTSWITH` | Validate only when shared-goal search behavior is in scope |
| `ORA_HRG_GOALS_SEARCH_BY_PERSON` | Validate only when administrator person-search behavior is in scope |
| `ORA_HRG_REQUEST_FEEDBACK_ENABLED` | Validate only when goal feedback is in scope |

### 8.3 Current Career Development dependencies

These profiles are managed as Career Development configuration. Validate them only when the corresponding development-goal capability is in scope; they are not prerequisites for all Goal Management implementations.

| Profile option | Conditional use |
|---|---|
| `ORA_HRD_COMPLETED_GOAL_EDIT_OPTIONS` | Completed development-goal edit behavior |
| `ORA_HRD_DELETE_HR_ASSIGNED_GOALS` | Deletion behavior for HR-assigned development goals |
| `ORA_HRD_INACTIVATE_HR_ASSIGNED_GOALS` | Inactivation behavior for HR-assigned development goals |
| `ORA_HRD_CAREER_AMBASSADORS_ENABLED` | Career Ambassadors capability |

### 8.4 Profiles not required for Redwood configuration

Do not configure the following profiles as Redwood prerequisites. Validate the current Redwood/VBS behavior and tenant metadata instead. Use them only for an explicitly requested classic or RUI compatibility assessment where the current tenant confirms the profile is still consumed.

| Profile option | Legacy purpose |
|---|---|
| `HRG_ADD_GOAL_REQ_APPR` | Classic approval request for adding goals |
| `HRG_CANCEL_GOAL_REQ_APPR` | Classic approval request for cancelling goals |
| `HRG_DELETE_GOAL_REQ_APPR` | Classic approval request for deleting goals |
| `HRG_KEY_ATTR_CHG_REQ_APPR` | Classic approval request for changing key goal attributes |
| `HRG_GOAL_COMPLN_REQ_APPR` | Classic approval request for completing goals |
| `HRG_ENABLE_MATRIX_MGMT` | Classic matrix-management behavior |
| `HRG_ENABLE_MULTIPLE_MEASUREMENT` | Classic multiple-measurement behavior |
| `HRG_USE_GOAL_PLAN_SET` | Classic Goal Plan Set behavior |
| `HRG_USE_GROUP_SPACE` | Classic group-space behavior |
| `ORA_HRG_PREFIX_GOAL_COPY_OTHER_GOAL_PLANS` | Obsolete and not consumed |
| `HRG_ENABLE_GOAL_DRILLDOWN_VIEW` | RUI drill-down behavior |
| `HRG_GOALS_RESPONSIVE_ENABLED` | RUI responsive goal pages |
| `HRG_USE_MEASUREMENTS` | RUI measurement behavior |
| `ORA_HRG_ENABLE_INLINE_WEIGHT_UPDATE` | RUI inline weight update |
| `HRG_ENABLE_OUTCOMES` | RUI target-outcome behavior |
| `HRG_ENABLE_TASK` | RUI task behavior |
| `HRD_CAREER_DEVELOPMENT_RESPONSIVE_ENABLED` | RUI Career Development pages |
| `ORA_HRD_AI_CAREER_AMBASSADORS` | Obsolete in 24A |
| `ORA_HRD_VBCS_ENABLED` | Obsolete in 24A |

For Redwood Goals Center, Goal Library, goal alignment, grant access, organization goals, and library-goal restrictions are available by default or are controlled by current Redwood page configuration.

### 8.5 Goal assignment performance profiles

| Profile option | Default / valid values | Best-practice use |
|---|---|---|
| `HRG_ONLINE_PROCESS_THRESHOLD` | Default 25 | Estimate records as goals x assignees; above threshold goes to scheduled process queue |
| `HRG_GP_MAX_THREADS` | Default 4; valid multithread 2-8; 0/1 single thread | Tune only after volume testing |
| `HRG_GP_MINCOUNT_EACHTHREAD` | Default 5000 | Tune with batch-volume evidence |
| `HRG_GP_MINCOUNT_LASTTHREAD` | Default 1000 | Tune with batch-volume evidence |
| `HRG_MASS_REQ_OPTIMIZATION_LEVEL` | Default 1; valid 0-3 | Increase only after diagnostics confirm logging/result overhead |

### 8.6 Review Period profile

| Profile option | Best-practice guidance |
|---|---|
| `ORA_HRT_DISPLAY_INACTIVE_REVIEW_PERIODS` | Set to `No` to hide inactive Review Periods from employee and manager responsive pages; HR specialists still see inactive periods |

---

## 9. Lookups and value-set best practices

Oracle supports Goal Management and Career Development lookups through **Worker Goal Setting Lookups** and **Manage Common Lookups**. Use `HRG` in the lookup type search field to find goal-related common lookups.

### 9.1 Lookup governance

- Update only lookup types with a User or Extensible configuration level.
- Do not modify System lookup meanings to force business terminology.
- Use effective dates and enabled flags deliberately.
- Keep lookup codes stable across environments.
- Migrate lookup changes before migrating objects that reference them.
- Maintain a lookup design table with code, meaning, description, enabled status, start date, end date, owner, and usage.

### 9.2 High-impact lookup types

| Lookup type | Used by | Best-practice note |
|---|---|---|
| `HRG_PERF_GOAL_CATEGORY` | Performance goals | Define categories before creating Performance Library Goals |
| `HRG_DEV_GOAL_CATEGORY` | Development goals | Define categories before creating Development Library Goals |
| `HRG_PRIORITY` | Performance and development goals | Keep meanings simple and consistent |
| `HRG_GOAL_TASK_TYPE` | Goal tasks | Define task types only if tasks are enabled |
| `HRG_GOAL_MEASUREMENT_LEVEL` | Goal measurements | Use if measurement levels are part of the design |
| `HRG_GOAL_QUANTITATIVE_UOM` | Goal measurements | Add UOM values cautiously; test display and reporting |
| `HRG_GOAL_QUANT_MEASURE_TYPE` | Goal measurements | System lookup for maximum/minimum behavior |
| `HRG_GOAL_ACCESS_LEVELS` | Library/plan goal access | Validate labels; do not hard-code codes |
| `HRG_GOAL_SOURCE` | Goal source | Usually not a consultant customization target unless integration requires it |
| `HRG_GOAL_STATUS` | Goal lifecycle | System-controlled; don't repurpose |
| `HRG_PROCESS_TYPE` | Scheduled process types | System-controlled |
| `HRG_COMPL_GOAL_EDIT_OPTIONS` | Completed-goal edit profile | Validate with profile setting |

### 9.3 Lookup migration sequence

```text
1. Configure lookup codes and meanings in source.
2. Export or document lookup setup.
3. Import/configure lookups in target.
4. Validate lookup codes exist and are enabled.
5. Only then migrate Library Goals, Goal Plans, and HDL files that reference the codes.
```

---

## 10. Descriptive flexfields and value sets

### 10.1 Delivered DFFs

Oracle documents these default descriptive flexfields for goals:

| DFF | Applies to | Best-practice use |
|---|---|---|
| `HRG_GOALS` | Worker goals and alignment details | Add attributes needed at goal level, such as strategic theme, project type, compliance indicator |
| `HRG_GOAL_PLANS_B` | Goal plan details | Add attributes needed at plan level, such as cycle owner, plan segment, rollout wave |

### 10.2 DFF design rules

- Use value sets for controlled values.
- Keep segment names business-friendly and reporting-friendly.
- Avoid sensitive personal data in goal DFFs.
- Decide whether fields are informational, required, or reporting-only.
- Align DFF visibility with TDS/VBS and page behavior.
- Deploy changed flexfields before testing pages, REST, HDL, or reporting.
- Include DFFs in migration and regression testing.

### 10.3 Value-set design rules

- Use independent value sets for stable business classifications.
- Avoid table-validated value sets unless the reference object is stable and accessible to the relevant users.
- Keep codes stable across environments.
- Validate value-set security and translations.

---

## 11. Target outcomes and Profile Management

Target outcomes connect goal completion to Talent Profile content such as competencies, skills, certifications, education, languages, memberships, and other eligible profile content.

### 11.1 Required prerequisites for performance goal target outcomes

For Performance Library Goals and performance goals, validate:

- Enhanced Talent Profiles are implemented.
- Profile content sections are configured for goal usage.
- Profile Content Section Access is granted to the relevant roles.
- Current Redwood/VBS page configuration exposes the target-outcome experience.
- For explicitly requested classic or RUI compatibility testing, the tenant still consumes the relevant legacy profile from section 8.4.

### 11.2 Required prerequisites for development goal target outcomes

For Development Library Goals, validate:

- Enhanced Talent Profiles are implemented.
- Content-section access is granted.
- Current Redwood/VBS page configuration exposes the development target-outcome experience.
- The applicable Career Development dependency from section 8.3 is validated when its related behavior is in scope.
- For explicitly requested classic or RUI compatibility testing, the tenant still consumes the relevant legacy profile or feature choice.

### 11.3 Best-practice content governance

- Do not enable target outcomes before the Profile Management content model is stable.
- Confirm that content sections use the correct goal subscriber configuration.
- Confirm whether completion of a goal should update the employee profile automatically or only support review.
- Test with employee and manager roles, not just HR administrator roles.
- If target outcomes don't appear, troubleshoot in this order:
  1. Feature/profile enabled
  2. Drill-down page enabled
  3. Enhanced Talent Profiles enabled
  4. Content section eligible for goals
  5. Content section access granted
  6. Redwood/VBS page visibility not hiding the section

---

## 12. Notifications, nudges, and approvals

### 12.1 Goal Management notifications

Use **Goal Management Notification Settings** to configure performance-goal notifications. Before enabling notifications, validate BI Publisher notification profiles, including the HCM and Talent Management email/worklist notification profiles documented by Oracle.

Best practices:

- Enable only notifications that are part of the communications design.
- Test with real recipient roles in a nonproduction pod.
- Document which events notify workers, managers, HR specialists, and requesters.
- Avoid enabling notifications before mass-assignment testing unless test email routing is controlled.

### 12.2 Redwood goal-setting deadline nudges

26B introduces a Redwood nudge option to remind employees and managers when goal plans have no goals before the goal-setting end date.

Best practices:

- Use nudges only after Goal Plan goal-setting dates are consistently populated.
- Enable `ORA_PER_NUDGE_CONFIGURATION_REDWOOD_ENABLED = Y` for Redwood nudge setup pages.
- Enable Redwood Goals Center profiles.
- Configure the Goal module and the reason for missing goals before the deadline.
- Test the nudge timing with a short test cycle before production rollout.

### 12.3 Approval rules and task expiration

Dependent setup includes:

- **Manage Approval Transactions for Human Capital Management** for approval rules and bypass approval.
- **Manage Task Configurations for Human Capital Management** for expiration policies.
- Transaction Console for review and operational troubleshooting.

Best practices:

- Decide which goal actions require approval before configuring Goal Plans.
- Test approval behavior for employee, manager, and HR-originated changes.
- Decide what happens when managers request more information after goal-setting end date restrictions apply.
- Document bypass approvals by subprocess, not as an informal exception.

---

## 13. Transaction Design Studio and Visual Builder Studio

### 13.1 Transaction Design Studio for Goal Management

Oracle documents these TDS actions for Goal Management:

- **Performance Goal Details**
- **Performance Goal Library**

TDS configurations for Goal Management apply when the Drill Down to Goal Details profile is enabled. If drill-down is disabled, older personalization approaches may apply.

Best practices:

- Use TDS for field visibility and requiredness, not for security enforcement alone.
- Validate role, legal employer, business unit, and page-context rules.
- Keep TDS rules minimal and named clearly.
- Avoid hiding fields that are required by integration, reporting, or HDL.
- Test both Add and Edit flows.

### 13.2 Performance Goal Library LOV/search configuration

For performance library-goal search, TDS can configure search/display fields such as:

- Goal name
- Goal category
- Goal subtype
- Business unit
- Department
- Job family
- Legal employer

Defaults include Goal name, Goal category, and Goal subtype. Best practice is to expose workforce-structure fields when library-goal restriction is in use.

### 13.3 Development Goal Library LOV/search configuration

For development library-goal search, TDS can configure search/display fields such as:

- Goal name
- Goal category
- Business unit
- Department
- Job family
- Legal employer

Defaults include Goal name and Goal category. Best practice is to expose workforce-structure fields when the Career Development Restrict Library Goal feature is enabled.

### 13.4 Visual Builder Studio rules and page properties

26B adds several VBS-based Redwood controls for goal pages. Treat these as UI behavior controls layered on top of security and profile options.

Examples:

| Area | VBS best-practice consideration |
|---|---|
| Goal actions by role | Hide actions only after confirming privileges; if privilege is absent, UI visibility cannot grant the action |
| Sharing with any person | Hide the any-person option when sharing must be restricted to accessible users |
| Request information in approvals | Disable reroute-like request-info options if approval governance requires manager-only handling |
| Task add buttons | Hide task add action when tasks should not be used, even if profile/feature permits tasks |
| Task measurements | Hide measurable-task switch when only simple tasks are desired |
| Dotted-line reports | Hide dotted-line reports if managers should manage direct reports only |
| Already-added goals on Explore/suggestions | Hide already-added shared, development, or organization goals to reduce duplicate selection |
| Negative measurements | Enable only when negative measurement values are part of the goal-measurement design |

---

## 14. Object 1: Review Periods

### 14.1 Purpose

Review Periods are business periods used to organize Talent Management processes into time-bound cycles. They tie together Goal Plans, Goal Plan Sets, Performance Document periods, and Check-In template behavior.

### 14.2 Navigation

```text
Setup and Maintenance > Workforce Development > Define Worker Goal Setting > Review Periods
```

Alternate administration routes:

```text
My Client Groups > Goals > Review Periods
My Client Groups > Performance > Review Periods
```

### 14.3 Required fields

| Field | Best-practice rule |
|---|---|
| Review Period Name | Required; unique; use a stable naming convention |
| Description | Recommended; include business cycle and usage |
| Status | Active or Inactive |
| Period Start Date | Required; must be on/before end date |
| Period End Date | Required; must be on/after start date |

### 14.4 Naming convention

Recommended examples:

| Scenario | Name | Description |
|---|---|---|
| Fiscal year | `FY2027` | Fiscal Year 2027 talent cycle |
| Calendar year | `CY2027` | Calendar Year 2027 performance and goals cycle |
| Semiannual | `FY2027-H1` | Fiscal Year 2027 first half cycle |
| Quarterly | `FY2027-Q1` | Fiscal Year 2027 Q1 goals cycle |

Avoid names such as `Current Year`, `Annual Review`, or `2027 New` because they are not stable across cycles.

### 14.5 Lifecycle rules

- You can create Review Periods whenever needed.
- Each Review Period must have a unique name.
- If a Review Period is in use, its start and end dates cannot be modified.
- The status can be changed to active or inactive at any time.
- Existing business objects continue to use a Review Period after it is made inactive.
- Inactive Review Periods are not selectable for new Goal Plans, Goal Plan Sets, or Performance Documents by HR specialists.
- Review Periods that are not in use can be deleted if the route supports deletion.
- Employee and manager pages can hide inactive periods when `ORA_HRT_DISPLAY_INACTIVE_REVIEW_PERIODS = No`; HR specialists still see them.

### 14.6 Best-practice create/update flow

```text
1. Search by exact Review Period name.
2. If found, compare dates, status, and description.
3. If not found, validate date order and create.
4. If date change is requested, check usage first.
5. If used, block date changes and propose a replacement Review Period.
6. Use inactive status to retire old periods rather than deleting them.
7. Verify visibility from the relevant worker, manager, HR, and performance pages.
```

### 14.7 Integration checks

A Review Period must align with Performance Management setup:

- Performance document start and end dates must be within the Review Period dates.
- Goal Plans associated with a Review Period and Performance Document Type determine which goals appear in performance documents.
- Check-In templates may be associated with all Review Periods or specific Review Periods.

### 14.8 Common consultant guidance

If asked to change a Review Period's dates after use, answer:

> Do not change dates on a Review Period already used by Goal Plans, Goal Plan Sets, or Performance Documents. Create a new Review Period, update future configuration to use it, and inactivate the old period after impact analysis.

---

## 15. Object 2: Goal Plans

### 15.1 Purpose

Goal Plans are collections of performance goals grouped by common characteristics such as time frame, population, department, or business cycle. Regular Goal Plans must be assigned to workers before goals can be added or assigned within the plan duration. Primary Goal Plan is a special common plan available across Review Periods.

### 15.2 Navigation

Redwood-enabled tenant:

```text
Setup and Maintenance > Workforce Development > Define Worker Goal Setting > Goal Plans
```

Fallback / non-Redwood:

```text
My Client Groups > Goals > Goal Plans
```

### 15.3 Regular versus Primary Goal Plan

| Capability | Regular Goal Plan | Primary Goal Plan |
|---|---|---|
| Review Period | Required | Common across all Review Periods |
| Worker assignment | Required through scheduled process | Not required |
| Active count | Multiple can exist | Only one active Primary Goal Plan |
| Goal Plan Sets | Can be used with sets | Primary Plan unavailable when Goal Plan Sets are enabled |
| Eligibility profiles | Supported | Not supported |
| Add goals while creating/editing plan | Supported | Not supported |
| Goal-setting period | Supported in Redwood | Not available |
| Use case | Annual/cycle plan by population | Common global plan for ad hoc and integrated goal usage |

### 15.4 Core fields

| Field | Best-practice rule |
|---|---|
| External ID | Required by FSCR; use for idempotency |
| Goal Plan Name | Required; business-friendly |
| Description | Recommended |
| Status | Create Inactive first |
| Type | Usually worker/performance plan; resolve in tenant |
| Review Period | Required for regular plans; must be active for new setup |
| Start and End Dates | For a regular plan, default both omitted dates from the selected active Review Period. A complete explicit pair overrides the default and must fit the Review Period; reject a partial pair. Align dates with performance document type dates. |
| Goal-setting start/end | Redwood behavior; employee restrictions only |
| Weighting enabled | Use only when ratings/calculation require relative weights |
| Enforce weight sum 100 | Use only when governance can enforce clean weights |
| Maximum/minimum goals | Use sparingly; define exceptions such as private goals |
| Access/update by roles | Align with HR/manager/worker responsibility model |
| HR-assigned goal action | Define cancel/delete/update behavior explicitly |
| Performance Document Types | Required if goals should populate performance documents |
| Eligibility profiles | Use for population filtering |
| Included/excluded workers | Use to define assignment population |

### 15.5 External ID naming convention

Goal Plan external ID supports a larger length than Library Goal external ID. Recommended patterns:

```text
GP_FY27_GLOBAL_PERF
GP_FY27_SALES_PERF
GP_CY27_US_CORP_PERF
```

Do not encode transient names such as implementation-wave owner unless required. Keep external IDs stable between test and production.

### 15.6 Goal-setting dates and restrictions

25D added goal-setting dates and restrictions for Redwood Goal Plans.

Best-practice interpretation:

- Use goal-setting dates to communicate the employee goal-entry window.
- The start date is informational and not enforced.
- Restrictions after end date apply to employees, not managers or HR specialists.
- Employees can still extend goals and submit a plan for approval after the goal-setting end date.
- Employees can still update progress information and progress notes even if regular editing is restricted.
- The feature is not available for Primary Goal Plans.
- If the Goal Plan or mass assignment doesn't allow workers to update goals, the goal-setting edit restriction is ignored.

### 15.6.1 Adding a Performance Library Goal to a Goal Plan

When an administrator selects an active Performance Library Goal for an existing
regular Goal Plan, use the current source identity as the copy reference and
create a Goal Plan goal. Default both omitted copied-goal dates from the Goal
Plan Start Date and End Date. A complete explicit pair overrides those defaults
and must remain inside the Goal Plan range; reject a partial pair. The new plan
goal is an independent copy: later Library Goal edits do not alter it.

### 15.7 Weighting best practices

- Enable weights only if the performance process uses weights.
- If enforcing 100%, validate plan goals before activation and assignment.
- Confirm `HRG_ALLOW_DECIMALS_IN_WEIGHTS` before designing decimal weights.
- Ensure performance document templates and goal sections support the intended weight behavior.
- Avoid allowing managers to create unbalanced weights when the performance process requires strict 100% totals.

### 15.8 Goal-count limits

- Blank maximum means unlimited goals.
- Organization goals are not counted against maximum-goal restrictions.
- Enforcing the maximum prevents managers and HR specialists from adding beyond the maximum.
- Private goal exceptions must be deliberate and documented.

### 15.9 Performance Document Type association

You can associate a Performance Document Type only when:

```text
Performance Document Type From Date <= Goal Plan Start Date
Performance Document Type To Date   >= Goal Plan End Date
Performance Document Type Status    = Active
```

Best practices:

- Validate document type dates before saving.
- Validate Performance Template document periods use the same Review Period.
- Confirm the Performance Goals section is configured to populate worker performance goals.
- Test Update Goals action behavior in performance documents.
- Remember that goal ratings and evaluation comments from performance documents do not become Goal Management ratings/comments in the same way.

### 15.10 Eligibility profile rules

Eligibility profiles on Goal Plans behave as follows:

| Configuration | Worker must satisfy |
|---|---|
| All selected profiles required | All selected profiles |
| No selected profile required | At least one selected profile |
| Mixed required and optional | All required profiles and at least one optional profile |
| One required profile | That profile |

Best practices:

- Use eligibility profiles for assignment population, not as a substitute for security.
- Document the Boolean expression for each Goal Plan.
- If Goal Plan Sets are enabled, remember that Goal Plan Set eligibility supersedes Goal Plan eligibility.
- Test the population with sample workers before assignment.

### 15.11 Included and excluded workers

Best practices:

- Define hierarchy scope in business language first.
- Convert to UI/HDL values only during implementation.
- Estimate assignees before submitting the assignment process.
- Treat excluded workers as future assignment filters; adding an exclusion later does not necessarily undo existing assignments.

Common HDL hierarchy mapping from Oracle examples:

| Business scope | HDL `CascadingLevel` |
|---|---:|
| Manager only | `0` |
| Direct reports only | `1` |
| All reports only | `999999` |
| Manager and direct reports | `2` |
| Manager and all reports | `1000000` |

### 15.12 Assignment process best practices

Regular Goal Plans require a scheduled process:

```text
Scheduled Processes for Performance Goals > Assign goal plans > Select Goal Plan > Submit
```

Before submission, capture:

- Goal Plan name and external ID
- Review Period
- Number of included goals
- Estimated assignees
- Eligibility expression
- Exclusions
- Estimated records = goals x assignees
- Whether scheduled queue/multithreading applies
- Notification behavior

After submission, capture:

- Process request ID
- Parent/child request IDs if multithreaded
- Status
- Error details
- Sample worker verification

### 15.13 Assignment rerun behavior

A rerun is additive. It may assign the plan to new workers and assign newly added goals to already selected workers. It should not be described as a reset or synchronization.

### 15.14 Delete and inactivate rules

- Delete only unassigned Goal Plans.
- Assigned Goal Plans can be made active or inactive, not deleted.
- Removing assignees is destructive and can permanently remove Goal Plans and goals for those assignees.
- Do not remove assignees when the plan is included in active Performance Documents for those assignees.
- `Delete All Assignees` requires a deliberately created user-level profile and should be treated as a controlled exceptional operation.

### 15.15 Goal Plan create checklist

```text
[ ] Redwood route verified or fallback route selected
[ ] GoalPlanExternalId defined
[ ] Review Period exists and active
[ ] Dates validated
[ ] Performance Document Type date envelope validated
[ ] Weighting policy validated
[ ] Goal-setting date policy validated
[ ] Goal count limits validated
[ ] Eligibility expression documented
[ ] Included/excluded population estimated
[ ] Created inactive
[ ] Child goals validated
[ ] Activated only after sign-off
[ ] Assignment process submitted only after explicit approval
[ ] Worker sample verified
```

---

## 16. Object 3: Performance Library Goals

### 16.1 Purpose

Performance Library Goals are reusable performance goals stored in the Goal Library. Users can copy them into Goal Management, Performance Management, and Talent Review contexts. Managers and HR specialists can assign them through Goal Plans or mass assignment.

### 16.2 Navigation

Redwood-enabled tenant:

```text
Setup and Maintenance > Workforce Development > Define Worker Goal Setting > Goal Library
```

Fallback / non-Redwood:

```text
My Client Groups > Goals > Performance Goal Library
```

### 16.3 Scope guardrail

Always confirm:

```yaml
goal_type: performance
```

Do not create a Development Library Goal from a Performance Library Goal prompt.

### 16.4 Core fields

| Field | Best-practice rule |
|---|---|
| External ID | Required by FSCR; max length is smaller than Goal Plan external ID, so keep short |
| Goal Name | Required; reusable and business-friendly |
| Type | Must resolve to performance type |
| Status | Create inactive first |
| Description | Recommended |
| Success Criteria | Strongly recommended |
| Start Date / Target Completion Date / To Date | Use only when lifecycle design requires date filtering |
| Performance Category | Optional unless the target tenant metadata or an approved governance policy requires it; validate the code when supplied or required |
| Subtype | Use for reporting or business classification |
| Priority / Level | Use only if governance requires it |
| Weight | Hidden by default in some UI flows; use only when plan design supports it |
| Available To | Explicitly choose HR only, HR+manager, or HR+manager+worker |
| Workforce restrictions | Use BU, Department, Legal Employer, Job Family, Job only when restriction design is ready |
| Tasks | Only when enabled and useful |
| Measurements | Must match measurement profile setting |
| Target Outcomes | Only after Profile Management prerequisites are met |
| Translations | Maintain for multilingual deployments |

### 16.5 External ID naming convention

Library Goal external IDs have a 30-character maximum in REST. Use short stable names:

```text
PGL_CUST_SAT_001
PGL_REV_GROW_001
PGL_QUALITY_001
PGL_COMPLIANCE_001
```

Avoid long fiscal-year IDs unless the goal is intentionally cycle-specific.

### 16.6 Status best practices

- Active means available to copy.
- Inactive means unavailable for new copying.
- A Library Goal can be inactivated even if workers have copied it.
- Existing copies continue to exist.
- Inactivation is the preferred retirement mechanism.

### 16.7 Copied-goal behavior

When a Performance Library Goal is copied, the copied goal can be changed. Later edits to the library goal do not update copied worker goals. External ID cannot be edited after creation.

Consultant answer pattern:

> Editing the library goal changes future copies only. Existing copied goals in worker plans, performance documents, or talent review contexts remain independent and must be handled separately if they require change.

### 16.8 Tasks, measurements, and outcomes

Before adding child sections, validate:

| Child section | Required setup |
|---|---|
| Tasks | Confirm the current Redwood/VBS page configuration exposes tasks; use `HRG_ENABLE_TASK` only for validated classic/RUI compatibility work |
| Measurements | Confirm the current Redwood page configuration and the requested measurement model; use `HRG_USE_MEASUREMENTS` only for validated classic/RUI compatibility work |
| Target Outcomes | Enhanced Talent Profiles, content-section access, and current Redwood/VBS page configuration; use legacy outcome or drill-down profiles only for validated classic/RUI compatibility work |

### 16.9 Workforce restrictions

In Redwood Goals Center, Oracle states that employees and managers are restricted to relevant legal entity, business unit, job family, and department library goals by default. Best practice is to validate actual visibility with sample users and current Redwood page configuration.

### 16.10 Availability best practices

| Available To | Use case |
|---|---|
| HR specialists only | Controlled HR assignment or plan seeding |
| HR specialists and managers | Manager assignment with HR governance |
| HR specialists, managers, and workers | Self-service library-goal discovery and copying |

Default availability may expose goals broadly, so explicitly set it during implementation.

### 16.11 Delete rules

Delete only when unused. If usage cannot be proven absent, inactivate instead. Usage may include Goal Plans, copied worker goals, performance documents, Talent Review, and mass assignment contexts.

### 16.12 Performance Library Goal checklist

```text
[ ] Goal type confirmed as Performance
[ ] GoalExternalId defined and length valid
[ ] Category/subtype lookups exist
[ ] Status set to Inactive for staging
[ ] Available To explicitly selected
[ ] Workforce restrictions designed and tested
[ ] Tasks profile and VBS settings checked
[ ] Measurements profile checked
[ ] Target outcome prerequisites checked
[ ] Translations completed if needed
[ ] Search LOV/TDS configuration checked
[ ] Activated only after visibility testing
[ ] Existing-copy impact explained before edits
```

---

## 17. Object 4: Development Library Goals

### 17.1 Purpose

Development Library Goals are reusable development goals stored in the development goal library. They support Career Development, Performance Management, and Talent Review contexts. Managers, employees, HR specialists, and other talent roles may copy or assign them depending on configuration and security.

### 17.2 Navigation

Primary route:

```text
My Client Groups > Career Development > Development Goal Library
```

If using a 26B redesigned Goal Library page, first verify that the page supports Development Library Goals and that the correct goal type is selected.

### 17.3 Scope guardrail

Always confirm:

```yaml
goal_type: development
```

Do not create a Performance Library Goal from a Development Library Goal prompt.

### 17.4 Career Development prerequisites

Before creating Development Library Goals, validate Career Development feature choices:

| Feature choice | Required when |
|---|---|
| Goal Library | Always required for Development Goal Library usage |
| Restrict Library Goal | Required only when library goals must be filtered by workforce structure |
| Development Goal Tasks | Required when adding tasks |
| Development Goal Measurement | Required when adding measurements; also controls single/multiple/disabled behavior |
| Target Outcomes | Required when adding target outcomes |
| Development Goal Drill Down Page | Required for detail sections such as measurements, tasks, and target outcomes |
| Development Goals Sharing | Required when sharing development goals is in scope |
| Development Intents | Required when associating intent such as current role, future role, or personal intent |
| Development Goal Learning | Required when Learning region/integration is in scope |
| Cancel/Delete Development Goals Assigned by HR | Required only if workers/managers can cancel or delete HR-assigned development goals |

### 17.5 Core fields

| Field | Best-practice rule |
|---|---|
| External ID | Required by FSCR; keep under REST max length |
| Goal Name | Required and reusable |
| Type | Must resolve to development type |
| Status | Create inactive first |
| Description | Recommended |
| Success Criteria | Recommended |
| Target Completion Date | Recommended for actionable development goals |
| Development Category | Required by governance |
| Priority | Optional, but useful for prioritization |
| Available To | Explicitly choose access scope |
| Business Unit / Department / Legal Employer / Job Family | Use when Restrict Library Goal is enabled or future filtering is expected |
| Tasks | Use when development actions need tracking |
| Measurements | Use only when meaningful for development outcomes |
| Target Outcomes | Use when tied to skills/competencies or other Talent Profile content |
| Development Intents | Use when enabled and business process requires intent capture |
| Learning | Use only when Career Development and Learning integration is designed |

### 17.6 External ID naming convention

Keep IDs short and type-specific:

```text
DGL_LEAD_001
DGL_CERT_PM_001
DGL_SKILL_AI_001
DGL_MENTOR_001
```

### 17.7 Development Library Goal status

- Active means available to copy.
- Inactive means unavailable for new copying.
- You can make a Development Library Goal inactive even if workers have copied it.
- Existing copied goals continue to exist.
- Inactivation is the preferred retirement path.

### 17.8 Copied-goal behavior

Oracle documents that Development Library Goals can be edited even after people copy them, but the copied goals are independent; updates to the library goal do not affect existing copied goals. The external ID cannot be edited.

### 17.9 Development library-goal restrictions

To restrict development library goals:

1. Enable **Restrict Library Goal** under the Career Development feature in the Workforce Development offering.
2. Define workforce structure parameters on library goals, such as legal employer, business unit, department, and job family.

When restricted:

| Scenario | Matching basis |
|---|---|
| Worker adds goal to own development plan | Worker's primary assignment |
| Manager/HR adds goal to a team member from Career Development or spotlight | Team member's primary assignment |
| Manager/HR adds goals to multiple team members from Career Overview | Manager or HR specialist's primary assignment |
| Talent Review facilitator adds goal to member | Review population member's primary assignment |
| Talent pool owner adds goal to talent pool | Talent pool owner's primary assignment |

Restriction does not apply to HR specialists using administrator pages from My Client Groups; they can select any library goal there.

### 17.10 Development Goal Library LOV/search configuration

Use Transaction Design Studio search configuration for Development Goal Library to expose relevant filters. Defaults are Goal name and Goal category. If restrictions are enabled, add workforce-structure filters so users can understand why goals are or are not visible.

### 17.11 Development Library Goal checklist

```text
[ ] Goal type confirmed as Development
[ ] Career Development Goal Library enabled
[ ] External ID defined and length valid
[ ] Development category lookup exists
[ ] Status set to Inactive for staging
[ ] Available To explicitly selected
[ ] Restrict Library Goal feature decision documented
[ ] Workforce restrictions defined when needed
[ ] Task feature checked
[ ] Measurement feature checked
[ ] Target outcome prerequisites checked
[ ] Drill-down page feature checked
[ ] Development intents / learning dependencies checked if used
[ ] TDS search configuration checked
[ ] Activated only after visibility testing
[ ] Existing-copy impact explained before edits
```

---

## 18. REST and HDL best practices

### 18.1 REST principles

Use REST when:

- The target object and operation are supported by Oracle HCM REST.
- The implementation needs repeatable automated setup.
- Security and audit controls are in place.
- Tenant-specific codes and IDs are resolved through metadata or LOV resources.

Do not use REST when:

- The endpoint is an LOV endpoint that supports only GET/Describe.
- The UI performs business validations that the REST flow has not replicated.
- Child collection synchronization is unclear.
- The operation is destructive and usage cannot be proven.

### 18.2 Goal Plans REST

Collection endpoint:

```text
/hcmRestApi/resources/11.13.18.05/goalPlans
```

Important fields include:

- `GoalPlanExternalId`
- `GoalPlanName`
- `StartDate`
- `EndDate`
- `ReviewPeriodId`
- `GoalPlanActiveCode`
- `GoalPlanTypeCode`
- `PrimaryGoalPlanFlag`
- `EnableWeightingFlag`
- `EnforceGoalWeightFlag`
- `GoalSettingStartDate`
- `GoalSettingEndDate`
- `RestrictGoalCreationFlag`
- `RestrictGoalUpdateFlag`

Best practice is to POST inactive, then PATCH active only after verification.

### 18.3 Library Goals REST

Collection endpoint:

```text
/hcmRestApi/resources/11.13.18.05/libraryGoals
```

This resource includes both performance and development library goal fields, including:

- `GoalExternalId`
- `GoalName`
- `TypeCode`
- `StatusCode`
- `PerfCategoryCode`
- `DevCategoryCode`
- `GoalSubTypeCode`
- `PriorityCode`
- `Visible`
- `BusinessUnitId`
- `DepartmentId`
- `LegalEmployerId`
- `JobFamilyId`
- `JobId`
- `libraryGoalTasks`
- `libraryGoalMeasures`
- `libGoalTargetOutcomes`
- `libraryGoalsDFF`

Best practices:

- Resolve `TypeCode` to Performance or Development explicitly.
- Use `PerfCategoryCode` for Performance Library Goals.
- Use `DevCategoryCode` for Development Library Goals.
- Do not guess status or visibility codes.
- Treat child collections as intentional merges, not implicit replacements.

### 18.4 HDL load order

Oracle HDL guidance identifies dependencies. Use this order:

```text
1. Worker and primary assignment
2. Eligibility profile
3. Organization
4. Goal plan document type
5. Review Period exists in target
6. Goal Plan
7. Content item for Library Goal
8. Goals and Goal Plan assignments, if used
```

Library Goals are loaded as Profile Management content items. The target tenant's ContentItem metadata must be checked before hard-coding positional item attributes.

### 18.5 HDL safety rules

- Ensure no pending performance or development goal transactions for affected workers before loading goal changes.
- Remember that HDL loading does not trigger approvals.
- Use stable `SourceSystemOwner` and `SourceSystemId`.
- Load lookups and value sets before objects that reference them.
- Load Review Periods through supported setup/UI unless a confirmed HDL object exists in the tenant.
- For development goals, remember worker development goals are not associated with Goal Plans.
- For worker performance goals, Goal Plans are required.

---

## 19. Diagnostics, integrity checks, and troubleshooting

### 19.1 Goal Management Diagnostics Report

Oracle provides a Goal Management Diagnostics Report process. It can show:

- Performance Goal data for a worker.
- Goal Plan assignments.
- Organization goals.
- Shared goals.
- Goal alignment details.
- Goal profile options and other configurations.
- Flexfield configuration.
- Notification setup.
- Bypass approval settings.
- Diagnostic lookup masking configuration.

Best practices:

- Run diagnostics after data migration and after annual-cycle setup.
- Run diagnostics for at least one worker per population segment.
- Save diagnostic output with the cutover evidence pack.
- Review masking lookup values before sharing outputs.

### 19.2 Common troubleshooting map

| Symptom | Likely causes | Checks |
|---|---|---|
| Goal Plan not visible to worker | Not assigned, inactive, wrong Review Period, data security | Assignment process, status, Review Period, worker security |
| Goals not in performance document | Review Period/document type mismatch, Performance Goals section not configured, approvals pending | Goal Plan doc type, template Review Period, section setup, Update Goals action |
| Library Goal not visible | Inactive, Available To excludes role, workforce restriction, TDS/LOV filters, Redwood default restriction | Status, visibility, BU/Dept/LE/JF, sample user |
| Target outcomes not visible | Profile/feature disabled, Enhanced Talent Profiles missing, no content access, VBS hidden | Profiles/features, content section access, page configuration |
| Goal Plan assignment did not process all workers | Eligibility, exclusions, manager hierarchy, process errors, data security | ESS log, population estimate, eligibility expression |
| Delete disabled | Object is used or route does not expose delete | Usage analysis, inactivate instead |
| HR specialist can view but not edit | Read-only custom role or removed manage privileges | Role privileges and aggregate grants |
| Employee cannot edit after goal-setting end date | Goal Plan restrictions or VBS/security | Goal-setting dates, worker update settings, page rules |

---

## 20. Testing strategy

### 20.1 Unit test each setup object

| Object | Unit tests |
|---|---|
| Review Period | Unique name, active/inactive, date validation, used-period date-change block, inactive visibility |
| Goal Plan | Create inactive, Review Period, doc type association, weights, goal counts, eligibility, population, activation |
| Performance Library Goal | External ID, status, category/subtype, availability, restrictions, tasks, measurements, outcomes, translations |
| Development Library Goal | External ID, status, development category, Career Development features, restrictions, tasks, measurements, outcomes, intents |

### 20.2 End-to-end test scenarios

1. Worker copies a Performance Library Goal into an assigned regular Goal Plan.
2. Manager assigns a Performance Library Goal to direct reports.
3. HR specialist assigns a Goal Plan to an eligibility-based population.
4. Performance Document is created and pulls goals from the matching Review Period and document type.
5. Worker copies a Development Library Goal into development plan.
6. Manager adds a Development Library Goal for a team member.
7. Restricted library goals are visible only for matching workforce structures.
8. Inactive Library Goals are not available for new copying.
9. Edited Library Goal does not update existing copied goals.
10. Read-only HR specialist can view but not modify goal objects.
11. Goal-setting end-date restriction blocks employee actions but not manager/HR actions.
12. Diagnostics report confirms profile, flexfield, notification, and goal assignment data.

### 20.3 Regression tests after quarterly update

After each Oracle quarterly update:

- Revalidate Redwood route behavior.
- Revalidate VBS page-property rules.
- Revalidate TDS rules and LOV filters.
- Revalidate scheduled process pages and advanced options.
- Revalidate read-only HR specialist behavior.
- Revalidate REST describe metadata for changed fields or child collections.
- Revalidate HDL object metadata.

---

## 21. Migration and cutover best practices

### 21.1 Migration sequence

```text
1. Profiles and feature choices
2. Lookups and value sets
3. DFFs and deployment
4. Profile Management content sections and access
5. Security roles and data roles
6. TDS and VBS customizations
7. Notifications and approvals
8. Review Periods
9. Performance Library Goals
10. Development Library Goals
11. Goal Plans
12. Goal Plan assignments or mass processes
13. Diagnostics and evidence
```

### 21.2 Cutover controls

- Freeze lookup and DFF changes before loading goals.
- Load Library Goals inactive, verify, then activate.
- Create Goal Plans inactive, verify, then activate.
- Schedule assignment only after payroll/HR data is stable enough for assignment population.
- Communicate worker and manager availability dates.
- Capture ESS process request IDs.
- Run diagnostics for representative workers.

### 21.3 Rollback strategy

| Setup item | Preferred rollback |
|---|---|
| Review Period | Inactivate if unused or incorrect; create corrected period |
| Goal Plan | Inactivate if assigned; delete only if unassigned |
| Performance Library Goal | Inactivate; delete only if unused |
| Development Library Goal | Inactivate; delete only if unused |
| Lookup value | Disable future use if already referenced; avoid deleting used codes |
| DFF segment | Hide/deactivate if used; evaluate data impact before removal |
| TDS/VBS rule | Disable or revert rule version |
| Assignment process | No simple rollback; use assignee removal only with explicit destructive approval |

---

## 22. Risk register

| Risk | Impact | Mitigation |
|---|---|---|
| Wrong route used for Goal Plans | Consultant follows obsolete or incompatible page | Detect Redwood profiles and verify actual page |
| Duplicate Library Goals | Users see inconsistent reusable goals | Use External ID idempotency and search before create |
| Goal Plan assignment sent to wrong population | Large-scale incorrect worker goals | Population estimate, eligibility expression, approval gate |
| Review Period dates wrong after use | Cannot easily change dates | Validate before use; create new Review Period if used |
| Performance documents don't pull goals | Review Period/document type mismatch | Validate template, document period, and Goal Plan associations |
| Library Goal restrictions misunderstood | Goals visible to wrong users or hidden from right users | Test sample users across BU/department/legal employer/job family |
| Target outcomes missing | Goal pages incomplete and profiles not updated | Validate profile/feature/content-section prerequisites |
| DFF not deployed | Fields missing or integration failure | Deploy DFF and retest before object setup |
| Read-only HR specialist cannot complete admin task | Missing manage privileges | Use separate edit-capable admin role for setup |
| HDL load bypasses approvals | Unapproved data changes | Treat HDL as admin migration; validate before/after |
| VBS hides action but privilege still exists elsewhere | Inconsistent control | Use privileges for security, VBS for UI visibility |

---

## 23. Codex response snippets

### 23.1 Review Period prompt

```text
For Review Period setup, first confirm the business cycle, unique name, dates, and status. Create the Review Period before Goal Plans or Performance Document periods. If the Review Period is already used, do not recommend changing start/end dates; create a replacement period and inactivate the old one after impact analysis.
```

### 23.2 Goal Plan prompt

```text
For Goal Plan setup, determine whether this is a regular Goal Plan or Primary Goal Plan. For a regular plan, create it inactive, associate an active Review Period, validate start/end dates, associate active Performance Document Types whose dates cover the plan, configure weights and restrictions, define eligibility/included/excluded population, then activate and run Assign goal plans only after explicit approval.
```

### 23.3 Performance Library Goal prompt

```text
For a Performance Library Goal, confirm goal_type=performance, require a short stable external ID, create inactive, set category/subtype/availability, validate tasks/measurements/target-outcome prerequisites, test visibility for intended roles and workforce structures, then activate. Explain that edits affect future copies only.
```

### 23.4 Development Library Goal prompt

```text
For a Development Library Goal, confirm goal_type=development and use the Career Development administrator flow unless the tenant's Redwood Goal Library page explicitly supports development goals. Validate Career Development feature choices for Goal Library, restrictions, tasks, measurements, target outcomes, drill-down page, intents, and learning before creating the goal inactive.
```

### 23.5 Dependent setup prompt

```text
For dependent Goal Management setup, cover Workforce Development offering readiness, security, profile options, Career Development features, lookups, value sets, DFF deployment, Profile Management target outcome prerequisites, notifications, approvals, TDS, VBS page properties, HDL/REST metadata, and diagnostics. Separate Oracle-required setup from customer governance choices.
```

---

## 24. Consultant checklist by phase

### 24.1 Design phase

```text
[ ] Decide Redwood/non-Redwood target experience
[ ] Define annual/semiannual/quarterly Review Period strategy
[ ] Decide regular Goal Plans vs Primary Goal Plan vs Goal Plan Sets
[ ] Define Performance Document Type and template integration
[ ] Define Performance Library Goal taxonomy
[ ] Define Development Library Goal taxonomy
[ ] Define categories, subtypes, priorities, measurement design
[ ] Define workforce restrictions and availability rules
[ ] Define target outcome and Profile Management strategy
[ ] Define notifications, nudges, approvals, and guided journeys
[ ] Define role/security matrix
[ ] Define migration and cutover sequence
```

### 24.2 Build phase

```text
[ ] Enable required profiles and feature choices
[ ] Configure security roles and data roles
[ ] Configure lookups and value sets
[ ] Configure and deploy DFFs
[ ] Configure Profile Management content sections and access
[ ] Configure TDS and VBS rules
[ ] Configure notifications and approvals
[ ] Create Review Periods
[ ] Create Library Goals inactive
[ ] Create Goal Plans inactive
[ ] Validate and activate only after sign-off
```

### 24.3 Test phase

```text
[ ] Test with implementation user
[ ] Test with HR specialist edit role
[ ] Test with HR specialist read-only role
[ ] Test with manager
[ ] Test with employee
[ ] Test REST/HDL idempotency if used
[ ] Test Performance Document integration
[ ] Test Development Goal Library visibility
[ ] Test restricted Library Goal visibility
[ ] Test diagnostics report
[ ] Document defects and remediation
```

### 24.4 Cutover phase

```text
[ ] Freeze setup inputs
[ ] Confirm latest worker and assignment data
[ ] Migrate lookups, DFF, profiles, features, and page rules
[ ] Migrate Review Periods
[ ] Migrate Library Goals inactive and validate
[ ] Activate Library Goals
[ ] Migrate Goal Plans inactive and validate
[ ] Activate Goal Plans
[ ] Submit assignment processes after approval
[ ] Monitor ESS processes
[ ] Run diagnostics and sample verification
[ ] Store evidence pack
```

---

## 25. Source references

These references were used to prepare this best-practice document. Oracle Help Center pages should be treated as authoritative for the current tenant release, but always verify behavior in the target pod.

### Oracle readiness / What's New

- Redwood Redesigned Goals Configuration Pages in Setup and Maintenance Work Area: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43819.htm
- Redwood Redesigned Scheduled Processes for Goals Pages: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43818.htm
- Redwood Read-Only Goals Administrative Tasks: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43816.htm
- Goal Setting Dates and Restrictions: https://docs.oracle.com/en/cloud/saas/readiness/hcm/25d/tama-25d/25D-talent-mgmt-wn-f40678.htm
- Redwood Nudge Reminder to Enter Goals Before Goal-Setting End Date: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43811.htm
- Redwood Control Goal Actions Based on Role: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43920.htm
- Redwood New Visual Builder Studio Page Properties: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43820.htm
- Redwood Hide Shared Goals and Organization Goals Already Added to Worker Goal Plan or Development Plan: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43817.htm
- Redwood Enable Negative Values for Goal Measurements: https://docs.oracle.com/en/cloud/saas/readiness/hcm/26b/tama-26b/26B-talent-mgmt-wn-f43922.htm

### Oracle implementation / using docs

- Overview of Worker Goal Settings: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/overview-of-worker-goal-settings.html
- Setup Tasks for Implementing Goal Management: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/setup-tasks-for-implementing-goal-management.html
- Goal Management Profile Options: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/goal-management-profile-options.html
- Goal Lookups: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/goal-lookups.html
- Descriptive Flexfields for Goals: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/descriptive-flexfields-for-goals.html
- Goal Notifications: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/goal-notifications.html
- How You Configure Goal Management Pages Using Transaction Design Studio: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/how-you-configure-goal-management-pages-using-transaction-design.html
- Configure Performance Goal Library List of Values: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/configure-performance-goal-library-list-of-values.html
- Configure Development Goal Library List of Values: https://docs.oracle.com/en/cloud/saas/talent-management/fatcd/configure-development-goal-library-list-of-values.html
- Goal Management Diagnostics: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/goal-management-diagnostics.html
- Create Review Periods: https://docs.oracle.com/en/cloud/saas/talent-management/faigc/create-review-periods.html
- Review Periods in Talent Management: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/review-periods-in-talent-management.html
- Goal Plans: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/goal-plans.html
- How You Create Goal Plans: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/how-you-create-goal-plans.html
- Overview of Primary Goal Plan: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/overview-of-primary-goal-plan.html
- How You Assign Goal Plans: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/how-you-assign-goal-plans.html
- How You Use Eligibility Profiles when Assigning Performance Goals: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/how-you-use-eligibility-profiles-when-assigning-performance.html
- How Performance Documents Work with Performance Goals: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/how-performance-documents-work-with-performance-goals.html
- Goal Library: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/goal-library.html
- How You Create Library Goals in Goal Management: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/how-you-create-library-goals-in-goal-management.html
- Considerations for Restricting Library Goals: https://docs.oracle.com/en/cloud/saas/talent-management/faugm/considerations-for-restricting-library-goals.html
- Redwood Library Goal Restriction FAQ: https://docs.oracle.com/en/cloud/saas/talent-management/fagcq/how-to-restrict-library-goals-access-to-the-employee-s-department-or-business-unit.html
- Development Goal Library: https://docs.oracle.com/en/cloud/saas/talent-management/faucd/development-goal-library.html
- How You Create Library Goals in Career Development: https://docs.oracle.com/en/cloud/saas/talent-management/faucd/how-you-create-library-goals-in-career-development.html
- How You Edit Library Goals in Career Development: https://docs.oracle.com/en/cloud/saas/talent-management/25b/faucd/how-you-edit-library-goals-in-career-development.html
- Considerations for Restricting Library Goals from Development Goal Library: https://docs.oracle.com/en/cloud/saas/talent-management/faucd/considerations-for-restricting-library-goals-from-development-goal-library.html
- Considerations for Implementing Career Development Features: https://docs.oracle.com/en/cloud/saas/talent-management/fatcd/considerations-for-implementing-career-development-features.html
- How Goal Management Works with Profiles: https://docs.oracle.com/en/cloud/saas/talent-management/faigm/how-goal-management-works-with-profiles.html

### REST and HDL

- REST: Create a Goal Plan: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-goalplans-post.html
- REST: Create a Library Goal: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-librarygoals-post.html
- REST: Update a Library Goal: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-librarygoals-librarygoalsuniqid-patch.html
- REST: Get a Library Goal: https://docs.oracle.com/en/cloud/saas/human-resources/farws/op-librarygoals-librarygoalsuniqid-get.html
- HDL: Overview of Loading Goals, Goal Plans, and Goal Plan Sets: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/overview-of-loading-goals-goal-plans-and-goal-plan-sets.html
- HDL: Guidelines for Loading Goals: https://docs.oracle.com/en/cloud/saas/human-resources/fahbo/guidelines-for-loading-goals.html

---

## 26. Final FSCR guidance

Use this document as the first-pass implementation reference for Goal Management consultant prompts. Then verify every tenant-specific point against the target environment. The best consultant answers should be explicit about route selection, safety gates, dependencies, and validation evidence.

The safest mental model is:

```text
Review Period defines the cycle.
Library Goals define reusable goal content.
Goal Plans define performance-goal containers, rules, populations, and performance-document integration.
Career Development feature choices govern Development Library Goal behavior.
Security, profiles/features, lookups, DFF, TDS/VBS, notifications, approvals, Profile Management, REST/HDL, and diagnostics make the setup usable, governable, and supportable.
```
