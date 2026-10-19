# ResourceUser Import and Export Defaults

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? |
|---|---|---|---|
| ResourcePartyNumber | Auto-generated | Creating a resource without a supplied public unique identifier | No |
| ResourcePartyNumber | Caller-supplied unique value | Creating a resource with a replacement public unique identifier | No |
| CX Import object code | ResourceUser | The selected task is Manage Resources, the operation is import, and no valid CX mapping CSV is supplied | No |
| Import field mapping | Automatic mapping | Source CSV headers match target object attributes | Yes |
| Export output settings | Oracle Export Management defaults | Caller does not provide an output setting | Yes |
| Export file name | Object name and timestamp in a ZIP file | Caller does not provide a file name | Yes |
| Reporting Hierarchy Tree Structure Code | RESOURCE_ORG_TREE_STRUCTURE | Reporting Hierarchy Generation is eligible for internal resources | No |
| Reporting Hierarchy Tree Code | GLOBAL_SALES_MARKETING | Reporting Hierarchy Generation is eligible for internal resources | No |
| LDAP ESS request parameters | `submit.argument1=ALL` (Oracle User Type), `submit.argument2=ALL` (required verified runtime value), `submit.argument3=A` (Oracle automatic Batch Size); all `STRING` | Send Pending LDAP Requests is eligible | No |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MR.IMPORT_DEFAULT | step | 3 | apply_default | defaulted->MR.IMPORT_VALIDATE | MR.OPERATION | stop | The selected operation is ResourceUser import. |
| MR.EXPORT_DEFAULT | step | 4 | apply_default | defaulted->MR.EXPORT_VALIDATE | MR.OPERATION | stop | The selected operation is ResourceUser export. |
