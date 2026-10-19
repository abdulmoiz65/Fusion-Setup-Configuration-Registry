"""Task-owned customer read adapter over unchanged core OAuth/byte transport.

Use only for the task-selected read workflow described in governed-read-routes.md.
No generic HTTP, token handling, retry or submission implementation lives here.
"""
from argparse import Namespace
from datetime import datetime, timezone
import hashlib
import importlib
import inspect
from pathlib import Path
import sys
from urllib.parse import urlsplit

from customer_soap_contract import build_request, inspect_response, ReadContractError


def load_core(repo):
    root = Path(repo).resolve()
    directory = root/'core/fusion-api/ucm-rest-client/scripts'
    auth = root/'core/auth/fusion-oauth-authentication/scripts'
    for module, expected in [('ucm_rest_client', directory/'ucm_rest_client.py'),
                             ('fusion_auth', auth/'fusion_auth.py')]:
        if not expected.is_file():
            raise ReadContractError('CORE_CLIENT_REQUIRED')
        existing = sys.modules.get(module)
        if existing is not None and Path(existing.__file__).resolve() != expected.resolve():
            raise ReadContractError('CORE_MODULE_ORIGIN_MISMATCH')
    # Imports remain pinned to the explicitly selected repository.
    original = list(sys.path)
    try:
        sys.path[:0] = [str(directory), str(auth)]
        core = importlib.import_module('ucm_rest_client')
    finally:
        sys.path[:] = original
    try:
        inspect.signature(core.request_bytes).bind({}, 'https://example.invalid',
            method='POST', authorization='', body=b'', headers={}, timeout=30)
    except TypeError as exc:
        raise ReadContractError('CORE_BYTE_CLIENT_SIGNATURE_UNSUPPORTED') from exc
    return core


def read(core, properties, token_cache, environment_url, operation, selectors, *, timeout=30):
    """One fixed read; no automatic login browser, refresh retry or generic URL input."""
    normalized = {key.replace('-', '_'): value for key, value in selectors.items()}
    allowed = {'account_id', 'account_number', 'source_name', 'location_id', 'party_number', 'site_number'}
    if len(normalized) != len(selectors) or not set(normalized) <= allowed:
        raise ReadContractError('INVALID_SELECTORS')
    path, action, payload = build_request(operation, **normalized)
    origin = urlsplit(environment_url)
    if origin.scheme != 'https' or not origin.hostname or origin.username or origin.password or \
            origin.path not in ('', '/') or origin.query or origin.fragment:
        raise ReadContractError('HTTPS_ENVIRONMENT_ORIGIN_REQUIRED')
    if type(timeout) is not int or not 1 <= timeout <= 120:
        raise ReadContractError('INVALID_TIMEOUT')
    props = core.read_properties(Path(properties))
    if props.get('restBaseUrl', '').rstrip('/') != environment_url.rstrip('/'):
        raise ReadContractError('API_PROFILE_ENVIRONMENT_MISMATCH')
    options = Namespace(auth_mode='oauth', access_token=None, redirect_url=None,
        auth_code=None, open_browser=False, callback_timeout=1,
        token_cache=Path(token_cache), force_login=False)
    try:
        authorization = core.get_authorization_header(props, options)
        content, _, status = core.request_bytes(props, environment_url.rstrip('/')+path,
            method='POST', authorization=authorization, body=payload,
            headers={'Content-Type':'text/xml; charset=UTF-8', 'Accept':'text/xml',
                     'Accept-Language':'en', 'SOAPAction':action}, timeout=timeout)
    except core.FusionHttpError as exc:
        raise ReadContractError('CUSTOMER_SOAP_HTTP_'+str(exc.status_code)) from None
    except Exception:
        # Never expose tokens, login URLs or SOAP fault bodies in diagnostics.
        raise ReadContractError('CUSTOMER_SOAP_CORE_CALL_FAILED') from None
    if not 200 <= status < 300:
        raise ReadContractError('CUSTOMER_SOAP_HTTP_STATUS')
    summary = inspect_response(content, operation, **normalized)
    summary.update(read_only=True, environment_url=environment_url.rstrip('/'),
        captured_at=datetime.now(timezone.utc).isoformat(),
        request_sha256=hashlib.sha256(payload).hexdigest(), automatic_retry=False,
        transport_owner='core.fusion-api.ucm-rest-client', parser_owner='manage-customer-uploads')
    return content, summary
