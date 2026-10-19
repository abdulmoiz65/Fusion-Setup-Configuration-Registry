# Change Line DFF Defaults

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Context Segment Display Type | List of Values | Initial selector configuration with Display Type omitted, or an explicit request to use the skill default; the documented non-Redwood flow is not explicitly selected. Disclose this skill default, not an Oracle factory default, in the proposed configuration. An unspecified UI remains unspecified, not inferred Redwood | No. Preserve explicit values for design validation and preserve omitted existing settings on partial updates. Never apply this selector default to a Global Segment or Context Sensitive Segment | |
| Context Segment Derivation Value | PRODUCT_CONTEXT | Default Type is Parameter and Derivation Value is omitted during initial selector configuration, or the user explicitly requests this default. This is a skill proposal default, not a mandatory field or an Oracle factory default; disclose it in the preview | No. Respect an explicit alternative or request to leave it blank, subject to target validation. Preserve omitted existing values on unrelated partial updates. Never apply this selector default to child fields | |

The design resource owns UI-specific enforcement. If the user explicitly selects the documented non-Redwood flow, propose its documented Hidden setting for review rather than silently applying List of Values or switching UI. Do not default Context Code, change type, Name, Code, API Name, or individual segment Default Type/Default Value from the selector policy. This node records a proposed default, not a Fusion write.

Disable-only requests for segments or Contexts do not configure the selector and apply neither selector default. For segment disable, preserve all properties other than the selected segment's EnabledFlag. For whole-Context disable, change only the selected Context's EnabledFlag and preserve every child's flag and definition. N is the explicit disable operation, not a missing-input default.

## Task Nodes

| Rule ID | Node Type | Sequence | Action Type | Transitions | Prerequisites | On Failure | Applies When |
|---|---|---|---|---|---|---|---|
| CLDFF.DEFAULTS | step | 35 | apply_default | success->CLDFF.DESIGN;failure->CLDFF.RETURN_ISSUES | CLDFF.DEPENDENCIES | stop | Apply only eligible Context Segment Display Type and Derivation Value defaults; otherwise preserve supplied or verified existing settings |
