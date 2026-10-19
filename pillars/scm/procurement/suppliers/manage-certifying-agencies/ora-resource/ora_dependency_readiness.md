# Manage Certifying Agencies Dependency Readiness

## Dependency Rules

| Dependency ID | Related Setup | Mandatory | Applies When | Status When Input Present | Status When Alternate Key Present | Status When Missing | Resolver or Workflow | Values to Fill | User Guidance |
|---|---|---|---|---|---|---|---|---|---|
| certifying_agency_identity | Certifying agency | Yes | Create or parent-only update | Satisfied | N/A | Blocked | Data Loader template | CertifyingAgency, Description | Provide CertifyingAgency directly for a parent-only PATCH; do not resolve or populate the parent CertifyingAgencyId. |
| child_patch_parent_identity | Certifying agency | Yes | Update with a child business-classification PATCH row | Satisfied | Lookup | Blocked | list_certifying_agency_candidates | CertifyingAgencyId, CertifyingAgency | Resolve the parent ID from the exact name only for the child row and child lookup. |
| business_classification_association | Supplier business classification association | Yes | Create or update | Satisfied | Lookup | Blocked | get_business_classification_lookup_code | Complete set of BusinessClassificationCode values | Provide the complete requested association set using a code or exact name for every classification. |
| existing_business_classification_association | Current child business-classification association | Yes | Update with a child PATCH row | Satisfied | Lookup | Blocked | get_existing_business_classification_associations | BusinessClassificationId, BusinessClassificationCode | Provide the existing association code or name so its current child ID can be resolved for the PATCH row. |

## Dependency Notes

- The confirmed `certifyingAgencies` Data Loader business object exposes the Business Classification child relationship. The complete approved Data Loader input is the association-state authority for this task.
- Do not infer agency-usage impact, deletion behavior, or a REST write contract. Setup-data changes route through core.data-loader.
