"""CPQ live checks and write callbacks; approval remains owned by the durable guard.

Adapted from the supplied CPQ candidate. No terminal approval, replacement
approval authority, mutation retry, or generic Core global patch is introduced.
"""
from __future__ import annotations

from pathlib import Path
import urllib.parse
import urllib.request
import urllib.error

import cpq_approval_contract as contract
import cpq_live_contract as live

loader = live.loader
STAGES = {"INITIALIZE": "initialize", "IMPORT_COMPANY_AND_ADMINS": "children", "SUBMIT": "submit"}
INITIATION_OPTIONS = {
    "fileAction": "IMPORT_AND_LOAD", "importConcurrentThreads": 8,
    "loadConcurrentThreads": 8, "importMaxErrorPercentage": 100,
    "loadMaxErrorPercentage": 100, "fileEncryption": "NONE",
    "verificationKey": None, "startDate": None, "deleteSourceFileFlag": "Y",
    "generateMappingFileFlag": "N", "uiInvoke": "Y",
}


def require(value, message):
    if not value:
        raise contract.ContractError(message)


def target_identity(host):
    try:
        url = urllib.parse.urlsplit(host)
        port = url.port
        require(url.scheme == "https" and url.hostname and not url.username and not url.password
                and url.path in ("", "/") and not url.query and not url.fragment
                and not any(c.isspace() for c in host) and "\\" not in host,
                "CPQ requires an exact HTTPS origin.")
        return (url.hostname.lower().rstrip("."), port or 443)
    except (TypeError, ValueError):
        raise contract.ContractError("CPQ requires an exact HTTPS origin.") from None


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        return None


def require_deployment(host):
    """Declared credential-free deployment probe; no redirects or retry."""
    target_identity(host)
    request = urllib.request.Request(host.rstrip("/") + "/cpq/rest/v1/site/version", method="GET")
    try:
        with urllib.request.build_opener(_NoRedirect()).open(request, timeout=30) as response:
            status = response.status
    except urllib.error.HTTPError as error:
        status = error.code
        error.close()
    except (OSError, urllib.error.URLError):
        raise contract.ContractError("CPQ deployment could not be verified safely.") from None
    require(status != 404, "CPQ is not deployed in this environment.")


def config_for(binding, properties, run_config=None):
    config = loader.read_config(Path(properties))
    preflight = binding["preflight"]
    target_identity(config["host"])
    require(config["host"] == preflight["host"]
            and (config.get("environment") or config["host"]) == preflight["environment"],
            "CPQ current target differs from the approved target.")
    if run_config is not None:
        require(loader.metadata.read_run_id(Path(run_config)) == preflight["runID"],
                "CPQ Run Book changed after preview.")
    return config


def route(preflight):
    return {
        "host": preflight["host"], "environment": preflight["environment"],
        "uploadFileName": preflight["uploadFileName"], "runID": preflight["runID"],
        "runBookTaskCode": "ORA_CPQ_SETUP_ASSISTANT" if preflight["supportsRunBookTaskCode"] else None,
        "ucmAccount": loader.UCM_DOCUMENT_ACCOUNT, "initiationOptions": dict(INITIATION_OPTIONS),
    }


def collect(binding, content, properties, run_config, task_input):
    """Called only at the routed read-only preview or pre-upload validation step."""
    import cpq_task_validation
    config = config_for(binding, properties, run_config)
    preflight = binding["preflight"]
    if binding["proposal"]["stage"] == "INITIALIZE":
        require_deployment(config["host"])
    eligible = preflight.get("eligible")
    expected_root = contract.INITIALIZE if binding["proposal"]["stage"] == "INITIALIZE" else contract.ASSISTANT
    require(isinstance(eligible, list) and bool(eligible)
            and all(isinstance(row, dict) and row.get("businessObject") == expected_root
                    and isinstance(row.get("sourceName"), str) and bool(row["sourceName"].strip()) for row in eligible)
            and preflight.get("mappingComplete") is True
            and isinstance(preflight.get("runID"), str) and bool(preflight["runID"].strip()),
            "CPQ requires eligible mapped preflight and a configured Run Book.")
    supported = loader._initiate_action_supports_run_book_task_code(config, getter=loader.metadata.get_json)
    require(type(preflight.get("supportsRunBookTaskCode")) is bool
            and supported == preflight["supportsRunBookTaskCode"],
            "CPQ Data Loader action registration changed.")
    task_evidence = cpq_task_validation.prepare(Path(task_input), preflight)
    preview = {k: v for k, v in binding["preview"].items() if k != "generatedAt"}
    require(preview == task_evidence["preview"], "CPQ preview differs from recomputed Task Hook evidence.")
    parsed = live.parse_registered_archive(content, config, getter=loader.metadata.get_json, byte_getter=loader.metadata.get_bytes)
    require(parsed.stage == STAGES[binding["proposal"]["stage"]], "CPQ live registration stage differs from preview.")
    require([{"section": op.section, "values": dict(op.fields)} for op in parsed.operations] == binding["operations"],
            "CPQ live intent differs from preview operations.")
    state = ({"assistant": live._assistant(config, loader.metadata.get_json)}
             if parsed.stage == "initialize" else live.discover_state(config, getter=loader.metadata.get_json))
    live.validate_operations(parsed, state)
    target = binding["proposal"]["target"]
    if parsed.stage != "initialize":
        require(target.get("assistantName") == state["assistant"]["Name"], "CPQ assistant target differs from discovery.")
        profile = state["CompanyProfiles"][0]
        require(str(target.get("companyProfileId")) == str(profile.get("CompanyProfileId") or profile.get("Id")),
                "CPQ Company Profile target differs from discovery.")
    return {"schemaVersion": "cpq-live-validation/1", "intent": parsed.as_manifest(),
            "state": state, "taskEvidence": task_evidence,
            "taskInputPath": str(Path(task_input).resolve()), "effectiveRoute": route(preflight)}


def verify_live(binding, content, properties, run_config):
    approved = binding["liveValidation"]
    current = collect(binding, content, properties, run_config, approved["taskInputPath"])
    require(contract.canonical_bytes(current) == contract.canonical_bytes(approved),
            "CPQ registration, readiness, routing or state changed since approval; preview again.")


def parsed_binding(binding):
    intent = binding["liveValidation"]["intent"]
    return contract.ParsedArchive(intent["stage"], intent["artifactSha256"],
        tuple(intent["registrationFingerprints"]), tuple(
            contract.Operation(op["member"], op["line"], op["section"], tuple(tuple(pair) for pair in op["fields"]))
            for op in intent["operations"]))


def verify_completed_load(binding, result, properties):
    return live.require_load_complete(result, config_for(binding, properties), getter=loader.metadata.get_json)


class FrozenAuth:
    def __init__(self, auth):
        self.context = auth.context
        self._token = auth.token()

    def token(self, *, refresh=False):
        require(not refresh, "CPQ write authentication failed; reconcile before any new approval. No mutation retry.")
        return self._token

    def secrets(self):
        return (self._token,)


def upload(binding, artifact, envelope, task_path, properties, run_config, before_upload,
           *, poster=None, multipart_uploader=None):
    """Guard unchanged Core callbacks against altered bytes, settings and retries.

    before_upload rechecks the consumed durable record, expiry, live binding and
    retained lock immediately before the first possible write. It grants no new
    approval. The same frozen identity is used by both actual write callbacks.
    """
    poster = poster or loader.post_json
    multipart_uploader = multipart_uploader or loader.post_ucm_multipart
    expected_route = binding["liveValidation"]["effectiveRoute"]
    require(expected_route == route(binding["preflight"]), "CPQ approved effective routing is inconsistent.")
    upload_attempted = initiation_attempted = False
    frozen = None
    content_id = None

    def upload_once(url, prepared, auth, **kwargs):
        nonlocal upload_attempted, frozen, content_id
        require(not upload_attempted and url == expected_route["host"] + loader.DOCUMENT_UPLOAD_PATH
                and not kwargs and isinstance(prepared, loader.PreparedArchive)
                and prepared.content == artifact.content
                and prepared.file_name == expected_route["uploadFileName"]
                and loader._ucm_document_account(prepared) == expected_route["ucmAccount"],
                "CPQ upload bytes, destination or settings differ from approval.")
        frozen = FrozenAuth(auth)
        before_upload()
        upload_attempted = True  # Never retry even when response is uncertain.
        response = multipart_uploader(url, prepared, frozen)
        if isinstance(response, dict):
            content_id = response.get("dDocName")
        return response

    def initiate_once(url, payload, auth, *, stage):
        nonlocal initiation_attempted
        expected = {**expected_route["initiationOptions"], "contentId": content_id,
                    "dataSetName": expected_route["uploadFileName"], "runID": expected_route["runID"]}
        if expected_route["runBookTaskCode"] is not None:
            expected["runBookTaskCode"] = expected_route["runBookTaskCode"]
        require(upload_attempted and frozen is not None and bool(content_id) and not initiation_attempted
                and url == expected_route["host"] + loader.INITIATE_PATH
                and stage == "data-load-initiation" and payload == expected,
                "CPQ initiation or routing-changing retry is not covered by approval.")
        initiation_attempted = True
        return poster(url, payload, frozen, stage=stage)

    try:
        return loader.upload_approved_preflight(envelope, Path(properties), run_config_path=Path(run_config),
            task_validation_envelope=task_path, poster=initiate_once, multipart_uploader=upload_once)
    except contract.ContractError as error:
        raise loader.DataLoadError("approval", str(error), content_id=content_id) from error
    except OSError as error:
        if content_id:
            raise loader.DataLoadError("transport", "CPQ initiation outcome is uncertain; reconcile the recorded upload.",
                                       content_id=content_id) from error
        raise
    except loader.DataLoadError as error:
        if content_id and not error.content_id:
            raise loader.DataLoadError(error.stage, error.message, http_status=error.http_status,
                                       content_id=content_id) from error
        raise

