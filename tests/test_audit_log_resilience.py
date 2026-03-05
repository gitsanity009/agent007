import logging
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import types

sys.modules.setdefault("simpleeval", types.SimpleNamespace(simple_eval=lambda *args, **kwargs: None))

from python.helpers import audit_log


def _reset_audit_logger_state():
    logger = logging.getLogger("agent007.audit")
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        try:
            handler.close()
        except Exception:
            pass
    audit_log._logger = None


def test_get_logger_disables_when_directory_cannot_be_created(monkeypatch):
    _reset_audit_logger_state()
    monkeypatch.setenv("AUDIT_LOG_ENABLED", "true")

    def raise_os_error(*_args, **_kwargs):
        raise PermissionError("read-only filesystem")

    monkeypatch.setattr(audit_log.Path, "mkdir", raise_os_error)

    logger = audit_log._get_logger()

    assert logger is False
    assert audit_log._logger is False


def test_get_logger_disables_when_file_handler_init_fails(monkeypatch):
    _reset_audit_logger_state()
    monkeypatch.setenv("AUDIT_LOG_ENABLED", "true")

    class RaisingFileHandler:
        def __init__(self, *_args, **_kwargs):
            raise PermissionError("cannot write")

    monkeypatch.setattr(audit_log.logging, "FileHandler", RaisingFileHandler)

    logger = audit_log._get_logger()

    assert logger is False
    assert audit_log._logger is False


def test_emit_disables_logging_when_write_fails(monkeypatch):
    _reset_audit_logger_state()

    class BrokenLogger:
        def info(self, _message):
            raise OSError("disk full")

    monkeypatch.setattr(audit_log, "_get_logger", lambda: BrokenLogger())

    audit_log._emit("TOOL_EXEC", {"tool_name": "x"})

    assert audit_log._logger is False
