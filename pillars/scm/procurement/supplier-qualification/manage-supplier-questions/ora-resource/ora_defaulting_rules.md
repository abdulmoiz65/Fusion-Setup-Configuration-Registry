# Supplier Qualification Questions Defaulting Rules

Apply these defaults before validation and preview. User-supplied values take precedence unless a rule says otherwise.

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| SupplierAttributeFlag | false | SupplierAttributeFlag is absent | No | |
| QuestionStatusCode | DRAFT | Both QuestionStatusCode and QuestionStatus are absent | No | |
| AttachmentAllowedCode | NOT_ALLOWED | Both AttachmentAllowedCode and AttachmentAllowed are absent | No | |
