# Implementation Plan: Dapr & Kafka Setup on Minikube

**Branch**: `018-dapr-kafka-minikube` | **Date**: 2026-01-29 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/018-dapr-kafka-minikube/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Install and configure Dapr on Minikube with Kafka/Redpanda Pub/Sub component for event-driven features. This involves initializing Dapr using the CLI, deploying a Kafka/Redpanda broker (preferably Redpanda for simplicity), creating Dapr pub/sub component configuration, and validating the setup by publishing and consuming task-events. The solution will enable applications to use Dapr for pub/sub without direct Kafka client code, maintaining compatibility with existing Phase V features.

## Technical Context

**Language/Version**: N/A (infrastructure setup using Dapr CLI, Helm, and Kubernetes)
**Primary Dependencies**: Dapr, Kafka/Redpanda, Minikube, Helm, kubectl
**Storage**: N/A (infrastructure setup)
**Testing**: Manual verification of Dapr sidecars, pub/sub functionality, and event flow
**Target Platform**: Minikube (local Kubernetes cluster)
**Project Type**: Infrastructure setup
**Performance Goals**: Reliable event delivery through pub/sub system with minimal latency
**Constraints**:
- Must use Dapr CLI and Helm for installation
- Prefer Redpanda (Kafka-compatible, simpler) or Strimzi for self-hosted Kafka
- No breaking changes to existing Phase V features
- Local Minikube cluster only (not cloud deployment)
**Scale/Scope**: Single-node Minikube cluster supporting pub/sub for task events

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Agentic Dev Stack: Write spec → Generate plan → Break into tasks → Implement via Claude Code
- [x] Cloud-Native First: Design for scalability, loose coupling, observability, and portability
- [x] Event-Driven Architecture: Use Kafka/Redpanda for all async communication
- [x] Dapr Everywhere: All inter-service communication, state, pub/sub, secrets, and scheduling via Dapr sidecars
- [x] AI-Assisted Ops: Use kubectl-ai, Kagent, and Claude Code for Kubernetes, Helm, and infra tasks
- [x] Zero to Minimal Cost: Prefer Oracle Always Free OKE, Redpanda Cloud free tier, Azure/GCP free credits
- [x] Demo-Ready: Final output must be a live cloud URL + GitHub repo with CI/CD pipeline (infrastructure enables demo-ready app)
- [x] Judges Focus: Show advanced features, event-driven design, Dapr abstraction, AI-assisted deployment, and monitoring
- [x] Tech stack compliance: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- [x] Monorepo structure compliance: .spec-kit/, specs/, frontend/, backend/
- [x] All API endpoints follow /api/{user_id}/tasks/* pattern with JWT validation
- [x] Dapr integration for all service communication, state management, pub/sub, and secrets
- [x] Kafka/Redpanda for all event streaming and async communication
- [x] Containerized deployment with Docker and orchestrated via Kubernetes
- [x] CI/CD pipeline via GitHub Actions (infrastructure supports CI/CD)
- [x] Monitoring with Prometheus + Grafana or cloud-native solutions (infrastructure supports monitoring)

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Infrastructure Components (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
dapr/
├── components/          # Dapr component configurations (pubsub, state store, etc.)
│   ├── pubsub.yaml      # Kafka/Redpanda pub/sub configuration
│   └── statestore.yaml  # State store configuration (if needed)
└── configs/             # Dapr configuration files
    └── config.yaml      # Dapr configuration

kafka/                   # Kafka/Redpanda specific configurations
├── helm-values/         # Helm values for Kafka/Redpanda deployment
│   └── redpanda-values.yaml
└── topics/              # Topic definitions (if needed)
    └── task-events.yaml

helm/                    # Helm charts for the application
└── todo-app/
    ├── Chart.yaml
    ├── values.yaml      # Updated values to include Dapr annotations
    └── templates/
        ├── deployment.yaml
        └── dapr-components/
            └── pubsub.yaml
```

**Structure Decision**: Infrastructure setup using Dapr and Kafka/Redpanda components with Helm chart updates to support pub/sub functionality. The setup includes Dapr component configurations for pub/sub and state management, along with Kafka/Redpanda configurations managed via Helm.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
