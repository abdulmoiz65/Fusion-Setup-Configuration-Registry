# Library Goal priority mapping provenance

Source: user-supplied Oracle `LibraryGoalCommonPVO.xml`, ViewObject version
14.1.2.15.16, inspected 2026-09-29. Source SHA-256:
`c1a266832a9632bf27ff0dde60d3424469c523a0ecffe66e0e932b29fcfc4cf3`.

The source package is `oracle.apps.hcm.goals.common.restModel.library.view`.
Lines 321–326 define ViewAttribute `PriorityCode`, EntityUsage `ContentItemEO`,
EntityAttrName `ItemText2`, and AliasName `ITEM_TEXT_2`. Lines 25–27 resolve
ContentItemEO to `oracle.apps.hcm.profiles.contentLibrary.model.entity.ContentItemEO`.
The priority lookup association independently uses ContentItemEO.ItemText2
(lines 29–44); the priority lookup criterion selects HRG_PRIORITY (line 981).
This is library-goal source, not the similarly named library-task view.

This establishes semantic mapping only, not current tenant metadata or values.
The resolver must still validate the physical field against the full current
ContentItem template and component metadata, reject contradictory labels or
context evidence, and read enabled/effective HRG_PRIORITY codes before use.
