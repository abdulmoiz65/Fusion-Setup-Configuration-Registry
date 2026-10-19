---
skill_id: "hcm.global-payroll.payroll-common"
name: "Payroll Common Implementation Guidance"
description: "Provides HCM Global Payroll implementation guidance for the Payroll Common functional area."
layer: "pillar"
pillar: "HCM"
offering: "Global Payroll"
functional_area: "Payroll Common"
functional_area_code: "ORA_PAYROLL_COMMON"
type: "planning"
execution_mode: "assisted"
owner_team: "HCM global payroll pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "payroll_common_scope"
  - "payroll_common_requirements"
outputs:
  - "functional_area_setup_plan"
  - "configuration_guidance"
  - "validation_checkpoints"
  - "skill_run_record"
  - "token_usage_record"
depends_on:
  - "shared.implementation-planning.offering-task-map-builder"
  - "shared.implementation-planning.task-dependency-resolver"
  - "shared.setup-export.functional-area-export"
uses_core:
  - "core.project-mgmt.artifact-version-manager"
  - "core.project-mgmt.artifact-registry-manager"
  - "core.project-mgmt.project-state-manager"
  - "core.diagnostics.role-access-check"
persists_project_state: true
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
state_updates:
  - "setup_task_sequence"
  - "design_decisions"
  - "configuration_blueprints"
  - "validation_results"
  - "token_usage_records"
workspace_outputs:
  - artifact_type: "setup_task_sequence"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/hcm/global-payroll/payroll-common/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "FND_MANAGE_PROFILE_OPTIONS"
  - "FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES"
  - "FND_MANAGE_COMMON_LOOKUPS"
  - "FND_MANAGE_STANDARD_LOOKUPS"
  - "FND_MANAGE_VALUE_SETS"
  - "FND_MANAGE_DESCRIPTIVE_FLEXFIELDS"
  - "FND_MANAGE_EXTENSIBLE_FLEXFIELDS"
  - "FND_MANAGE_KEY_FLEXFIELDS"
  - "PER_MANAGE_WORKFORCE_RECORDS_PROFILE_OPTIONS"
  - "PER_MANAGE_WORKFORCE_RECORDS_EMPLOYMENT_PROFILE_OPTIONS"
  - "PAY_MANAGE_PAYROLL_EMPLOYMENT_HIERARCHY_PROFILE_OPTIONS"
  - "ORA_SVC_MANAGE_ADDRESS_VALIDATION"
  - "PER_MANAGE_ORGANIZATION_LOOKUPS"
  - "PER_MANAGE_LOCATION_LOOKUPS"
  - "PER_MANAGE_JOB_LOOKUPS"
  - "PER_MANAGE_POSITION_LOOKUPS"
  - "PER_MANAGE_PERSON_LOOKUPS"
  - "ORA_PER_MANAGE_BARGAINING_UNIT_LOOKUP"
  - "PER_MANAGE_ASSIGNMENT_GRADE_LOOKUPS"
  - "PER_MANAGE_WORK_TERMS/ASSIGNMENT_JOB_DETAIL_LOOKUPS"
  - "PER_MANAGE_EMPLOYMENT_CONTRACT_LOOKUPS"
  - "PER_MANAGE_TERMINATIONS_LOOKUPS"
  - "PER_MANAGE_DOCUMENTS_LOOKUPS"
  - "HRX_MANAGE_CHINESE_PAYROLL_DEDUCTION_DEFINITIONS_LOOKUPS"
  - "HRX_MANAGE_UK_PAYROLL_LOOKUPS"
  - "PAY_MANAGE_PAYROLL_LOOKUPS"
  - "ORA_HWM_MANAGE_WORKFORCE_MANAGEMENT_LOOKUPS"
  - "PER_MANAGE_EXTENDED_LOOKUP_CODE"
  - "ORA_ANC_MANAGE_GLOBAL_ABSENCE_LOOKUPS"
  - "PER_MANAGE_ASSIGNMENT_RESPONSIBILITY_LOOKUPS"
  - "PER_MANAGE_VALUE_SETS"
  - "PAY_MANAGE_PAYROLL_VALUE_SETS"
  - "ORA_HXT_MANAGE_TIME_AND_LABOR_VALUE_SETS"
  - "ORA_ANC_MANAGE_GLOBAL_ABSENCE_VALUE_SETS"
  - "PER_DESC_FLEXFIELDS_FOR_HR_ENTERPRISE_STRUCTURES"
  - "ORA_PER_MANAGE_ORGSTRUCTURES_EXTENSIBLE_FLEXFIELDS"
  - "PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_GRADE"
  - "ORA_PER_MANAGE_WORKFORCE_STRUCTURES_DESCRIPTIVE_FLEXFIELDS"
  - "ORA_PER_MANAGE_WORKFORCE_STRUCTURES_EXTENSIBLE_FLEXFIELDS"
  - "PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_PERSON"
  - "ORA_PER_MANAGE_PERSON_EXTENSIBLE_FLEXFIELDS"
  - "PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_EMPLOYMENT"
  - "ORA_PER_MANAGE_EMPLOYMENT_EXTENSIBLE_FLEXFIELDS"
  - "PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_DOCUMENTS"
  - "ORA_DOCUMENT_TYPE_DESCRIPTIVE_FLEXFIELDS"
  - "PAY_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_PAYROLL"
  - "ORA_PAY_MANAGE_EXTENSIBLE_FLEXFIELDS_FOR_PAYROLL"
  - "FND_MANAGE_AUDIT_POLICIES"
  - "ORA_GMS_MANAGE_AUDIT_TYPES"
applicability:
  industries:
    - "All"
  countries:
    - "All"
  fusion_releases:
    - "Current Oracle Fusion Cloud release"
side_effects: []
required_privileges: []
---

# Payroll Common Implementation Guidance

## Purpose

Provides HCM Payroll implementation guidance for the Payroll Common functional area.

## When to Use

Use this functional-area skill after Payroll scope is confirmed and the project needs payroll common setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `HCM`
- Offering: `Global Payroll` (`ORA_GLOBAL_PAYROLL`)
- Functional area / Setup Object: `Payroll Common` (`ORA_PAYROLL_COMMON`)

## Setup Tasks

1. [Manage Profile Options](manage-profile-options/SKILL.md) (`FND_MANAGE_PROFILE_OPTIONS`)
2. [Manage Administrator Profile Values](manage-administrator-profile-values/SKILL.md) (`FND_MANAGE_ADMINISTRATOR_PROFILE_VALUES`)
3. [Manage Common Lookups](manage-common-lookups/SKILL.md) (`FND_MANAGE_COMMON_LOOKUPS`)
4. [Manage Standard Lookups](manage-standard-lookups/SKILL.md) (`FND_MANAGE_STANDARD_LOOKUPS`)
5. [Manage Value Sets](manage-value-sets/SKILL.md) (`FND_MANAGE_VALUE_SETS`)
6. [Manage Descriptive Flexfields](manage-descriptive-flexfields/SKILL.md) (`FND_MANAGE_DESCRIPTIVE_FLEXFIELDS`)
7. [Manage Extensible Flexfields](manage-extensible-flexfields/SKILL.md) (`FND_MANAGE_EXTENSIBLE_FLEXFIELDS`)
8. [Manage Key Flexfields](manage-key-flexfields/SKILL.md) (`FND_MANAGE_KEY_FLEXFIELDS`)
9. [Manage Workforce Records Profile Option Values](manage-workforce-records-profile-option-values/SKILL.md) (`PER_MANAGE_WORKFORCE_RECORDS_PROFILE_OPTIONS`)
10. [Manage Workforce Records Employment Profile Option Values](manage-workforce-records-employment-profile-option-values/SKILL.md) (`PER_MANAGE_WORKFORCE_RECORDS_EMPLOYMENT_PROFILE_OPTIONS`)
11. [Payroll Employment Hierarchy Profile Option Values](payroll-employment-hierarchy-profile-option-values/SKILL.md) (`PAY_MANAGE_PAYROLL_EMPLOYMENT_HIERARCHY_PROFILE_OPTIONS`)
12. [Manage Address Validation Profile Options](manage-address-validation-profile-options/SKILL.md) (`ORA_SVC_MANAGE_ADDRESS_VALIDATION`)
13. [Manage Organization Lookups](manage-organization-lookups/SKILL.md) (`PER_MANAGE_ORGANIZATION_LOOKUPS`)
14. [Manage Location Lookups](manage-location-lookups/SKILL.md) (`PER_MANAGE_LOCATION_LOOKUPS`)
15. [Manage Job Lookups](manage-job-lookups/SKILL.md) (`PER_MANAGE_JOB_LOOKUPS`)
16. [Manage Position Lookups](manage-position-lookups/SKILL.md) (`PER_MANAGE_POSITION_LOOKUPS`)
17. [Manage Person Lookups](manage-person-lookups/SKILL.md) (`PER_MANAGE_PERSON_LOOKUPS`)
18. [Manage Bargaining Unit Lookup](manage-bargaining-unit-lookup/SKILL.md) (`ORA_PER_MANAGE_BARGAINING_UNIT_LOOKUP`)
19. [Manage Assignment Grade Lookups](manage-assignment-grade-lookups/SKILL.md) (`PER_MANAGE_ASSIGNMENT_GRADE_LOOKUPS`)
20. [Manage Work Terms and Assignment Lookups](manage-work-terms-and-assignment-lookups/SKILL.md) (`PER_MANAGE_WORK_TERMS/ASSIGNMENT_JOB_DETAIL_LOOKUPS`)
21. [Manage Employment Contract Lookups](manage-employment-contract-lookups/SKILL.md) (`PER_MANAGE_EMPLOYMENT_CONTRACT_LOOKUPS`)
22. [Manage Termination Lookups](manage-termination-lookups/SKILL.md) (`PER_MANAGE_TERMINATIONS_LOOKUPS`)
23. [Document Type Lookups](document-type-lookups/SKILL.md) (`PER_MANAGE_DOCUMENTS_LOOKUPS`)
24. [Manage Payroll Lookups for China](manage-payroll-lookups-for-china/SKILL.md) (`HRX_MANAGE_CHINESE_PAYROLL_DEDUCTION_DEFINITIONS_LOOKUPS`)
25. [Manage Payroll Lookups for UK](manage-payroll-lookups-for-uk/SKILL.md) (`HRX_MANAGE_UK_PAYROLL_LOOKUPS`)
26. [Payroll Lookups](payroll-lookups/SKILL.md) (`PAY_MANAGE_PAYROLL_LOOKUPS`)
27. [Workforce Management Lookups](workforce-management-lookups/SKILL.md) (`ORA_HWM_MANAGE_WORKFORCE_MANAGEMENT_LOOKUPS`)
28. [Manage Extended Lookup Codes](manage-extended-lookup-codes/SKILL.md) (`PER_MANAGE_EXTENDED_LOOKUP_CODE`)
29. [Manage Global Absences Lookups](manage-global-absences-lookups/SKILL.md) (`ORA_ANC_MANAGE_GLOBAL_ABSENCE_LOOKUPS`)
30. [Manage Assignment Responsibility Lookups](manage-assignment-responsibility-lookups/SKILL.md) (`PER_MANAGE_ASSIGNMENT_RESPONSIBILITY_LOOKUPS`)
31. [Manage Value Sets for Global Human Resources](manage-value-sets-for-global-human-resources/SKILL.md) (`PER_MANAGE_VALUE_SETS`)
32. [Payroll Value Sets](payroll-value-sets/SKILL.md) (`PAY_MANAGE_PAYROLL_VALUE_SETS`)
33. [Time and Labor Value Sets](time-and-labor-value-sets/SKILL.md) (`ORA_HXT_MANAGE_TIME_AND_LABOR_VALUE_SETS`)
34. [Manage Global Absences Value Sets](manage-global-absences-value-sets/SKILL.md) (`ORA_ANC_MANAGE_GLOBAL_ABSENCE_VALUE_SETS`)
35. [Manage Organization Structure Descriptive Flexfields](manage-organization-structure-descriptive-flexfields/SKILL.md) (`PER_DESC_FLEXFIELDS_FOR_HR_ENTERPRISE_STRUCTURES`)
36. [Manage Organization Structure Extensible Flexfields](manage-organization-structure-extensible-flexfields/SKILL.md) (`ORA_PER_MANAGE_ORGSTRUCTURES_EXTENSIBLE_FLEXFIELDS`)
37. [Manage Grade Descriptive Flexfields](manage-grade-descriptive-flexfields/SKILL.md) (`PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_GRADE`)
38. [Manage Workforce Structures Descriptive Flexfields](manage-workforce-structures-descriptive-flexfields/SKILL.md) (`ORA_PER_MANAGE_WORKFORCE_STRUCTURES_DESCRIPTIVE_FLEXFIELDS`)
39. [Manage Workforce Structures Extensible Flexfields](manage-workforce-structures-extensible-flexfields/SKILL.md) (`ORA_PER_MANAGE_WORKFORCE_STRUCTURES_EXTENSIBLE_FLEXFIELDS`)
40. [Manage Person Descriptive Flexfields](manage-person-descriptive-flexfields/SKILL.md) (`PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_PERSON`)
41. [Manage Person Extensible Flexfield](manage-person-extensible-flexfield/SKILL.md) (`ORA_PER_MANAGE_PERSON_EXTENSIBLE_FLEXFIELDS`)
42. [Manage Employment Descriptive Flexfields](manage-employment-descriptive-flexfields/SKILL.md) (`PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_EMPLOYMENT`)
43. [Manage Employment Extensible Flexfields](manage-employment-extensible-flexfields/SKILL.md) (`ORA_PER_MANAGE_EMPLOYMENT_EXTENSIBLE_FLEXFIELDS`)
44. [Document Records Descriptive Flexfields](document-records-descriptive-flexfields/SKILL.md) (`PER_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_DOCUMENTS`)
45. [Document Type Descriptive Flexfields](document-type-descriptive-flexfields/SKILL.md) (`ORA_DOCUMENT_TYPE_DESCRIPTIVE_FLEXFIELDS`)
46. [Descriptive Flexfields for Payroll](descriptive-flexfields-for-payroll/SKILL.md) (`PAY_MANAGE_DESCRIPTIVE_FLEXFIELDS_FOR_PAYROLL`)
47. [Extensible Flexfields for Payroll](extensible-flexfields-for-payroll/SKILL.md) (`ORA_PAY_MANAGE_EXTENSIBLE_FLEXFIELDS_FOR_PAYROLL`)
48. [Manage Audit Policies](manage-audit-policies/SKILL.md) (`FND_MANAGE_AUDIT_POLICIES`)
49. [Manage Audit Types](manage-audit-types/SKILL.md) (`ORA_GMS_MANAGE_AUDIT_TYPES`)

## Inputs

- `implementation_objective`
- `project_context`
- `payroll_common_scope`
- `payroll_common_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Track token usage for any generated project artifact or skill-run record using the manifest policy.
