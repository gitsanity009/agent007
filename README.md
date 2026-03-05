<div align="center">

# `Agent 007`

### Autonomous AI Agent for Classified Environments

Built on [Agent Zero](https://github.com/agent0ai/agent-zero) with JSIG/RMF security controls baked in.

</div>

---

## Overview

Agent 007 is a rebranded and hardened fork of Agent Zero, designed for use in controlled and classified environments. It integrates security controls aligned with JSIG (Joint SAP Implementation Guide) and the NIST Risk Management Framework (RMF) at a moderate (IL4-equivalent) level, while remaining practical and usable for real work.

## Security Controls

### Classification Banners (JSIG/RMF)
- Top and bottom classification banners on all pages per JSIG requirements
- Configurable via environment variables:
  - `CLASSIFICATION_LEVEL` - `unclassified`, `cui`, `confidential`, `secret`, `top-secret`, `ts-sci`
  - `CLASSIFICATION_TEXT` - Custom banner text override
- Default: **UNCLASSIFIED** (green banner)

### DoD Warning/Consent Banner
- Standard DoD Notice and Consent banner on the login page
- Displayed before authentication per STIG requirements

### Audit Logging (AU-3, AU-12)
- Structured JSON audit log at `logs/audit.log`
- Logs: authentication (success/failure), logouts, session timeouts, tool executions, code executions, file access, settings changes, system startup/shutdown
- Configurable via:
  - `AUDIT_LOG_ENABLED` - `true`/`false` (default: `true`)
  - `AUDIT_LOG_PATH` - Custom log path

### Session Controls (AC-12)
- Inactivity timeout (default: 30 minutes, configurable via `SESSION_TIMEOUT_MINUTES`)
- Session lifetime limit (default: 8 hours, configurable via `SESSION_LIFETIME_HOURS`)
- HttpOnly and SameSite=Strict session cookies
- Session timeout events logged to audit log

### Network Isolation
- External update checks disabled (no outbound calls to agent-zero.ai)
- External links removed from UI
- All operations designed for air-gapped/isolated network use

## Configuration

All security settings are configurable via environment variables in your `.env` file:

```bash
# Classification
CLASSIFICATION_LEVEL=unclassified
CLASSIFICATION_TEXT=                    # Optional custom banner text

# Session Controls
SESSION_TIMEOUT_MINUTES=30              # Inactivity timeout
SESSION_LIFETIME_HOURS=8                # Maximum session duration

# Audit
AUDIT_LOG_ENABLED=true
AUDIT_LOG_PATH=logs/audit.log

# Authentication (required for classified use)
AUTH_LOGIN=your_username
AUTH_PASSWORD=your_password
```

## Quick Start

```bash
# Configure your environment
cp .env.example .env
# Edit .env with your settings

# Run with Docker
docker build -f DockerfileLocal -t agent007 .
docker run -p 50001:80 agent007

# Visit http://localhost:50001 to start
```

## Documentation

See the [docs/](./docs/) directory for detailed documentation on:
- [Installation](./docs/setup/installation.md)
- [Usage](./docs/guides/usage.md)
- [Development Setup](./docs/setup/dev-setup.md)
- [Architecture](./docs/developer/architecture.md)

## Based On

Agent 007 is built on [Agent Zero](https://github.com/agent0ai/agent-zero) (MIT License).
All original Agent Zero features are preserved -- multi-agent cooperation, memory, skills, MCP, A2A, projects, and more.

## Key Features (inherited from Agent Zero)

- **General-purpose Assistant** with persistent memory
- **Computer as a Tool** - code execution, terminal access, browser agent
- **Multi-agent Cooperation** - subordinate agents for subtask delegation
- **Skills System** - portable `SKILL.md` standard
- **MCP Server + Client** support
- **A2A Protocol** support
- **Git-based Projects** with authentication
- **Fully Dockerized** with Kali Linux base
