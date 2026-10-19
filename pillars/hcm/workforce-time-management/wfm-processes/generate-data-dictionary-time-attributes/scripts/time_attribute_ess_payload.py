"""Build the verified ESS payload for Generate Data Dictionary Time Attributes.

This module owns only task-specific Scheduler facts and parameter validation.
Submission and monitoring remain with core.fusion-api.ess-job-submitter.
"""

from __future__ import annotations

from typing import Any


class PayloadValidationError(ValueError):
    """Raised when task-owned ESS inputs cannot form a safe payload."""


TIME_ATTRIBUTE_JOB_DEFINITION_ID = (
    "JobDefinition://oracle/apps/ess/hcm/wfm/repositoryDataDictionary/"
    "TimeAttributeFieldGenerationJob"
)
TIME_ATTRIBUTE_APPLICATION = "EarHcmEss"
TIME_ATTRIBUTE_PRODUCT = "HCM"
INCLUDE_PAYROLL_TIME_TYPE_DEFAULT = "Y"
INCLUDE_PAYROLL_TIME_TYPE_VALUES = frozenset({"Y", "N"})
LEGISLATIVE_DATA_GROUP_SCOPES = frozenset({"all", "specific"})


def _parameter(name: str, value: str) -> dict[str, str]:
    return {"name": name, "paramType": "STRING", "value": value}


def build_time_attribute_ess_payload(
    *,
    include_payroll_time_type: str | None = None,
    legislative_data_group_scope: str | None = None,
    legislative_data_group_id: str | int | None = None,
    description: str = "Generate Data Dictionary Time Attributes",
) -> dict[str, Any]:
    """Build the task-owned immediate ESS request body.

    ``legislative_data_group_scope`` records the user's explicit choice of
    ``all`` LDGs or one ``specific`` LDG. For ``all``, argument 4 is omitted.
    For ``specific``, ``legislative_data_group_id`` must already be the ID
    resolved from the current environment's legislativeDataGroupsLOV response.
    """
    payroll_value = INCLUDE_PAYROLL_TIME_TYPE_DEFAULT if include_payroll_time_type is None else include_payroll_time_type
    if payroll_value not in INCLUDE_PAYROLL_TIME_TYPE_VALUES:
        raise PayloadValidationError("include_payroll_time_type must be Y or N")
    if not isinstance(description, str) or not description.strip():
        raise PayloadValidationError("description must be a non-empty string")
    if legislative_data_group_scope not in LEGISLATIVE_DATA_GROUP_SCOPES:
        raise PayloadValidationError(
            "legislative_data_group_scope must be an explicit 'all' or 'specific' selection"
        )
    if legislative_data_group_scope == "all" and legislative_data_group_id is not None:
        raise PayloadValidationError(
            "legislative_data_group_id must be omitted when legislative_data_group_scope is 'all'"
        )
    if legislative_data_group_scope == "specific" and legislative_data_group_id is None:
        raise PayloadValidationError(
            "legislative_data_group_id is required when legislative_data_group_scope is 'specific'"
        )

    parameters = [_parameter("submit.argument1", payroll_value)]
    if legislative_data_group_scope == "specific":
        if isinstance(legislative_data_group_id, bool) or str(legislative_data_group_id).strip() == "":
            raise PayloadValidationError("legislative_data_group_id must be a resolved non-empty ID")
        parameters.append(_parameter("submit.argument4", str(legislative_data_group_id)))

    return {
        "description": description,
        "jobDefinitionId": TIME_ATTRIBUTE_JOB_DEFINITION_ID,
        "application": TIME_ATTRIBUTE_APPLICATION,
        "product": TIME_ATTRIBUTE_PRODUCT,
        "requestParameters": parameters,
    }
