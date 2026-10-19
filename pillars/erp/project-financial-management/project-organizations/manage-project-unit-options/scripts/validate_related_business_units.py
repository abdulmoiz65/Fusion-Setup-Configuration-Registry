"""Validate relationship input; Fusion FSM import validates BU eligibility."""


class RelatedBusinessUnitError(ValueError):
    def __init__(self, blockers):
        self.blockers = blockers
        self.failure_class = "input_validation"
        super().__init__("; ".join(blockers))


def validate_related_business_units(requested, receipt=None, target=None, operation="add"):
    """Return additions for Fusion validation; retain removal-safety evidence."""
    if (operation not in {"add", "remove"} or not isinstance(requested, list)
            or any(not isinstance(name, str) or not name.strip() for name in requested)
            or len(set(requested)) != len(requested)):
        raise RelatedBusinessUnitError(["Supply distinct exact business-unit names and add or remove."])
    if operation == "add":
        return [{"BusinessUnitName": name, "FusionValidationDeferred": True}
                for name in requested]
    if (not isinstance(receipt, dict) or receipt.get("Fresh") is not True
            or receipt.get("Complete") is not True or not receipt.get("EvidenceRef")
            or not target or receipt.get("TargetEnvironment") != target
            or not isinstance(receipt.get("BusinessUnits"), list)
            or any(not isinstance(row, dict) for row in receipt["BusinessUnits"])):
        raise RelatedBusinessUnitError(["Complete fresh target-bound relationship-usage evidence is required for removal."])
    blockers, resolved = [], []
    for name in requested:
        matches = [row for row in receipt["BusinessUnits"] if row.get("BusinessUnitName") == name]
        if len(matches) != 1:
            blockers.append(name + ": no unique relationship-usage record was resolved.")
            continue
        row = matches[0]
        if row.get("IsDeletable") is not True or row.get("ProjectOrTemplateUse") is not False:
            blockers.append(name + ": the relationship is used or its removability is unverified.")
            continue
        resolved.append(dict(row))
    if blockers:
        # No validated subset is returned; preserve the complete original request.
        raise RelatedBusinessUnitError(blockers)
    return resolved
