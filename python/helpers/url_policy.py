import os
import re
import ipaddress
from urllib.parse import urlparse
from typing import Any


_TRUE_VALUES = {"1", "true", "yes", "on"}
_URL_RE = re.compile(r"https?://[^\s'\"<>()\[\]{}]+", re.IGNORECASE)


def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in _TRUE_VALUES


def _parse_domains(name: str) -> set[str]:
    raw = os.getenv(name, "")
    return {
        item.strip().lower().lstrip(".")
        for item in raw.split(",")
        if item and item.strip()
    }


def _is_local_host(host: str) -> bool:
    host = host.lower().strip("[]")
    if host in {"localhost", "127.0.0.1", "::1"}:
        return True
    try:
        return ipaddress.ip_address(host).is_private
    except ValueError:
        return host.endswith(".local")


def _matches_domain(host: str, domain: str) -> bool:
    host = host.lower()
    domain = domain.lower().lstrip(".")
    return host == domain or host.endswith(f".{domain}")


def url_allowed(url: str) -> bool:
    if not _env_flag("A007_RESTRICT_EXTERNAL"):
        return True

    parsed = urlparse(url)
    if parsed.scheme.lower() not in {"http", "https"}:
        return True

    host = (parsed.hostname or "").lower()
    if not host:
        return False

    blocked = _parse_domains("A007_BLOCKED_DOMAINS")
    if any(_matches_domain(host, domain) for domain in blocked):
        return False

    if _is_local_host(host):
        return True

    allowed = _parse_domains("A007_ALLOWED_DOMAINS")
    if not allowed:
        return False

    return any(_matches_domain(host, domain) for domain in allowed)


def assert_url_allowed(url: str, context: str = "outbound request") -> None:
    if not url_allowed(url):
        raise ValueError(
            f"Blocked by URL restriction policy ({context}): '{url}'. "
            "Configure A007_ALLOWED_DOMAINS / A007_BLOCKED_DOMAINS as needed."
        )


def enforce_on_value(value: Any, context: str = "tool arguments") -> None:
    if isinstance(value, dict):
        for item in value.values():
            enforce_on_value(item, context=context)
        return
    if isinstance(value, (list, tuple, set)):
        for item in value:
            enforce_on_value(item, context=context)
        return
    if not isinstance(value, str):
        return

    for match in _URL_RE.findall(value):
        assert_url_allowed(match, context=context)
