"""CAP-only business vocabulary. No target verification or authorization."""

CODES = frozenset({"ORA_EVERYONE", "ORA_CONTRIBUTORS"})
LABELS = {"ORA_EVERYONE": "Everyone (all catalog administrators)",
          "ORA_CONTRIBUTORS": "Contributors only"}
ALIASES = {
    "everyone": "ORA_EVERYONE",
    "everyone (all catalog administrators)": "ORA_EVERYONE",
    "all catalog administrators": "ORA_EVERYONE",
    "all catalog admins": "ORA_EVERYONE",
    "all catalog managers": "ORA_EVERYONE",
    "contributors": "ORA_CONTRIBUTORS",
    "contributors only": "ORA_CONTRIBUTORS",
    "only contributors": "ORA_CONTRIBUTORS",
}
ACCESS_NOTE = ("Visibility controls catalog-administrator viewing, not learner enrollment "
               "or permission to manage content. Contributor membership, functional "
               "privileges and central override access remain separate. No contributors "
               "are added by choosing either value; empty membership does not imply creator-only access.")


def normalize(value):
    """Map only unambiguous complete choices; never substring-match prose."""
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise ValueError("Choose Everyone (all catalog administrators) or Contributors only")
    key = " ".join(value.split()).casefold()
    codes = {code.casefold(): code for code in CODES}
    result = codes.get(key) or ALIASES.get(key)
    if result is None:
        raise ValueError("Visibility is unclear: choose Everyone (all catalog administrators) or Contributors only; learner access is separate")
    return result


def review(value):
    code = normalize(value)
    return {"input": value, "code": code, "label": LABELS[code], "access_note": ACCESS_NOTE}
