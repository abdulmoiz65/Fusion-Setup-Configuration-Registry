# Schedule Generation Profile Error Handling

## Error Situations

| Situation | What Should Happen |
|---|---|
| Required input is missing or invalid | Identify the field and stop before execution. |
| Latest profile or child state cannot be uniquely resolved before an update | Stop before generating an update archive. Show the unmatched or ambiguous business identity and request correction or selection. |
| Lookup returns no or multiple results | Show candidates and require explicit user selection. |
| Lookup contract is TBD | Stop and request the source-proved resolver contract. |
| Fusion rejects a Boolean value serialized as True or False | Correct every generated Boolean value to the lowercase literal true or false, regenerate and revalidate the complete immutable artifact, and require fresh approval before retry. |
| Self-scheduling rotation is enabled without both required window values | Stop before execution. Require SelfScheduledOpens and SelfScheduledEnds, with each value 0 or greater. |
| Fusion reports Enter at least 1 self-scheduling rotation, or disable self-scheduling rotations (HTS-1680256) | Do not retry unchanged. Add at least one selfSchedulingRotations child row together with both required self-scheduling window values, or set SelfSchedRotationEnabledFlag to false. Regenerate, revalidate, and require fresh approval before retry. |
| Fusion reports Enter a start time deviation, end time deviation, or both | Do not retry. When DeviationAllowTimeFlag is true, provide DeviationAllowStartMinutes, DeviationAllowEndMinutes, or both. Do not substitute StartEarlyPeriod, StartLatePeriod, EndEarlyPeriod, or EndLatePeriod. |
| A deferred Condition Builder group value is supplied | Ignore the value and explain that it is unavailable until Condition Builder uptake. |
| Complete Summary cannot be generated solely from verified structured values | Stop before provider-owned approval; correct the structured values or summary contract without exposing technical values to the user. |
| Approved execution route fails | Preserve the returned reference and stop before retry. |
| The create duplicate check finds an exact existing configuration | Show the matching profile name and reference code plus business-only comparison evidence. Ask whether the user still wants to create a separate profile. Stop until an explicit contextual yes or no is received. Do not run this prompt for an explicit duplicate operation. |
| The create duplicate check cannot retrieve or compare every relevant parent or child value | Treat the result as uncertain and stop before approval or creation. Do not create the profile or treat a partial comparison as unique. |
| A status request reports a failed, active, unavailable, or uncertain Data Loader result | Return the complete Data Loader status report, every available actionable error, and its next action. Do not render a profile success summary or claim that any requested operation completed. |
| A successful terminal status cannot verify the requested profile operation | Treat the outcome as uncertain. Report the verification issue and do not render a profile success summary. |

## Post-Status Profile Summary

For a successful terminal Data Loader status with no diagnostics, use
`verify_completed_schedule_profile_operation` to read back the target before
claiming that it was created, updated, deleted, or duplicated. Append the
following business-only section after the unchanged Data Loader status report.

## Profile Summary

| Business Setting | Verified Value |
|---|---|
| Operation | Created, Updated, Deleted, or Duplicated |
| <business label> | <verified business display value> |

For create, update, and duplicate, include the verified profile name,
effective dates, status, and every populated business child section. For
delete, include the retained pre-operation profile name and state that the
exact profile was verified as deleted. Use business labels and display values
only; omit IDs, codes, request identifiers, REST or API details, loader-file
details, diagnostics, and technical notes.

## Error Classifications

| Result Category | When Used | Next Action |
|---|---|---|
| MISSING | Required information is absent | Request the missing value. |
| FAILED | Validation, lookup, or workflow failure | Report the failure and stop. |
| BLOCKED | A required source contract is TBD | Request the missing contract. |

## Refusal Rules

| Situation | What Must Not Happen |
|---|---|
| Lookup has no exact match | Do not select the nearest candidate automatically. |
| A mutation has failed or is uncertain | Do not retry automatically. |
| An update has not refreshed the current parent and relevant children | Do not reuse a prior DAT, workbook, local input, or child identifiers from chat history. |
| A Complete Summary is not ready | Do not begin the provider-owned approval process or expose internal values, diagnostics, or technical notes. |
| The selected execution route is not approved | Do not call a direct REST write endpoint. |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| SGP.EXECUTION_GATE | step | 20 | execution_gate | ready->SGP.DONE;blocked->SGP.ERROR | SGP.COMPLETE_SUMMARY | stop | After the Complete Summary and before the unchanged provider-owned approval process and approved execution route |
| SGP.ERROR | step | 21 | error_handler | handled->SGP.RETURN_ERROR | none | stop | A preceding node reports an error or blocker |
| SGP.RETURN_ERROR | terminal | 22 | terminal | none | none | stop | An error or blocker was handled |
| SGP.DONE | terminal | 23 | terminal | none | SGP.EXECUTION_GATE | stop | The execution gate is ready |
