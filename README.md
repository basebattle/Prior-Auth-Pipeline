# Prior-Auth-Pipeline
Multi-Agent System Automating Prior Auth Review Using LangGraph.

## Architecture
- LangGraph Orchestration
- Multi-Agent Consensus: Clinical, Billing, and Regulatory agents.
- Real-time decision endpoints mapped in `specs/routes.json`.

## Hardening
- Enterprise logging via `backend/config/production_logging.py`.
- Isolated environment enforcement using `uv`.
