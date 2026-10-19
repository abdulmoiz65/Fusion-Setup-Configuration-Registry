---
skill_id: "cx.customer-data-management.trading-community-foundation"
name: "Trading Community Foundation Implementation Guidance"
description: "Provides CX Customer Data Management implementation guidance for the Trading Community Foundation functional area."
layer: "pillar"
pillar: "CX"
offering: "Customer Data Management"
functional_area: "Trading Community Foundation"
functional_area_code: "ORA_HZ_CDM_FOUNDATION"
type: "planning"
execution_mode: "assisted"
owner_team: "CX customer data management pillar team"
version: "0.1.0"
inputs:
  - "implementation_objective"
  - "project_context"
  - "trading_community_foundation_scope"
  - "trading_community_foundation_requirements"
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
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "configuration_blueprint"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "design_decision"
    default_location: "project/{project_id}/decisions/"
    versioning_policy: "append-only"
  - artifact_type: "validation_result"
    default_location: "project/{project_id}/artifacts/pillars/cx/customer-data-management/trading-community-foundation/current/"
    versioning_policy: "major-new-version-minor-confirm-update"
  - artifact_type: "skill_run"
    default_location: "project/{project_id}/state/runs/"
    versioning_policy: "append-only"
  - artifact_type: "token_usage_record"
    default_location: "project/{project_id}/artifacts/shared/token-usage/current/token-usage-log.md"
    versioning_policy: "append-only"
required_setup_tasks:
  - "HZ_MANAGE_TRADING_COMMUNITY_SOURCE_SYSTEMS"
  - "HZ_MANAGE_SOURCE_SYSTEM_ENTITIES"
  - "HZ_MANAGE_SOURCE_SYSTEM_LOOKUPS"
  - "HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS"
  - "HZ_MANAGE_PARTY_USAGE_LOOKUPS"
  - "HZ_MANAGE_CONTACT_POINT_LOOKUPS"
  - "HZ_MANAGE_TRADING_COMMUNITY_ORGANIZATION_LOOKUPS"
  - "HZ_MANAGE_TRADING_COMMUNITY_LOCATION_LOOKUPS"
  - "HZ_MANAGE_TRADING_COMMUNITY_PERSON_LOOKUPS"
  - "HZ_MANAGE_CONTACT_LOOKUPS"
  - "HZ_MANAGE_CUSTOMER_ACCOUNT_LOOKUPS"
  - "HZ_MANAGE_IMPORT_LOOKUPS"
  - "HZ_MANAGE_GROUP_LOOKUPS"
  - "HZ_MANAGE_RELATIONSHIP_LOOKUPS"
  - "HZ_MANAGE_DATA_STYLES"
  - "HZ_MANAGE_NAME_FORMATS"
  - "HZ_MANAGE_ADDRESS_FORMATS"
  - "HZ_MANAGE_HIERARCHY_TYPES"
  - "HZ_MANAGE_HIERARCHY_LABELS"
  - "ORA_HZ_MANAGE_DOCUMENT_SEQUENCES"
  - "HZ_MANAGE_PARTY_USAGE_FILTER_RULES"
  - "HZ_MANAGE_RELATIONSHIP_GROUPS"
  - "HZ_MANAGE_CLASSIFICATION_CATEGORIES"
  - "HZ_RUN_PARTY_HIERARCHY_GENERATION"
  - "HZ_MANAGE_ADDITIONAL_NAME_TYPES"
  - "HZ_RUN_TRADING_COMM_CURRENT_RECORD_INFO_MAINTENANCE"
  - "HZ_IMPORT_PARTNERS"
  - "FND_MANAGE_AUDIT_POLICIES"
  - "HZ_MANAGE_PARTY_USAGES"
  - "ORA_HZ_MANAGE_TREE_STRUCTURES"
  - "HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES"
  - "HZ_MANAGE_RELATIONSHIP_TYPES"
  - "HZ_MANAGE_CLASSIFICATION_GROUPS"
  - "HZ_RUN_HIERARCHY_AUDIT"
  - "HZ_RUN_CLASSIFICATION_HIERARCHY_GENERATION"
  - "HZ_MANAGE_TELEPHONE_NUMBERING_PLANS"
  - "ORA_HZ_MANAGE_MESSAGES"
  - "HZ_MANAGE_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_SOURCE_SYSTEM_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_CONTACT_POINT_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_TRADING_COMMUNITY_ORGANIZATION_DESC_FLEXFIELDS"
  - "HZ_TRADING_COMMUNITY_ORGANIZATION_SITE_DESC_FLEXFIELDS"
  - "HZ_MANAGE_TRADING_COMMUNITY_LOCATION_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_TRADING_COMMUNITY_PERSON_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_TRADING_COMMUNITY_PERSON_SITE_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_CONTACT_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_CUSTOMER_ACCOUNT_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_CUSTOMER_ACCOUNT_SITE_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_CUSTOMER_ACCOUNT_SITE_USE_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_CUSTOMER_ACCOUNT_CONTACT_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_CUSTOMER_ACCOUNT_CONTACT_ROLE_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS"
  - "HZ_MANAGE_DATA_FORMAT_PROFILE_OPTIONS"
  - "HZ_MANAGE_TRADING_COMMUNITY_COMMON_PROFILE_OPTIONS"
  - "HZ_MANAGE_TRADING_COMMUNITY_LOCATION_PROFILE_OPTIONS"
  - "HZ_MANAGE_TRADING_COMMUNITY_PERSON_PROFILE_OPTIONS"
  - "HZ_MANAGE_CUSTOMER_ACCOUNT_PROFILE_OPTIONS"
  - "HZ_MANAGE_IMPORT_PROFILES"
  - "ZCA_MANAGE_CALENDAR_PROFILE_OPTION"
  - "ZCA_MANAGE_CURRENCY_PROFILE_OPTIONS"
  - "ZCA_MANAGE_WAREHOUSE_ENABLE_PROFILE"
  - "ZCA_MANAGE_PUBLIC_UNIQUE_IDENTIFIER_PROFILE_OPTIONS"
  - "HZ_MANAGE_HIERARCHIES"
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

# Trading Community Foundation Implementation Guidance

## Purpose

Provides CX Customer Data Management implementation guidance for the Trading Community Foundation functional area.

## When to Use

Use this functional-area skill after Customer Data Management scope is confirmed and the project needs trading community foundation setup planning, baseline export, import sequencing, or validation checkpoints.

## Catalog Metadata

- Pillar: `CX`
- Offering: `Customer Data Management` (`ZCH_CDM`)
- Functional area / Setup Object: `Trading Community Foundation` (`ORA_HZ_CDM_FOUNDATION`)
- Effective task catalog: `knowledge/setup-task-catalog/effective/setupTasksAll.json`
- Effective hierarchy catalog: `knowledge/setup-task-catalog/effective/offering-functional-area-task-catalog.json`
- Provenance composition: `release - pre_release.removals + pre_release.items + custom.items`
- Source catalogs: release `setupTasksAll.json`, pre-release supplement, and custom `setupTasksAll.json`
- Exact occurrence flags for tasks 1-23 below: Available `Y`, export/import `Y`, CSV export/import `Y`
- Party hierarchy generation flags: Available `Y`, export/import `N`, CSV export/import `N`

## Setup Tasks

1. [Manage Trading Community Source Systems](manage-trading-community-source-systems/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_SOURCE_SYSTEMS`)
2. [Manage Source System Entities](manage-source-system-entities/SKILL.md) (`HZ_MANAGE_SOURCE_SYSTEM_ENTITIES`)
3. [Manage Source System Lookups](manage-source-system-lookups/SKILL.md) (`HZ_MANAGE_SOURCE_SYSTEM_LOOKUPS`)
4. [Manage Trading Community Common Lookups](manage-trading-community-common-lookups/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_COMMON_LOOKUPS`)
5. [Manage Party Usage Lookups](manage-party-usage-lookups/SKILL.md) (`HZ_MANAGE_PARTY_USAGE_LOOKUPS`)
6. [Manage Contact Point Lookups](manage-contact-point-lookups/SKILL.md) (`HZ_MANAGE_CONTACT_POINT_LOOKUPS`)
7. [Manage Trading Community Organization Lookups](manage-trading-community-organization-lookups/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_ORGANIZATION_LOOKUPS`)
8. [Manage Trading Community Location Lookups](manage-trading-community-location-lookups/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_LOCATION_LOOKUPS`)
9. [Manage Trading Community Person Lookups](manage-trading-community-person-lookups/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_PERSON_LOOKUPS`)
10. [Manage Contact Lookups](manage-contact-lookups/SKILL.md) (`HZ_MANAGE_CONTACT_LOOKUPS`)
11. [Manage Customer Account Lookups](manage-customer-account-lookups/SKILL.md) (`HZ_MANAGE_CUSTOMER_ACCOUNT_LOOKUPS`)
12. [Manage Import Lookups](manage-import-lookups/SKILL.md) (`HZ_MANAGE_IMPORT_LOOKUPS`)
13. [Manage Group Lookups](manage-group-lookups/SKILL.md) (`HZ_MANAGE_GROUP_LOOKUPS`)
14. [Manage Relationship Lookups](manage-relationship-lookups/SKILL.md) (`HZ_MANAGE_RELATIONSHIP_LOOKUPS`)
15. [Manage Data Styles](manage-data-styles/SKILL.md) (`HZ_MANAGE_DATA_STYLES`)
16. [Manage Name Formats](manage-name-formats/SKILL.md) (`HZ_MANAGE_NAME_FORMATS`)
17. [Manage Address Formats](manage-address-formats/SKILL.md) (`HZ_MANAGE_ADDRESS_FORMATS`)
18. [Manage Hierarchy Types](manage-hierarchy-types/SKILL.md) (`HZ_MANAGE_HIERARCHY_TYPES`)
19. [Manage Hierarchy Labels](manage-hierarchy-labels/SKILL.md) (`HZ_MANAGE_HIERARCHY_LABELS`)
20. [Manage Trading Community Document Sequences](manage-trading-community-document-sequences/SKILL.md) (`ORA_HZ_MANAGE_DOCUMENT_SEQUENCES`)
21. [Manage Party Usage Filter Rules](manage-party-usage-filter-rules/SKILL.md) (`HZ_MANAGE_PARTY_USAGE_FILTER_RULES`)
22. [Manage Relationship Groups](manage-relationship-groups/SKILL.md) (`HZ_MANAGE_RELATIONSHIP_GROUPS`)
23. [Manage Classification Categories](manage-classification-categories/SKILL.md) (`HZ_MANAGE_CLASSIFICATION_CATEGORIES`)
24. [Run Trading Community Party Hierarchy Generation](run-trading-community-party-hierarchy-generation/SKILL.md) (`HZ_RUN_PARTY_HIERARCHY_GENERATION`)
25. [Manage Additional Name Types](manage-additional-name-types/SKILL.md) (`HZ_MANAGE_ADDITIONAL_NAME_TYPES`)
26. [Run Trading Community Current Record Information Maintenance](run-trading-community-current-record-information-maintenance/SKILL.md) (`HZ_RUN_TRADING_COMM_CURRENT_RECORD_INFO_MAINTENANCE`)
27. [Manage Party Usages](manage-party-usages/SKILL.md) (`HZ_MANAGE_PARTY_USAGES`)
28. [Manage Classification Groups](manage-classification-groups/SKILL.md) (`HZ_MANAGE_CLASSIFICATION_GROUPS`)
29. [Audit Trading Community Party Hierarchy](audit-trading-community-party-hierarchy/SKILL.md) (`HZ_RUN_HIERARCHY_AUDIT`)
30. [Run Classification Hierarchy Generation](run-classification-hierarchy-generation/SKILL.md) (`HZ_RUN_CLASSIFICATION_HIERARCHY_GENERATION`)
31. [Manage Phone Numbering Plans](manage-phone-numbering-plans/SKILL.md) (`HZ_MANAGE_TELEPHONE_NUMBERING_PLANS`)
32. [Manage Trading Community Messages](manage-trading-community-messages/SKILL.md) (`ORA_HZ_MANAGE_MESSAGES`)
33. [Manage Relationship Descriptive Flexfields](manage-relationship-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS`)
34. [Manage Source System Descriptive Flexfields](manage-source-system-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_SOURCE_SYSTEM_DESCRIPTIVE_FLEXFIELDS`)
35. [Manage Contact Point Descriptive Flexfields](manage-contact-point-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_CONTACT_POINT_DESCRIPTIVE_FLEXFIELDS`)
36. [Manage Trading Community Organization Descriptive Flexfields](manage-trading-community-organization-descriptive-flexfields/SKILL.md) (`HZ_TRADING_COMMUNITY_ORGANIZATION_DESC_FLEXFIELDS`)
37. [Manage Trading Community Organization Site Descriptive Flexfields](manage-trading-community-organization-site-descriptive-flexfields/SKILL.md) (`HZ_TRADING_COMMUNITY_ORGANIZATION_SITE_DESC_FLEXFIELDS`)
38. [Manage Trading Community Location Descriptive Flexfields](manage-trading-community-location-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_LOCATION_DESCRIPTIVE_FLEXFIELDS`)
39. [Manage Trading Community Person Descriptive Flexfields](manage-trading-community-person-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_PERSON_DESCRIPTIVE_FLEXFIELDS`)
40. [Manage Trading Community Person Site Descriptive Flexfields](manage-trading-community-person-site-descriptive-flexfields/SKILL.md) (`HZ_TRADING_COMMUNITY_PERSON_SITE_DESCRIPTIVE_FLEXFIELDS`)
41. [Manage Contact Descriptive Flexfields](manage-contact-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_CONTACT_DESCRIPTIVE_FLEXFIELDS`)
42. [Manage Customer Account Descriptive Flexfields](manage-customer-account-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_CUSTOMER_ACCOUNT_DESCRIPTIVE_FLEXFIELDS`)
43. [Manage Customer Account Site Descriptive Flexfields](manage-customer-account-site-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_CUSTOMER_ACCOUNT_SITE_DESCRIPTIVE_FLEXFIELDS`)
44. [Manage Customer Account Site Use Descriptive Flexfields](manage-customer-account-site-use-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_CUSTOMER_ACCOUNT_SITE_USE_DESCRIPTIVE_FLEXFIELDS`)
45. [Manage Customer Account Contact Descriptive Flexfields](manage-customer-account-contact-descriptive-flexfields/SKILL.md) (`HZ_MANAGE_CUSTOMER_ACCOUNT_CONTACT_DESCRIPTIVE_FLEXFIELDS`)
46. [Manage Customer Account Contact Role Descriptive Flexfields](manage-customer-account-contact-role-descriptive-flexfields/SKILL.md) (`HZ_CUSTOMER_ACCOUNT_CONTACT_ROLE_DESCRIPTIVE_FLEXFIELDS`)
47. [Manage Customer Account Relationship Descriptive Flexfields](manage-customer-account-relationship-descriptive-flexfields/SKILL.md) (`HZ_CUSTOMER_ACCOUNT_RELATIONSHIP_DESCRIPTIVE_FLEXFIELDS`)
48. [Manage Data Format Profile Options](manage-data-format-profile-options/SKILL.md) (`HZ_MANAGE_DATA_FORMAT_PROFILE_OPTIONS`)
50. [Manage Trading Community Common Profile Options](manage-trading-community-common-profile-options/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_COMMON_PROFILE_OPTIONS`)
51. [Manage Trading Community Location Profile Options](manage-trading-community-location-profile-options/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_LOCATION_PROFILE_OPTIONS`)
52. [Manage Trading Community Person Profile Options](manage-trading-community-person-profile-options/SKILL.md) (`HZ_MANAGE_TRADING_COMMUNITY_PERSON_PROFILE_OPTIONS`)
53. [Manage Customer Account Profile Options](manage-customer-account-profile-options/SKILL.md) (`HZ_MANAGE_CUSTOMER_ACCOUNT_PROFILE_OPTIONS`)
54. [Manage Import Profile Options](manage-import-profile-options/SKILL.md) (`HZ_MANAGE_IMPORT_PROFILES`)
55. [Manage Calendar Profile Option](manage-calendar-profile-option/SKILL.md) (`ZCA_MANAGE_CALENDAR_PROFILE_OPTION`)
56. [Manage Currency Profile Options](manage-currency-profile-options/SKILL.md) (`ZCA_MANAGE_CURRENCY_PROFILE_OPTIONS`)
57. [Manage Data Warehouse Profile Option](manage-data-warehouse-profile-option/SKILL.md) (`ZCA_MANAGE_WAREHOUSE_ENABLE_PROFILE`)
58. [Manage Public Unique Identifier Profile Options](manage-public-unique-identifier-profile-options/SKILL.md) (`ZCA_MANAGE_PUBLIC_UNIQUE_IDENTIFIER_PROFILE_OPTIONS`)
59. [Manage Trading Community Tree Structures](manage-trading-community-tree-structures/SKILL.md) (`ORA_HZ_MANAGE_TREE_STRUCTURES`)
60. [Manage Additional Identifier Types](manage-additional-identifier-types/SKILL.md) (`HZ_MANAGE_ADDITIONAL_IDENTIFIER_TYPES`)
61. [Manage Relationship Types](manage-relationship-types/SKILL.md) (`HZ_MANAGE_RELATIONSHIP_TYPES`)
62. [Manage Hierarchies](manage-hierarchies/SKILL.md) (`HZ_MANAGE_HIERARCHIES`)

## Inputs

- `implementation_objective`
- `project_context`
- `trading_community_foundation_scope`
- `trading_community_foundation_requirements`

## Outputs

- `functional_area_setup_plan`
- `configuration_guidance`
- `validation_checkpoints`
- `skill_run_record`
- `token_usage_record`

## Implementation Notes

Use the generated nested setup-task skills for task-level planning, sequencing, setup-data routing, and validation. Use `Manage Address Formats` for its task-specific whole-package migration and validation routing. Add task representations only through the catalog-backed pillar skill generator. Track token usage for any generated project artifact or skill-run record using the manifest policy.
