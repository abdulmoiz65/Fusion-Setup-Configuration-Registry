#!/usr/bin/env python3
"""Enroll OAuth trust from a user-supplied Fusion URL or approved issuer."""
import argparse
import getpass
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import tempfile

import fusion_auth as auth


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    trust = commands.add_parser("trust", help="Enroll trust from Fusion login redirects or explicit IdP settings")
    trust.add_argument("--environment", required=True)
    source = trust.add_mutually_exclusive_group(required=True)
    source.add_argument("--fusion-url", help="User-supplied Fusion HTTPS URL; derive issuer from its login redirects")
    source.add_argument("--issuer", help="Explicit independently approved issuer HTTPS origin")
    trust.add_argument("--client-id", required=True)
    trust.add_argument("--authorize-path", default="/oauth2/v1/authorize")
    trust.add_argument("--token-path", default="/oauth2/v1/token")
    trust.add_argument("--replace", action="store_true", help="Explicitly replace an existing enrollment")
    secret = commands.add_parser("store-client-secret", help="Store a prompted secret in private platform storage after trust validation")
    secret.add_argument("--properties", required=True, type=Path)
    secret.add_argument("--migrate-properties-secret", action="store_true", help="After pin validation, move clientSecret to private credential storage and clear its properties value")
    account_cmd = commands.add_parser("client-secret-account", help="Print the non-secret account binding for a trusted OAuth client")
    account_cmd.add_argument("--properties", required=True, type=Path)
    check = commands.add_parser("check-client-secret", help="Validate access to the enrolled or cloud-mounted client secret without printing it")
    check.add_argument("--properties", required=True, type=Path)
    args = parser.parse_args(argv)
    if args.command == "trust":
        if args.fusion_url and (args.authorize_path != auth.OAUTH_AUTHORIZE_PATH or args.token_path != auth.OAUTH_TOKEN_PATH):
            parser.error("Custom endpoint paths require explicit --issuer enrollment")
        existing_policy = False
        try:
            policy = auth.load_oauth_trust_policy()
            existing_policy = True
        except auth.UnauthorizedTokenEndpointError:
            if auth.OAUTH_TRUST_POLICY.exists() or auth.OAUTH_TRUST_POLICY.is_symlink():
                raise
            policy = {"version": 1, "environments": {}}
        if args.environment in policy["environments"] and not args.replace:
            parser.error("Environment already enrolled; review the new pins and use --replace")
        entry = (auth.fusion_oauth_trust_entry(args.environment, args.fusion_url, args.client_id)
                 if args.fusion_url else auth.oauth_trust_entry(args.environment, args.issuer, args.client_id,
                                                               args.authorize_path, args.token_path))
        policy["environments"][args.environment] = entry
        auth.write_private_json(auth.OAUTH_TRUST_POLICY, policy, replace=existing_policy)
        print("OAuth trust policy enrolled; no properties file was used as a trust source.")
    else:
        props = auth.read_properties(args.properties)
        account = auth.client_secret_account(props)  # Validate before reading a secret.
        if args.command == "client-secret-account":
            print(account)
            return 0
        if args.command == "check-client-secret":
            auth.load_client_secret(props)
            print("Confidential-client secret is available for the trusted environment and client.")
            return 0
        if sys.platform != "win32" and not sys.platform.startswith("linux") and not auth.keychain_available():
            parser.error("Confidential-client storage requires macOS Keychain or Windows Credential Manager; otherwise use PKCE")
        if args.properties.is_symlink():
            parser.error("Refusing a symlinked properties file")
        original = args.properties.read_text()
        value = props.get("clientSecret", "") if args.migrate_properties_secret else getpass.getpass("Approved OAuth client secret (hidden): ")
        if not value or any(c in value for c in "\r\n\x00"):
            parser.error("Secret must be nonempty and single-line")
        # Interactive security input keeps the secret out of OS process arguments.
        if sys.platform == "win32":
            from windows_private_storage import store_client_secret_windows
            store_client_secret_windows(auth.CLIENT_SECRET_SERVICE, account, value)
        elif sys.platform.startswith("linux"):
            auth.store_linux_client_secret(props, value)
        else:
            command = shlex.join(["add-generic-password", "-U", "-s", auth.CLIENT_SECRET_SERVICE,
                                  "-a", account, "-w", value]) + "\n"
            result = subprocess.run(["security", "-i"], input=command, capture_output=True, text=True, check=False)
            if result.returncode:
                raise RuntimeError("Keychain storage failed; no secret was printed")
            if auth.load_client_secret(props) != value:
                raise RuntimeError("Keychain verification failed")
        if args.migrate_properties_secret:
            if args.properties.read_text() != original:
                raise RuntimeError("Credential storage succeeded but properties changed; refusing to overwrite them")
            sanitized = re.sub(r"(?m)^(\s*clientSecret\s*=)[^\r\n]*", r"\1", original)
            temporary = None
            try:
                with tempfile.NamedTemporaryFile(mode="w", dir=args.properties.parent, delete=False) as handle:
                    temporary = Path(handle.name)
                    handle.write(sanitized)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, args.properties)
            finally:
                if temporary:
                    temporary.unlink(missing_ok=True)
            print("Client secret verified in private credential storage and removed from properties; other settings preserved.")
        else:
            print("Client secret stored in private credential storage; remove any clientSecret value from properties.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
