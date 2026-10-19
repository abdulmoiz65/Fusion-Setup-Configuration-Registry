"""Validation profiles shared by intake and approval validation; no I/O."""
from copy import deepcopy

VERSION = "0.11.0"
MODES = ("simple", "deep")
_COMMON = {
    "local_checks": ["mandatory_fields", "hierarchy", "supported_operations", "basic_types",
                     "workbook_key_uniqueness", "payload_shape", "known_local_length_limits"],
    "environment_binding": True,
    "immutable_approval": True,
    "response_verification": True,
    "automatic_write_retry": False,
}
_LIVE = ["describe", "alert_type", "access_level", "mime_type", "language",
         "recipient_channel", "existing_alert_duplicates"]


def policy(mode):
    if mode not in MODES:
        raise ValueError("validation mode must be exactly simple or deep")
    return {**deepcopy(_COMMON), "live_preflight_checks": list(_LIVE) if mode == "deep" else [],
            "business_value_authority": "Fusion",
            "existing_item_identity_checks": "required_for_non_create_intents"}


def preflight_requests(mode, operations, execution_mode):
    """Business-value preflight only; existing-item identity gates stay on operations.

    This plan is never executed by the intake reader.
    """
    policy(mode)
    if mode == "simple":
        return []
    headers = {"REST-Framework-Version": "4" if execution_mode == "batch-create" else "9"}
    resource = "/hcmRestApi/resources/11.13.18.05/eventAlerts"
    requests = [{"resolver": "inspect_event_alert_contract", "method": "GET",
                 "path": resource + "/describe", "headers": headers, "query": {}}]
    has_templates = any(op["entity"] == "template" for op in operations)
    has_recipients = any(op["entity"] == "template_recipient" for op in operations)
    lookups = [("resolve_alert_type_code", "ORA_HRC_ALERT_TYPE"),
               ("resolve_alert_access_level", "ORA_HRC_ALERT_ACCESS_LEVEL")]
    if has_templates:
        lookups.append(("resolve_template_mime_type", "ORA_HRC_ALERT_MIME_TYPE"))
    if has_recipients:
        lookups.append(("resolve_recipient_channel_type", "ORA_HRC_ALERT_CHANNEL_TYPE"))
    for resolver, lookup_type in lookups:
        requests.append({"resolver": resolver, "method": "GET",
                         "path": "/fscmRestApi/resources/11.13.18.05/commonLookupsLOV",
                         "headers": headers, "query": {"finder": "LookupTypeFinder;LookupType=" + lookup_type,
                         "fields": "LookupCode,Meaning", "onlyData": "true"}})
    if has_templates:
        requests.append({"resolver": "resolve_template_language", "method": "GET",
                         "path": "/hcmRestApi/resources/11.13.18.05/languagesLOV", "headers": headers,
                         "query": {"finder": "ActiveLanguageFinder", "fields": "LanguageCode,Description", "onlyData": "true"}})
    for op in operations:
        if op["entity"] == "alert" and op["operation"] == "CREATE":
            requests.append({"resolver": "find_event_alert_by_code", "method": "GET", "path": resource,
                             "headers": headers, "query": {"finder": "findByAlertCode;AlertCode=" + op["payload"]["AlertCode"],
                             "fields": "AlertCode,AlertId", "onlyData": "true"}})
    return requests
