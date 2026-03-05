import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import run_ui


def test_socketio_engine_configuration_defaults():
    server = run_ui.socketio_server.eio

    assert server.ping_interval == 25
    assert server.ping_timeout == 20
    assert server.max_http_buffer_size == 50 * 1024 * 1024


def test_parse_session_timeout_seconds_falls_back_on_invalid_values():
    assert run_ui._parse_session_timeout_seconds("") == 30 * 60
    assert run_ui._parse_session_timeout_seconds("not-a-number") == 30 * 60


def test_parse_session_timeout_seconds_uses_configured_minutes():
    assert run_ui._parse_session_timeout_seconds("45") == 45 * 60
