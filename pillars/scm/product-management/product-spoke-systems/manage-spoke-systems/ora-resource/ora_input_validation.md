# Manage Spoke Systems Input Validation

## Source and Scope

Source: the latest developer instruction makes spokeSystemCode mandatory and requires an error when it is not provided. Earlier requests distinguish Import Options from Publication Options, and request Effective Date, Item Structure Name, Include digital asset files, and Attachment Categories. UI screenshots do not establish REST enums or writable field names. Customer values are not reusable defaults.

The user requested removal of the incomplete rules. This resource now validates only mandatory input presence. Passing it does not verify that the code exists in Fusion or validate an options payload. The invoking runbook and core.data-loader retain responsibility for live metadata validation, record identity, artifact preparation, approval, and submission.

## Required Groups

| Requirement Group | Accepted Fields | If Missing | How to Resolve | Applies When | Resolver |
|---|---|---|---|---|---|
| Source system identity | spokeSystemCode (mandatory) | Show error: spokeSystemCode is mandatory. Please provide spokeSystemCode. Stop validation before lookups, preview, or submission. | Ask the user to provide spokeSystemCode; do not substitute Name or a record ID | Every options update | |

## Field Validation

| Check | What Happens | Applies When | Resolver |
|---|---|---|---|
| Mandatory spokeSystemCode | If spokeSystemCode is absent, null, empty, or whitespace-only, show error: spokeSystemCode is mandatory. Please provide spokeSystemCode. Return failed and stop; a supplied value passes this mandatory-input check only. | Every options update; evaluate first | |

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| MSS.VALIDATE_INPUT | decision | 10 | validate_input | passed->MSS.DONE;failed->MSS.HANDLE_ISSUE | none | stop | A Manage Spoke Systems options update is requested |
