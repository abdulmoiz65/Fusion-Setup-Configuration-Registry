# Manage Email Templates Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Campaign Basic Editor DesignMetadata | Use the hardcoded minimal layout JSON below | Campaign Communication Template and Basic Editor are selected | No | |
| Campaign Advanced Block Editor DesignMetadata | Use the hardcoded minimal layout JSON below | Campaign Communication Template and Advanced Block Editor are selected | No | |
| Campaign HTML Editor defaults | Use blank `DesignMetadata`, `MessageLanguage` `US`, and `DefaultLanguageFlag` `Y` | Campaign Communication Template and HTML Editor are selected | No | |
| Campaign MessageDesignCode | Generate from the normalized template name, UTC millisecond timestamp, and Base32 nonce using the 32-character rule below | Standard Campaign template creation | No | |
| Agent-specific Advanced metadata | Do not use the TEMPLATE_FOR_REC_AGENT design as the generic Advanced Block Editor default | A standard Campaign template is created | No | |
| Express template values | TBD; a representative Express export must establish the type code and editor-specific metadata baseline | Express Communication Template is selected | No | |

## Hardcoded Campaign Creation Defaults

Use these constants only for a newly created **Campaign Communication Template**.
They do not replace the source archive values for cross-environment imports or
the fresh-export evidence required for status transitions and conflict checks.

| UI selection | DesignTypeCode | DesignEditorTypeCode | DesignMetadata | MessageLanguage | DefaultLanguageFlag |
|---|---|---|---|---|---|
| Basic | ORA_EMP_CAMP_TEMPLATE_USER | ORA_BASIC | `campaign_minimal_layout_json` | US | Y |
| Advanced Block | ORA_EMP_CAMP_TEMPLATE_USER | ORA_ADVANCED | `campaign_minimal_layout_json` | US | Y |
| HTML | ORA_EMP_CAMP_TEMPLATE_USER | ORA_HTML | blank | US | Y |

For an individual Campaign-template create, these hardcoded values are
authoritative. Obtain one fresh target export per immutable candidate and reuse
it to detect both an existing `DesignName` and `MessageDesignCode` conflict.
Do not re-export solely to generate or retry a `MessageDesignCode`. Do not compare a target template's editor metadata, language, or default-language flag with the creation defaults. Preserve source values instead
when importing an unmodified cross-environment archive or changing the status
of an existing template.

## MessageDesignCode Generation

For a new Campaign template, generate a value of at most 32 characters using:

```text
<NAME_STEM_15>_<YYMMDDHHMMSSmmm><BASE32_NONCE>
```

1. Convert `DesignName` to uppercase, replace each run of non-alphanumeric
   characters with one underscore, and trim leading or trailing underscores.
2. Take the first 15 characters as `NAME_STEM_15`.
3. Append an underscore and the current UTC timestamp in `YYMMDDHHMMSSmmm`
   format.
4. Append one random RFC 4648 Base32 character (`A-Z` or `2-7`).
5. Run `scripts/generate_message_design_code.py --name <DesignName>
   --target-export <fresh-target-fsm-export.zip>` to compare the candidate with
   every `MessageDesignCode` in the same target export already used for the
   `DesignName` check. The script tries each Base32 nonce once and fails if it
   cannot establish uniqueness before preview.
6. Use the accepted value unchanged in the parent, metadata, and type CSV rows.

For example, the name `FSCR Testing 12345` can produce
`FSCR_TESTING_12_260916140124567K`. This technical value remains internal and
is never requested from or displayed to the requester.

`campaign_minimal_layout_json`:

```json
{"backgroundColor":"#ffffff","pageColor":"#ffffff","sections":[{"id":"section_1_0_0cwv9psl","style":"","noOfColumns":1,"columnType":"a","editLock":false,"row":0,"rowIndex":0,"components":[]}]}
```
