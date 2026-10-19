# Manage External Integrations Reference Lookups

Use the live GET only for current Microsoft Teams and Slack status. Export examples are not status evidence.

## Status Lookup Source

The public [Recruiting Settings REST resource](https://docs.oracle.com/en/cloud/saas/human-resources/farws/api-recruiting-settings.html) documents the recruitingUISettings collection.

## Live Lookups

| Resolver | Runs When | Source Values | Request Path or URL | Requested Fields | Match Rule | Values to Fill | If No Match or Many Matches |
|---|---|---|---|---|---|---|---|
| get_communicate_integration_status | Current Microsoft Teams or Slack status is requested | Configured Fusion environment; ORA_HCO_MSTEAMS_ENABLED and ORA_HCO_SLACK_ENABLED | GET /hcmRestApi/resources/latest/recruitingUISettings?finder=findBySettingCodes%3BSettingCodes%3D%22ORA_HCO_MSTEAMS_ENABLED%2CORA_HCO_SLACK_ENABLED%22&onlyData=true | items.SettingCode and items.SettingValue | Match SettingCode exactly and require one row per requested integration; never use row position | Y to Enabled; N to Disabled | Report the affected integration as Unknown; do not choose an arbitrary row |

## Lookup Execution Rules

| Situation | What Happens |
|---|---|
| Status is requested | Run the GET through core.fusion-api.rest-api-client with REST-Framework-Version: 9 |
| A requested setting has one exact row with Y | Report that integration as Enabled |
| A requested setting has one exact row with N | Report that integration as Disabled |
| A row is missing, duplicated, or has another value | Report that integration as Unknown and state the observed issue |
| Both integrations are requested | Return separate Microsoft Teams and Slack results |
| The GET fails | Report the failure; do not infer status from an export or earlier result |
| Any status lookup runs | Do not call updateSettingValues, submit an import, or change configuration |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MEI.READ_STATUS | step | 2 | reference_lookup | received->MEI.EVALUATE_STATUS;failed->MEI.HANDLE_ERROR | MEI.VALIDATE_INPUT | stop | Read the requested current integration status with get_communicate_integration_status |
| MEI.EVALUATE_STATUS | decision | 3 | evaluate_result | reported->MEI.RETURN_STATUS;issues->MEI.HANDLE_ERROR | MEI.READ_STATUS | stop | Map each exact GET result to Enabled, Disabled, or Unknown |

## Public Documentation for Setting Changes

Checked 2026-09-09. Return the document matching the integration named in a setting-change request.

| Integration | Public Oracle Document | Coverage |
|---|---|---|
| Microsoft Teams | [How do I enable Microsoft Teams integration?](https://docs.oracle.com/en/cloud/saas/talent-management/fahco/how-do-i-enable-microsoft-teams-integration.html) | Public setup guidance; it does not document a whole-integration disable procedure |
| Slack | [How do I enable Slack integration?](https://docs.oracle.com/en/cloud/saas/talent-management/fahco/how-do-i-enable-slack-integration.html) | Public setup guidance; it does not document a whole-integration disable procedure |

## Export Example

Manage External Integrations_20260825_102148_993.zip is an FSM export example only. It must not be used to decide whether Microsoft Teams or Slack is currently enabled.
