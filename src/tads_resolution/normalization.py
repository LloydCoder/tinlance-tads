"""Conservative identity normalization; normalization never proves identity."""

import re
import unicodedata

_CORPORATE_SUFFIXES = {
    "inc",
    "incorporated",
    "corp",
    "corporation",
    "ltd",
    "limited",
    "llc",
    "plc",
    "gmbh",
    "ag",
    "sa",
    "bv",
}


def normalize_name(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    value = re.sub(r"[^\w\s.-]", " ", value)
    tokens = [token for token in re.split(r"[\s.-]+", value) if token]
    while tokens and tokens[-1] in _CORPORATE_SUFFIXES:
        tokens.pop()
    return " ".join(tokens)


def normalize_domain(value: str) -> str:
    value = value.strip().casefold().rstrip(".")
    if value.startswith("https://"):
        value = value[8:]
    elif value.startswith("http://"):
        value = value[7:]
    value = value.split("/", 1)[0]
    if value.startswith("www."):
        value = value[4:]
    if not value or "." not in value or any(ch.isspace() for ch in value):
        raise ValueError("invalid domain")
    return value
