# Benefit Groups Input Validation

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Requested operation | Create, Read/verify, Update, or Delete | Block the request before preview or execution | Supply one supported operation | Every request | |
| HDL artifact | A nonempty immutable Benefit Groups HDL artifact validated by core.data-loader | Block Create, Update, or Delete before approval | Generate or validate the artifact through core.data-loader | Create, Update, or Delete | |
| Target context | Exact target environment and active Run Book context | Block a side-effecting request | Select the target and activate the project Run Book through the routed workflow | Create, Update, or Delete | |
| Create identity | BenefitGroupName, maximum 240 characters | Block Create before preview or execution | Supply a nonblank unique BenefitGroupName | Create | |

## Dependency-Aware Validation

| Applies When | Result | Next Action | Resolver |
|---|---|---|---|
| A request changes Benefit Groups data | Continue only when the HDL artifact, target environment, and active Run Book context are present | Continue to dependency readiness checks | |
| A benefitGroups row supplies LegalEmployer | Validate that row's value through the selected legalEmployersLov resolver | Record valid, invalid, ambiguous, or unverified_forbidden for that row and field | |
| The LegalEmployer lookup returns 403 | Do not fail field validation or mark the value invalid; record unverified_forbidden | Continue independent checks; retain the unverified status for load readiness | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| HDL business object | Require benefitGroups; reject the Benefit Groups task display name as a DAT object identifier | Every request | |
| Operation value | Reject an operation outside Create, Read/verify, Update, or Delete | Every request | |
| Artifact integrity | Reject an empty, changed, malformed, or unvalidated artifact | Create, Update, or Delete | |
| Create key | Require BenefitGroupName for a create record; it is the current user-key alternative to BenefitGroupId | Create | |
| Rest action | Require RestAction; use POST for Create | Create | |
| Optional description | Reject BenefitGroupDescription longer than 240 characters when supplied | Create or Update | |
| Optional legal-employer reference | When supplied, validate LegalEmployer as a string of at most 240 characters or LegalEntityId as a string of at most 18 characters; do not infer either value | Create or Update | |
| LegalEmployer lookup | When LegalEmployer is supplied, require an exact Name match from legalEmployersLov through the selected read-only REST client; skip this name lookup when only LegalEntityId is supplied | Any included benefitGroups row with LegalEmployer | |
| Update and delete identity | Require the object user keys required by the live HDL schema; do not infer missing identity values | Update or Delete | |
| CSV route | Reject CSV export/import as a substitute route because catalog support is N | Every request that proposes CSV export/import | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| BEN_GRP.VALIDATE_REQUEST | decision | 10 | validate_input | valid->BEN_GRP.APPLY_DEFAULTS;invalid->BEN_GRP.HANDLE_ISSUE | none | stop | Validate the requested operation, artifact, target context, identity, and unsupported CSV route |
