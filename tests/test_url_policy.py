from python.helpers import url_policy


def test_url_policy_blocks_external_when_restricted(monkeypatch):
    monkeypatch.setenv("A007_RESTRICT_EXTERNAL", "true")
    monkeypatch.delenv("A007_ALLOWED_DOMAINS", raising=False)
    monkeypatch.delenv("A007_BLOCKED_DOMAINS", raising=False)

    assert url_policy.url_allowed("http://localhost:8080")
    assert not url_policy.url_allowed("https://example.com")


def test_url_policy_applies_allow_and_block_lists(monkeypatch):
    monkeypatch.setenv("A007_RESTRICT_EXTERNAL", "1")
    monkeypatch.setenv("A007_ALLOWED_DOMAINS", "example.com,api.test.mil")
    monkeypatch.setenv("A007_BLOCKED_DOMAINS", "blocked.example.com")

    assert url_policy.url_allowed("https://example.com/path")
    assert url_policy.url_allowed("https://sub.example.com/path")
    assert not url_policy.url_allowed("https://blocked.example.com")
    assert not url_policy.url_allowed("https://evil.com")


def test_enforce_on_value_scans_nested_values(monkeypatch):
    monkeypatch.setenv("A007_RESTRICT_EXTERNAL", "true")
    monkeypatch.setenv("A007_ALLOWED_DOMAINS", "allowed.mil")

    url_policy.enforce_on_value({"nested": ["https://allowed.mil/data"]})

    try:
        url_policy.enforce_on_value({"url": "https://denied.com"})
    except ValueError as exc:
        assert "Blocked by URL restriction policy" in str(exc)
    else:
        raise AssertionError("Expected URL restriction policy exception")
