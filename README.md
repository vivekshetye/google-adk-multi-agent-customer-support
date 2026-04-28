# Multi-Agent Customer Support with Google ADK

A production-ready multi-agent customer support system built with Google ADK (Agent Development Kit) and A2A protocol. Demonstrates how to build, test, and deploy multi-agent AI systems using Google Agents CLI and Claude Code.

## Overview

This project implements a 4-agent customer support team:

```
User Input
    │
    ▼
┌─────────────────┐
│   Concierge     │ ← Entry point (root agent)
│  (Dispatcher &  │
│   Triage)       │
└────────┬────────┘
         │ A2A calls
  ┌──────┴───────────────────────────┐
  │                                  │
  ▼                                  ▼
┌──────────────┐            ┌──────────────┐
│ Logistician  │◄──────────►│   Resolver   │
│ (Orders &    │            │ (Returns &   │
│  Warehouse)  │            │  Conflicts)  │
└──────────────┘            └──────────────┘
  │
  ▼
┌──────────────┐
│   Stylist    │
│ (Product     │
│  Discovery)  │
└──────────────┘
```

| Agent | Role |
|-------|------|
| Concierge | Routes user requests to the right specialist |
| Logistician | Handles order status, shipping, inventory |
| Resolver | Processes returns and refunds (flags >$100 for human review) |
| Stylist | Product search and recommendations |

## Features

- **A2A Protocol** — Agents communicate via Agent-to-Agent protocol
- **Human-in-the-Loop** — High-value refunds are flagged for human review
- **Production Ready** — CI/CD with GitHub Actions, Terraform infrastructure, Docker
- **Observability** — Cloud Trace, BigQuery, and Cloud Logging integration
- **Built with Google Agents CLI** — Scaffold, test, and deploy in minutes

---

## Quick Start

### Prerequisites

```bash
# Install Google Agents CLI
uvx google-agents-cli setup

# Install dependencies
agents-cli install
```

### Run Locally

```bash
agents-cli playground
```

### Test the Agent

```bash
# Run unit and integration tests
uv run pytest tests/unit tests/integration

# Run evaluation tests
agents-cli eval run
```

---

## Project Structure

```
customer-support/
├── app/                     # Agent code
│   ├── agent.py             # Main entry point
│   ├── agents/              # Agent definitions (concierge, logistician, resolver, stylist)
│   ├── app_utils/           # Utilities (telemetry, typing)
│   └── tools/               # Agent tools
├── customer_support/        # Support module + Terraform
├── data/                    # Mock data (orders.json, products.json)
├── deployment/              # Terraform configurations
│   └── terraform/           # (cicd/, shared/, single-project/)
├── tests/                   # Test suites (unit/, integration/, eval/, load_test/)
├── .github/workflows/        # GitHub Actions CI/CD
├── CLAUDE.md                # Development guide
├── pyproject.toml           # Project dependencies
└── Dockerfile              # Container image
```

---

## Deployment

### Deploy to Google Cloud

```bash
# Set your project
gcloud config set project <your-project-id>

# Deploy to Cloud Run
agents-cli deploy
```

### Add CI/CD

```bash
agents-cli scaffold enhance      # Add CI/CD + Terraform
agents-cli infra cicd            # Full infrastructure setup
```

---

## For YouTube Viewers

This project accompanies a video walkthrough. Key commands from the video:

| Command | Purpose |
|---------|---------|
| `uvx google-agents-cli setup` | Install the CLI |
| `agents-cli install` | Install dependencies |
| `agents-cli playground` | Test locally |
| `agents-cli deploy` | Deploy to Cloud Run |

**File locations mentioned in the video:**
- Agent code: `app/agents/`
- Tests: `tests/`
- Infrastructure: `deployment/terraform/`

---

## Commands Reference

| Command | Description |
|---------|-------------|
| `agents-cli install` | Install dependencies |
| `agents-cli playground` | Launch local dev server |
| `agents-cli lint` | Run code quality checks |
| `agents-cli eval run` | Run evaluation tests |
| `agents-cli deploy` | Deploy to Cloud Run |
| `agents-cli scaffold enhance` | Add CI/CD and Terraform |
| `uv run pytest tests/unit tests/integration` | Run unit and integration tests |

---

## License

Apache License 2.0 — See [LICENSE](LICENSE) for details.

---

## Related Resources

- [Google ADK Documentation](https://google.github.io/adk-docs/)
- [Google Agents CLI](https://google.github.io/agents-cli/)
- [A2A Protocol](https://a2a-protocol.org/)
- [A2A Inspector](https://github.com/a2aproject/a2a-inspector) — Test A2A interoperability