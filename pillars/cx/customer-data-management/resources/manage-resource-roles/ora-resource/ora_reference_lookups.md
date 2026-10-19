# Manage Resource Roles Reference Lookups

## REST Header Requirement

Every Fusion REST lookup in this file must include
`REST-Framework-Version: 9`, in addition to OAuth authorization and any
endpoint-specific headers.

## Lookup Operations

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| ListResourceRoles | All existing resource roles are needed | None | /crmRestApi/resources/11.13.18.05/resourceRoles | Resource role attributes returned by Oracle | Use the collection response as returned | Resource-role list | Stop and report the Fusion response |
| GetResourceRole | One existing resource role is needed | RoleCode | /crmRestApi/resources/11.13.18.05/resourceRoles/{RoleCode} | Resource role attributes returned by Oracle | Exact RoleCode path match | Resource-role detail | Stop and report not found or ambiguous input |
| GetResourceRoleType | A role type is supplied for create, update, import, or validation | Role Type or RoleTypeCode | Route to `cx.customer-data-management.resources.manage-resource-role-lookups`, which reads `JTF_RS_ROLE_TYPE` through the documented standard-lookup REST resource | Lookup codes | Exact `LookupCode` match | Validated role type | Block the role operation and direct the user to Manage Resource Role Lookups to set up the lookup code, then revalidate |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| A collection lookup is requested | Send a read-only GET to the documented resourceRoles collection endpoint |
| An item lookup is requested | Require RoleCode and send a read-only GET to the documented resourceRoles item endpoint |
| A response is empty or not found | Report the Fusion response; do not create or update a resource role |
| A role type is supplied | Use Manage Resource Role Lookups to read the `JTF_RS_ROLE_TYPE` standard lookup and accept the type only when one returned `LookupCode` exactly matches the supplied Role Type or RoleTypeCode |
| The supplied role type is not an exact active lookup code | Stop the role operation. Guide the user to set up or activate the code with Manage Resource Role Lookups; do not create, import, or update the resource role until the lookup validation passes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MRR.ROLE_TYPE_LOOKUP | decision | 3 | reference_lookup | valid->MRR.DEPENDENCIES;invalid->MRR.BLOCKED | MRR.VALIDATE | stop | A Role Type or RoleTypeCode is supplied for a resource role |
