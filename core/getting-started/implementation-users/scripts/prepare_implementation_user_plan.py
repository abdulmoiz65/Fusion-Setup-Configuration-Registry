#!/usr/bin/env python3
"""Prepare a gated Fusion implementation-user setup plan."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


BASE_JOB_ROLES = [
    {
        "displayName": "Application Implementation Consultant",
        "roleCode": "ORA_ASM_APPLICATION_IMPLEMENTATION_CONSULTANT_JOB",
    },
    {
        "displayName": "IT Security Manager",
        "roleCode": "ORA_FND_IT_SECURITY_MANAGER_JOB",
    },
    {
        "displayName": "Application Diagnostic Administrator",
        "roleCode": "ORA_FND_DIAG_ADMINISTRATOR_JOB",
    },
]

FSM_REQUIRED_ROLES = [
    {
        "displayName": "Application Implementation Consultant",
        "roleType": "Job",
        "roleCode": "ORA_ASM_APPLICATION_IMPLEMENTATION_CONSULTANT_JOB",
        "source": "Oracle 26B Functional Setup Manager Roles and Allowed Activities mapping",
    },
]

ABSTRACT_ROLES = []

SETUP_TASKS = [
    {"taskName": "Create Implementation Users", "taskCode": "FND_CREATE_IMPLEMENTATION_USERS"},
    {
        "taskName": "Import Users and Roles into Application Security",
        "taskCode": "ORA_ASE_IMPORT_USERS_AND_ROLES",
    },
]

USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_.@-]+$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validate_username(username: str) -> None:
    if not USERNAME_PATTERN.fullmatch(username):
        raise ValueError(
            "username must contain only letters, numbers, dot, underscore, hyphen, or @. "
            "Do not paste command flags into the username value."
        )
    if username.startswith("-") or "--" in username:
        raise ValueError("username looks like a command option; pass only the Fusion username")


def validate_email(email: str) -> None:
    if not EMAIL_PATTERN.fullmatch(email):
        raise ValueError("email must be a valid address such as user@example.com")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare a gated Fusion implementation-user setup plan.")
    parser.add_argument("--username")
    parser.add_argument("--email")
    parser.add_argument("--last-name")
    parser.add_argument("--project-id")
    parser.add_argument("--execution-mode", choices=["preview", "execute"], default="preview")
    parser.add_argument("--output")
    return parser.parse_args()


def require_value(value: str | None, prompt: str) -> str:
    if value:
        return value
    return input(prompt)


def build_plan(args: argparse.Namespace) -> dict[str, Any]:
    username = require_value(args.username, "Implementation username: ").strip()
    if not username:
        raise ValueError("username is required")
    validate_username(username)

    email = require_value(args.email, "Implementation user email: ").strip()
    if not email:
        raise ValueError("email is required")
    validate_email(email)

    return {
        "generatedAt": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "release": "Oracle Fusion Cloud Applications 26B",
        "mode": args.execution_mode,
        "projectId": args.project_id,
        "oracleGrounding": {
            "source": "https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/mapping-of-setup-activities-and-required-roles.html#Roles-and-the-Allowed-Activities",
            "allowedActivitiesSource": "https://docs.oracle.com/en/cloud/saas/applications-common/26b/oafsm/mapping-of-setup-activities-and-required-roles.html#Roles-and-the-Allowed-Activities",
            "requiredRolesForAllowedActivities": FSM_REQUIRED_ROLES,
            "privilegesAreNotRoleGrants": [
                "Manage Setup Migration Settings",
                "Manage Third Party Applications",
                "task-specific setup data privileges",
            ],
        },
        "user": {
            "username": username,
            "email": email,
            "lastName": (args.last_name or username).strip(),
            "associatedPersonType": "None",
            "userCategory": "DEFAULT",
            "active": True,
        },
        "setupTasks": SETUP_TASKS,
        "baseJobRoles": BASE_JOB_ROLES,
        "abstractRoles": [],
        "finalRoleAssignments": [
            *[role["displayName"] for role in BASE_JOB_ROLES],
        ],
        "writeGate": {
            "requiresExplicitApproval": True,
            "requiresReadOnlyPreflight": True,
            "requiresResolvedRoleIds": True,
            "requiresAiProfileOptionVerification": False,
        },
        "validationChecklist": [
            "User exists and is active.",
            "Application Implementation Consultant role is assigned.",
            "IT Security Manager role is assigned.",
            "Application Diagnostic Administrator role is assigned.",
        ],
    }


def main() -> int:
    args = parse_args()
    plan = build_plan(args)
    rendered = json.dumps(plan, indent=2)
    if args.output:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(rendered + "\n", encoding="utf-8")
        print(f"Wrote {output_path}")
    else:
        print(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
