# Maintenance Program Algorithm Workflow

## Use

Read this reference before handling any `Manage Algorithms for Subscriptions to Maintenance Cloud` or companion Service Mapping request for `Subscription Maintenance Program Integration`.

This workflow is advisory. It may use the companion skill for read-only REST describe of supported Subscription Product resources to identify candidate variable names. It does not import, publish, run scheduled processes, mutate Service Mapping, or connect to Fusion for anything other than the routed describe checks permitted below.

## Mandatory Initial Inputs

Every implementer requirement must include all of the following in the same request before analysis, source recommendation, Groovy drafting, or local XML editing:

| Required Input | Required Validation | If Missing or Invalid |
|---|---|---|
| Business requirement | States the desired Maintenance program or work requirement target behavior | Ask the implementer to provide the requirement again with the attachments |
| `Algorithm_BO.xml` | File name must be exactly `Algorithm_BO.xml`; content must be for `Subscription Maintenance Program Integration`; the highest `VersionNum` must have `ActiveFlag=Y` | Reject and ask for the current valid export |
| Service Mapping source XML | File name may vary; content must have `contextName="MaintenanceProgramInterface"` | Reject and ask for a valid source copied from View Source XML |

Do not use chat cache, prior project artifacts, remembered paths, or assumptions to pass this preflight. If the implementer omits either XML, tell them both attachments are mandatory and ask them to post the requirement again with the current exports.

## Export Guidance

To obtain `Algorithm_BO.xml`:

1. Navigate to **Subscription Configuration > Dynamic Matrix Configuration > Manage Algorithms**.
2. Confirm `Subscription Maintenance Program Integration` has its highest version in in-progress state.
3. Select `Subscription Maintenance Program Integration`; do not open it.
4. Use **Actions > Export Selected**.
5. Unzip `subscriptionMaintenanceProgramIntegration.zip`.
6. Attach `Algorithm_BO.xml` with the initial requirement.

To obtain the Service Mapping source XML:

1. Navigate to **Subscription Configuration > Dynamic Matrix Configuration > Manage Service Mappings**.
2. Select `Subscription Maintenance Program Integration`; do not open it.
3. Use **Actions > View Source XML**.
4. Copy the source XML to any file name.
5. Attach that file with the initial requirement.

The Service Mapping source file is read-only evidence. Do not edit it or return a revised source XML.

## Source Resolution

After preflight passes, inspect the supplied Service Mapping source XML for relevant attributes under `CoveredAssets` or `Products`.

| Source State | Required Behavior |
|---|---|
| Required attribute is already exposed in `CoveredAssets` or `Products` | Use the exposed alias in the Groovy proposal after confirming it fits the requirement |
| Required attribute is absent from the source XML | Route to the Service Mappings companion for the supported describe lookup and source-resolution handoff; do not propose a new `_Custom` alias yet |
| Candidate is identified by describe | Return the exact source object, exact attribute name, data type, evidence source, and proposed alias; confirm the candidate with the implementer before treating it as implemented |
| Describe cannot be run, fails, or returns multiple plausible candidates | Return `needs_describe` or `needs_decision` with the missing evidence or alternatives; do not choose a source by target-field meaning alone |
| Implementer explicitly asks to proceed without describe evidence | Use the named candidate only as an assumption, mark it as not describe-confirmed, and use `<attributeName>_Custom` as the proposed Service Mapping alias |

The companion must understand the relevant object from the customer requirement. Use `Products` for product-level Subscription Product values and `CoveredAssets` or covered levels for covered asset or covered-level values.

Missing source values follow a describe-first rule: source XML is authoritative when the alias already exists; otherwise, the companion must use the permitted describe path for the relevant source object before recommending Service Mapping variables. The proposed alias should come from the exact described attribute name plus the required Service Mapping suffix or the exact alias already exposed by the current source XML, not from a guessed target-column or business-label match.

## Permitted Describe Paths

The only permitted live REST describe paths for this workflow are:

| Purpose | Describe Path |
|---|---|
| Product-level source discovery | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe` |
| Covered asset or covered-level source discovery | `/crmRestApi/resources/11.13.18.05/subscriptionProducts/describe?partialDescription=coveredLevels` |

Describe is used only to get variable names, data types, and candidate source evidence. Do not use general GET, POST, PUT, PATCH, DELETE, import, publish, or scheduled-process calls in these advisory skills.

## Groovy Drafting

Draft Groovy only after the mandatory XML inputs pass preflight and every source value is either exposed, confirmed from companion source resolution, or explicitly marked as a named assumption.

Use Service Mapping source aliases directly in `AttributeValue` whenever the source value already has the needed meaning and type and the alias is exposed in the current source XML or confirmed by the permitted describe lookup. For example, use `CoveredAssets.<exposedOrDescribeConfirmedAttribute>` or `Products.<exposedOrDescribeConfirmedAttribute>` directly instead of creating a generic helper that calls `toString()`.

Do not add blanket conversion helpers such as `toMaintenanceAttributeValue` or generic `.toString()` wrapping around all source values. Only apply an explicit conversion, concatenation, or date format when the requirement itself needs it or a documented runtime contract requires it. For example, program code composition may use `'OSS' + Products.SubscriptionProductId`, while date fields should normally receive the confirmed date alias directly.

Use `ProgramInterface.insert` with this shape:

```groovy
ProgramInterface.insert([
    AttributeName: '<column name from MNT_PROGRAMS_INT or MNT_WORK_REQUIREMENTS_INT>',
    AttributeValue: <hardcoded value, derived value, CoveredAssets value, or Products value>,
    SourceId: CoveredAssets.CoveredLevelId,
    AttributeContext: '<PGM or WR>'
])
```

Set `AttributeContext` from the target table:

| Target Table | AttributeContext |
|---|---|
| `MNT_PROGRAMS_INT` | `PGM` |
| `MNT_WORK_REQUIREMENTS_INT` | `WR` |

Validate every `AttributeName` against the task target references before drafting:

- `MNT_PROGRAMS_INT`: `references/ora_mnt_programs_int_reference.md`
- `MNT_WORK_REQUIREMENTS_INT`: `references/ora_mnt_work_requirements_int_reference.md`

Do not infer a Subscription source alias from a Maintenance target column. Source aliases must come from the current Service Mapping XML, a confirmed companion describe result, or a named no-describe assumption explicitly accepted by the implementer.

## Approval and Local XML Update

For any new or changed implementer requirement, present the complete draft Groovy to the implementer for approval before editing any local XML or generating any `Algorithm_BO.xml` artifact. The first artifact for a change must be a Groovy proposal or equivalent approval draft, not an updated XML file.

Stop after presenting the draft Groovy unless the current user message is an explicit approval of a previously presented exact draft. Do not combine first-time Groovy drafting and `Algorithm_BO.xml` generation in the same response, even when the XML and source mapping exports are available.

Approval must be bound to the exact Groovy body or named proposal artifact. If the Groovy changes after approval, request approval again before generating or updating `Algorithm_BO.xml`.

After explicit approval of that exact Groovy:

1. Edit only the highest `VersionNum` whose `ActiveFlag=Y` in `Algorithm_BO.xml`.
2. Inspect the selected action's current `ActionExpression` before writing the approved Groovy.
3. If the current `ActionExpression` already contains executable Groovy, append the approved Groovy after the existing executable logic and preserve the existing statement order.
4. If the current `ActionExpression` is blank, placeholder text, sample text, or comment-only content such as `//...` or `/*...*/`, ignore or remove that non-executable content and write only the approved Groovy.
5. Do not treat comments as existing logic, and do not retain comments merely to preserve delivered sample text.
6. Keep the resulting `ActionExpression` valid Groovy and XML-safe.
7. Preserve unrelated versions, actions, metadata, and Service Mapping source XML.
8. Provide the updated local `Algorithm_BO.xml` for the implementer to import manually.
9. Tell the implementer to import the file from the same Manage Algorithms page.

Do not create a Fusion import, run an import, publish, or execute runtime validation from this skill.

## Service Mapping Steps for Unresolved or Assumed Sources

When the Groovy proposal uses a source that is not already present in the supplied Service Mapping source XML, provide the implementer these manual Service Mapping steps for each describe-confirmed but unexposed source or each explicitly approved no-describe assumption:

1. Enter a sandbox with **Manage Service Mappings** available.
2. Navigate to **Subscription Configuration > Dynamic Matrix Configuration > Manage Service Mappings**.
3. In the relevant entity, `CoveredAssets` or `Products`, create the attribute using the selected alias from the exact described attribute name, or the explicitly approved assumed `<attributeName>_Custom` alias, and the confirmed or assumed data type.
4. In **Sources** under the respective entity object, map it to the selected source attribute under the respective source.
5. In **Services** for the respective source, add read permissions as needed.

Return these steps with the final handoff whenever any source was assumed, uncreated, unexposed, or unpublished.
