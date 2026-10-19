# Oracle 26B HCM Implementation User and AI Agent Studio Reference

Use this reference when creating greenfield HCM implementation users for
Workforce Deployment.

## Oracle Sources

- HCM implementation users:
  https://docs.oracle.com/en/cloud/saas/human-resources/ochus/overview-of-creating-hcm-implementation-users.html
- Functional Setup Manager setup activity role mapping:
  https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/mapping-of-setup-activities-and-required-roles.html#s20075606
- HCMUser implementation user:
  https://docs.oracle.com/en/cloud/saas/human-resources/ochus/create-the-hcmuser-implementation-user.html
- HCM data roles:
  https://docs.oracle.com/en/cloud/saas/human-resources/ochus/overview-of-hcm-data-roles-for-implementation-users.html
- Abstract-role security profiles:
  https://docs.oracle.com/en/cloud/saas/human-resources/ochus/assign-security-profiles-to-abstract-roles.html
- HCM implementation role mapping:
  https://docs.oracle.com/en/cloud/saas/human-resources/ochus/create-a-role-mapping-for-hcm-implementation-data-roles.html
- Assign roles to HCMUser:
  https://docs.oracle.com/en/cloud/saas/human-resources/ochus/assign-abstract-and-data-roles-to-hcmuser.html
- AI Agent Studio access requirements:
  https://docs.oracle.com/en/cloud/saas/fusion-ai/26b/aiaas/access-ai-agent-studio.html
- AI Agent Studio all-products configuration access:
  https://docs.oracle.com/en/cloud/saas/fusion-ai/26b/aiaas/access-to-configure-ai-agents-in-all-products.html
- HCM AI Agent Studio configuration access:
  https://docs.oracle.com/en/cloud/saas/fusion-ai/26b/aiaas/access-to-configure-ai-agents-in-oracle-fusion-cloud-human-capital-management-hcm.html

## Setup Task Codes

| Task | Task Code | Purpose |
| --- | --- | --- |
| Create Implementation Users | FND_CREATE_IMPLEMENTATION_USERS | Create or edit implementation user accounts |
| Create Data Role for Implementation Users | FND_CREATE_DATA_ROLE_FOR_IMPLEMENTATION_USERS | Create implementation data roles |
| Assign Security Profiles to Role | ORA_PER_ASSIGN_SECURITY_PROFILES_TO_ROLE | Create/edit HCM data roles and assign security profiles |
| Manage Role Provisioning Rules | ORA_PER_MANAGE_ROLE_PROVISIONING_RULES | Create the Requestable Roles mapping |
| Manage Administrator Profile Values | FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES | Set AI Agent Studio profile option |
| Import Users and Roles into Application Security | ORA_ASE_IMPORT_USERS_AND_ROLES | Initialize or refresh security tables |

## Setup Sequence

1. Sign in using the Oracle HCM Cloud service administrator from the welcome or
   activation email.
2. Run `Retrieve Latest LDAP Changes`.
3. Run `Import Users and Roles into Application Security`.
4. Set profile option `ORA_ASE_SAS_INTEGRATION_ENABLED` at Site level to `Yes`.
5. Create the implementation user through `Create Implementation Users`.
6. Assign base HCMUser job roles.
7. Create or verify HCM data roles.
8. Assign HCM security profiles to data roles and abstract roles.
9. Create `Requestable Roles` role mapping.
10. Assign abstract, data, and AI Agent Studio access roles to the user.
11. Run AI Agent Studio security-data import scheduled processes.
12. Validate HCM and AI Agent Studio access.

## Implementation User Fields

| Field | Value |
| --- | --- |
| Associated Person Type | None |
| User Category | DEFAULT |
| Last Name | Username unless explicitly supplied |
| Email | User-provided valid email |
| User Name | User-provided username |
| Active | Selected |

## Base Job Roles

| Display Name | Role Code |
| --- | --- |
| Application Administrator | ORA_FND_APPLICATION_ADMINISTRATOR_JOB |
| Application Implementation Consultant | ORA_ASM_APPLICATION_IMPLEMENTATION_CONSULTANT_JOB |
| Application Implementation Manager | ORA_ASM_APPLICATION_IMPLEMENTATION_MANAGER_JOB |
| Application Diagnostics Regular User | ORA_FND_DIAG_REGULAR_USER_JOB |
| Application Diagnostics Viewer | ORA_FND_DIAG_VIEWER_JOB |
| Application Diagnostic Administrator | ORA_FND_DIAG_ADMINISTRATOR_JOB |
| IT Security Manager | ORA_FND_IT_SECURITY_MANAGER_JOB |

## Oracle Functional Setup Manager Setup Activity Roles

Oracle 26B `Mapping of Setup Activities and Required Roles` lists these
distinct roles across setup activities:

| Display Name | Type |
| --- | --- |
| Application Implementation Consultant | Job |
| Application Implementation Manager | Job |
| Functional Setups User | Abstract |
| Export Import Functional Setups User | Abstract |

Treat `Manage Setup Migration Settings`, `Manage Third Party Applications`, and
task-specific setup data privileges as privilege requirements, not distinct role
grants.

## Required HCM Data Roles

| Data Role | Job Role |
| --- | --- |
| HRAnalyst_ViewAll | Human Resource Analyst |
| HCMApplicationAdministrator_ViewAll | Human Capital Management Application Administrator |
| HRSpecialist_ViewAll | Human Resource Specialist |

Optional licensed-service roles:

| Data Role | Condition |
| --- | --- |
| CompensationAdmin_ViewAll | Workforce Compensation licensed |
| CompensationMgr_ViewAll | Workforce Compensation licensed |
| PayrollAdmin_ViewAll | Global Payroll licensed |
| PayrollMgr_ViewAll | Global Payroll licensed |

## HCM Data Role Security Profiles

| Data Role | Security Profile Assignments |
| --- | --- |
| HRAnalyst_ViewAll | Organization: View All Organizations; Position: View All Positions; Legislative Data Group: View All Legislative Data Groups; Person: View All People; Public Person: View All People; Document Type: View All Document Types; Payroll Flow: View All Flows |
| HCMApplicationAdministrator_ViewAll | Organization: View All Organizations; Position: View All Positions; Legislative Data Group: View All Legislative Data Groups; Person: View All People; Public Person: View All People; Document Type: View All Document Types; Payroll: View All Payrolls; Payroll Flow: View All Flows; Transaction: View All HCM Transactions |
| HRSpecialist_ViewAll | Organization: View All Organizations; Position: View All Positions; Countries: View All Countries; Legislative Data Group: View All Legislative Data Groups; Person: View All People; Public Person: View All People; Document Type: View All Document Types; Payroll: View All Payrolls; Payroll Flow: View All Flows |

## Abstract Role Security Profiles

| Abstract Role | Security Profile Assignments |
| --- | --- |
| Employee | Organization: View All Organizations; Position: View All Positions; Country: View All Countries; LDG: View All Legislative Data Groups; Person: View Own Record; Public Person: View All Workers; Document Type: View All Document Types |
| Contingent Worker | Organization: View All Organizations; Position: View All Positions; Country: View All Countries; LDG: View All Legislative Data Groups; Person: View Own Record; Public Person: View All Workers; Document Type: View All Document Types |
| Line Manager | Organization: View All Organizations; Position: View All Positions; Country: View All Countries; LDG: View All Legislative Data Groups; Person: View Manager Hierarchy; Public Person: View All Workers; Document Type: View All Document Types; Payroll: View All Payrolls; Payroll Flow: View All Flows |

## Role Mapping

Create one implementation-only mapping:

- Mapping Name: `Requestable Roles`
- Condition: HR Assignment Status = `Active`
- Associated roles: required HCM data roles and any licensed optional data roles
- Requestable: selected
- Self-Requestable: not selected
- Autoprovision: not selected

Delete the role mapping when implementation is complete to avoid broad ongoing
requestability of implementation roles.

## Final Roles Assigned to the User

Assign these roles after the setup roles and security profiles exist:

- base job roles
- `Functional Setups User`
- `Export Import Functional Setups User`
- `Employee`
- `Contingent Worker`
- `Line Manager`
- `HRAnalyst_ViewAll`
- `HCMApplicationAdministrator_ViewAll`
- `HRSpecialist_ViewAll`
- optional licensed-service data roles, when created
- approved AI Agent Studio all-products custom access role

## AI Agent Studio Access Requirements

Required profile setting:

| Profile Option | Code | Level | Value |
| --- | --- | --- | --- |
| Enable Security Console External Application Integration | ORA_ASE_SAS_INTEGRATION_ENABLED | Site | Yes |

After setting the profile option, run these scheduled processes sequentially:

1. `Import Resource Application Security Data`
2. `Import User and Role Application Security Data`

For all-products AI Agent Studio configuration access:

- Go to Security Console and create a custom job role.
- Enable permission groups.
- On the Role Hierarchy page, open the Roles and Permission Groups tab and add
  the product administrator duty roles below.
- Open the Roles and Privileges tab and add `Manage All Intelligent Agents`
  (`ORA_FAI_MANAGE_ALL_AI_AGENTS`).
- Save the custom role and assign it to implementation users who need access to
  configure all agents in all products.

| Product | Duty Role | Code |
| --- | --- | --- |
| CX | Fai Genai Agent CX Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_CX_ADMINISTRATOR_DUTY |
| Financials | Fai Genai Agent FIN Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_FIN_ADMINISTRATOR_DUTY |
| GRC | Fai Genai Agent GRC Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_GRC_ADMINISTRATOR_DUTY |
| HCM | Fai Genai Agent HCM Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_HCM_ADMINISTRATOR_DUTY |
| Procurement | Fai Genai Agent PRC Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_PRC_ADMINISTRATOR_DUTY |
| Project Management | Fai Genai Agent PRJ Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_PRJ_ADMINISTRATOR_DUTY |
| Public Sector | Fai Genai Agent PSC Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_PSC_ADMINISTRATOR_DUTY |
| SCM | Fai Genai Agent SCM Administrator Duty | ORA_DR_FAI_GENERATIVE_AI_AGENT_SCM_ADMINISTRATOR_DUTY |

| Privilege Role | Code |
| --- | --- |
| Manage All Intelligent Agents | ORA_FAI_MANAGE_ALL_AI_AGENTS |

Optional AI Agent Studio capabilities:

- For External REST API tools, add `Create and Edit Backends for Visual Builder
  Studio` (`ORA_FND_TRAP_PRIV`) to the custom role.
- For channel creation, add the channel permission groups and the
  `AllRowsAllFields` security view.
- For monitored agent records, add `read:Generative AI Workflow Execution` and
  the `AllRowsRestrictedFields` security view.
