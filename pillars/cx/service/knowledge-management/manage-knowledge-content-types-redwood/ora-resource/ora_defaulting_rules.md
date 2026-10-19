# Content Type Defaulting Rules

## Standard Defaults

| Field | Default Value | Applies When | Override User Value? | Resolver |
|---|---|---|---|---|
| Reference Key | Application-generated from the content type name | Creating a content type | Yes | |
| Title field | Default title field | Creating a content type | Yes; the title field remains required | |
| articleGroup | ARTICLE | Creating a new content type | Yes | |
| contentSourceType | INTERNAL | Creating a new content type when the exported value is missing | Yes | |
| allowCheckOut | TRUE | Creating a new content type | Yes | |
| hasProducts | TRUE | Creating a new content type | Yes | |
| hasCategories | TRUE | Creating a new content type | Yes | |
| hasUserGroups | TRUE | Creating a new content type | Yes | |
| categoriesRequireWorkflowApproval | TRUE | Creating a new content type | Yes | |
| userGroupRequireWorkflowApproval | TRUE | Creating a new content type | Yes | |
| viewsRequireWorkflowApproval | TRUE | Creating a new content type | Yes | |
| displayDatesRequireWorkflowApproval | TRUE | Creating a new content type | Yes | |
| eventDatesRequireWorkflowApproval | TRUE | Creating a new content type | Yes | |
| restrictAuthoringToWorkflowUser | TRUE | Creating a new content type | Yes | |
| hasPriority, hasRelatedContent, hasTalkBack, isEvent, isModerated, requireAtLeastOneProduct, requireAtLeastOneCategory, requireAtLeastOneUserGroup, restrictToOneUserGroupSelection, notifyOnWorkflowApproval, notifyOnWorkflowRejection, notifyGroupOnWorkflowRejection, removeVersions, validateHtml, allowUnsafeHTMLAndJS | FALSE | Creating a new content type | Yes | |
| requireWorkflowApproval, allowPreselectedUserGroupChange, enableFullTextSearch, includeInMasterIdentifier, isRequired | TRUE | Creating a new schema attribute | Yes | |
| counter | 0 | Creating a new schema attribute | Yes | |
| counterPrefix | blank | Creating a new schema attribute | Yes | |
| isNode, allowMultipleNodes, readOnly, enableAttributeLevelSearch | FALSE | Creating a new schema attribute | Yes | |
| wysiwygType | FULL | Creating or changing an attribute whose schemaAttrType is WYSIWYG_EDIT | Yes | |
