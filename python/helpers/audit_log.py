"""
Audit Logging Module - JSIG/RMF Compliance (IL4 Moderate)

Provides structured audit logging for security-relevant events per
NIST SP 800-53 AU controls and JSIG requirements.

Audit events are written to a dedicated audit log file (logs/audit.log)
in JSON format for easy ingestion by SIEM tools.

Configurable via environment variables:
    AUDIT_LOG_PATH    - Path to audit log file (default: logs/audit.log)
    AUDIT_LOG_ENABLED - Enable/disable audit logging (default: true)
"""

import json
import os
import time
import logging
import threading
from datetime import datetime, timezone
from pathlib import Path

from python.helpers.files import get_abs_path

_lock = threading.Lock()
_logger = None


def _get_logger():
    global _logger
    if _logger is not None:
        return _logger

    enabled = os.getenv("AUDIT_LOG_ENABLED", "true").lower() != "false"
    if not enabled:
        _logger = False
        return _logger

    log_path = os.getenv("AUDIT_LOG_PATH", get_abs_path("logs/audit.log"))
    log_dir = os.path.dirname(log_path)
    Path(log_dir).mkdir(parents=True, exist_ok=True)

    _logger = logging.getLogger("agent007.audit")
    _logger.setLevel(logging.INFO)
    _logger.propagate = False

    if not _logger.handlers:
        handler = logging.FileHandler(log_path, encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(message)s"))
        _logger.addHandler(handler)

    return _logger


def _emit(event_type: str, details: dict, user: str = "system", severity: str = "INFO"):
    """Write a structured audit log entry."""
    logger = _get_logger()
    if logger is False:
        return

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "severity": severity,
        "user": user,
        "details": details,
    }

    with _lock:
        logger.info(json.dumps(entry, default=str))


# --- Public audit event functions ---

def log_login_success(username: str, remote_addr: str):
    """AU-3: Log successful authentication."""
    _emit("AUTH_SUCCESS", {
        "username": username,
        "remote_addr": remote_addr,
    }, user=username)


def log_login_failure(username: str, remote_addr: str):
    """AU-3: Log failed authentication attempt."""
    _emit("AUTH_FAILURE", {
        "username": username,
        "remote_addr": remote_addr,
    }, user=username, severity="WARNING")


def log_logout(username: str):
    """AU-3: Log user logout."""
    _emit("LOGOUT", {"username": username}, user=username)


def log_session_timeout(username: str):
    """AC-12: Log session termination due to inactivity."""
    _emit("SESSION_TIMEOUT", {"username": username}, user=username, severity="WARNING")


def log_chat_start(user: str, chat_id: str):
    """AU-3: Log new chat session creation."""
    _emit("CHAT_START", {"chat_id": chat_id}, user=user)


def log_tool_execution(user: str, tool_name: str, agent_id: str = "0"):
    """AU-3: Log agent tool execution."""
    _emit("TOOL_EXEC", {
        "tool_name": tool_name,
        "agent_id": agent_id,
    }, user=user)


def log_code_execution(user: str, runtime: str = "python", agent_id: str = "0"):
    """AU-3: Log code execution events."""
    _emit("CODE_EXEC", {
        "runtime": runtime,
        "agent_id": agent_id,
    }, user=user)


def log_file_access(user: str, file_path: str, action: str = "read"):
    """AU-3: Log file access events."""
    _emit("FILE_ACCESS", {
        "file_path": file_path,
        "action": action,
    }, user=user)


def log_settings_change(user: str, setting_key: str):
    """AU-3: Log configuration changes."""
    _emit("SETTINGS_CHANGE", {
        "setting_key": setting_key,
    }, user=user, severity="WARNING")


def log_startup(classification_level: str):
    """AU-3: Log system startup."""
    _emit("SYSTEM_STARTUP", {
        "classification_level": classification_level,
    })


def log_shutdown():
    """AU-3: Log system shutdown."""
    _emit("SYSTEM_SHUTDOWN", {})
