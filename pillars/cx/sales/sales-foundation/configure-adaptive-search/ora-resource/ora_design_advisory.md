# Adaptive Search Publish Design Advisory

## Guidance Sources

| Source Mode | Allowed Sources | When Used |
|---|---|---|
| Product behavior | [Overview of Adaptive Search Setup](https://docs.oracle.com/en/cloud/saas/sales/fassr/overview-of-adaptive-search-setup.html), [Publish a Limited Set of Objects in Adaptive Search](https://docs.oracle.com/en/cloud/saas/sales/oasal/how-to-publish-a-limited-set-of-objects-in-adaptive-search.html), and [Run and Monitor Adaptive Search Processes](https://docs.oracle.com/en/cloud/saas/sales/fassr/how-do-i-monitor-adaptive-search-background-processes.html) | Explain the purpose, Full/Partial choice, and monitoring impact of publishing |
| REST behavior | Approved Oracle internal publish/status design and release-specific validation | Explain endpoint, lifecycle, states, and known limitations |
| Repository behavior | FSCR governance and error-handling standards | Explain approval, persistence, retry, and redaction rules |

## Guidance Topics

| Topic | Advisory Level | What To Explain | Do Not Include |
|---|---|---|---|
| Object selection | Required | Requested objects are explicit while mandatory internal objects remain Fusion-determined | Claims that the request contains every effective indexed object |
| Selective-publish impact | Required | A validated object selection uses `publishType: selective`; Fusion can add mandatory internal objects and may block conflicting changes | Claims that only the visible requested objects are affected or that the publish has zero downtime |
| New-environment full-publish impact | Required only for a null or empty Entities result | The full publish initializes an environment whose object catalog is not yet available | Claims that a null or empty result proves a fully healthy configuration |
| API support boundary | Required | The publish action is internally documented and must be release-validated | Representation as a generally supported public REST contract without approval |
| Scheduling | Informational | A later internal contract supports delayed execution | Scheduling behavior in the version-one implementation |

## Output Rules

| Situation | What Happens |
|---|---|
| Product behavior is not established by an approved source | Mark it TBD and block any dependent live behavior |
| User asks for public/customer-facing guidance | State the internal-only boundary and route for publication review |
| User asks to add an object | For recognized CPQ aliases, add both direct CPQ entity names without Entities validation; otherwise call the Entities endpoint with `isDocument=true` and without `isEnabled`, validate the requested display name against `localizedName`, and map it uniquely to `entityName` only for payload construction |
