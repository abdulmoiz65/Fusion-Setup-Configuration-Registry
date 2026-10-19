# Manage Sales Methods and Sales Stages Defaulting Rules

Oracle documents Common Set as a normal sales-method choice, but this workflow
does not assign it automatically. Set selection is an explicit user decision:
the requester must confirm Common Set or identify a different exact Set ID or
Set Code before the review draft can be complete.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
| --- | --- | --- | --- | --- |
| Set | User choice required; no automatic default | A new sales method has no explicit set | No |  |

## Review-Only Proposal Values

These values are synthetic drafting aids, not Oracle defaults. Use them only to
complete a proposal before user review. Never use an assumed value in an import
package until the user approves or replaces it.

| Field | Review-Only Proposal | Applies When | Override User or Baseline Value? | Requires Review? |
| --- | --- | --- | --- | --- |
| Operation | Create | No exact operation or existing update target was supplied | No | Yes |
| Sales Method Name | Enterprise Opportunity Method | No exact method name or update target was supplied | No | Yes |
| Description | Synthetic example for review | Description is blank | No | Yes |
| Close Window | 90 days | Close Window is blank | No | Yes |
| Sales Motion | Redwood | Sales motion is unspecified | No | Yes |
| Stage PhaseCd | Prospecting and Qualification: QUALIFICATION-DISCOVERY; Solution: WORKING-DEAL; Negotiation, Closed Won, and Closed No Sale: CLOSING; Closed Lost: LOST-DEAL | A synthetic stage profile is needed and no exact target-baseline or user value exists | No | Yes |
| Sales Stages | Prospecting, Qualification, Solution, Negotiation, Closed Won, Closed Lost, Closed No Sale with the complete values in the task sample | No stage design was supplied | No | Yes |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OPP.SALES_METHODS.DEFAULT | step | 2 | apply_default | applied->OPP.SALES_METHODS.DESIGN;not_applicable->OPP.SALES_METHODS.DESIGN;set_choice_missing->OPP.SALES_METHODS.RETURN_MISSING | OPP.SALES_METHODS.VALIDATE | stop | Before design validation; fill review-only proposal values by precedence, but never default Set and stop when the user has not confirmed Common Set or selected a different exact set |
