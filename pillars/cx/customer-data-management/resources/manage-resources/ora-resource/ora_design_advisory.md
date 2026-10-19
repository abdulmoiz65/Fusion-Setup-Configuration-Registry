# ResourceUser Import and Export Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Oracle implementation guidance | Oracle Import Your Resource Data guide | Mapping source data, preparing the CSV, and reviewing results. |
| Oracle Export Management guidance | Oracle Export Data and Export Management Overview guides | Selecting ResourceUser fields, filters, output options, scheduling, and reviewing results. |
| Oracle post-import guidance | Oracle Reporting Hierarchy Generation and Send Pending LDAP Requests guides | Determining process eligibility and parameters. |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Record identification | Recommended | Prefer the public unique identifier and use ResourcePartyNumber for updates. | Unsupported identifier assumptions. |
| CSV preparation | Required | Map source attributes, complete prerequisites, and use the Resource Import Objects template. | Unmapped attribute values. |
| Resource role selection | Required when applicable | When Organization is supplied, map Role to ResourceOrgRoleCode. Map Role to IndividualRoleCode only when the caller explicitly identifies it as individual. | Inferred role type or role codes not defined in the environment. |
| Parent and child CSV ordering | Required when applicable | Keep a parent and its dependent resources in one CSV only when the parent row precedes every dependent row. | Reordering a child ahead of its parent. |
| Export activity design | Required | Use a unique name, filter the top-level ResourceUser object, and select only caller-requested fields. | Default party-name filters or unsupported object assumptions. |
| Export output and delivery | Optional | Explain output settings, future or recurring scheduling, split export, notification recipients, and ZIP download. | Security configuration changes. |
| Post-import ESS processing | Required when applicable | Explain that Reporting Hierarchy Generation and Send Pending LDAP Requests are independent eligible processes and can run in parallel only after fresh post-import approval. | Undocumented job-definition identifiers or direct REST payloads. |

## Output Rules

| Situation | What Happens |
|---|---|
| Source does not define an attribute contract | Mark the detail TBD. |
| User requests import advice | Explain documented mapping and prerequisite requirements. |
| User requests export advice | Explain documented filter, field-selection, output, scheduling, and ZIP result-review options. |
