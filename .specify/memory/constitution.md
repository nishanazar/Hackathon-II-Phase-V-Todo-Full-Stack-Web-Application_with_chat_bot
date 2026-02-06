<!--
Sync Impact Report:
- Version change: 2.0.0 -> 3.0.0
- Modified principles: All principles updated for Phase V Advanced Cloud Deployment
- Added sections: Core Principles (8), Key Standards, Constraints, Success Criteria, High-Level Architecture, Workflow for Phase V
- Removed sections: Old principles from Phase II Full-Stack Web App
- Templates requiring updates: .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->

# Phase V Constitution: Advanced Cloud Deployment

## Core Principles

### I. Agentic Dev Stack: Write spec → Generate plan → Break into tasks → Implement via Claude Code
Every step of the development process must follow the agentic workflow: first write specifications, then generate implementation plans, break those plans into specific tasks, and finally implement everything through AI agents like Claude Code. No manual coding is allowed. This ensures consistency, traceability, and adherence to best practices throughout the development lifecycle.

### II. Cloud-Native First: Design for scalability, loose coupling, observability, and portability
All components must be designed with cloud-native principles in mind. This includes building for scalability, ensuring loose coupling between services, implementing comprehensive observability, and maintaining portability across different cloud providers. Applications must be containerized and designed to run optimally in container orchestration environments like Kubernetes.

### III. Event-Driven Architecture: Use Kafka/Redpanda for all async communication
All asynchronous communication between services must be handled through event streams using Kafka or Redpanda. This includes notifications, reminders, audit logs, and real-time synchronization. This architecture pattern ensures resilience, scalability, and decoupling of services while enabling complex processing patterns.

### IV. Dapr Everywhere: All inter-service communication, state, pub/sub, secrets, and scheduling via Dapr sidecars
Distributed Application Runtime (Dapr) must be used for all cross-service communication, state management, pub/sub messaging, secrets management, and job scheduling. All services must be deployed with Dapr sidecars to abstract away infrastructure concerns and provide consistent patterns across the entire application.

### V. AI-Assisted Ops: Use kubectl-ai, Kagent, and Claude Code for Kubernetes, Helm, and infra tasks
Infrastructure operations must leverage AI assistance tools like kubectl-ai, Kagent, and Claude Code for managing Kubernetes clusters, Helm charts, and other infrastructure tasks. This ensures efficient operations and reduces human error in complex deployment scenarios.

### VI. Zero to Minimal Cost: Prefer Oracle Always Free OKE, Redpanda Cloud free tier, Azure/GCP free credits
Cost optimization is critical. Whenever possible, utilize free tiers and credits such as Oracle Always Free OKE, Redpanda Cloud free tier, or Azure/GCP free credits. This allows for extensive development and testing without incurring significant expenses while still providing production-like environments.

### VII. Demo-Ready: Final output must be a live cloud URL + GitHub repo with CI/CD pipeline
Every implementation must result in a demo-ready application accessible via a live cloud URL, with a properly configured GitHub repository that includes a functioning CI/CD pipeline. This ensures that all work produces tangible, demonstrable results.

### VIII. Judges Focus: Show advanced features, event-driven design, Dapr abstraction, AI-assisted deployment, and monitoring
All implementations must emphasize the advanced features, event-driven architecture, Dapr integration, AI-assisted deployment processes, and comprehensive monitoring. This is critical for evaluation and demonstration purposes.

## Key Standards

The application must adhere to these technology requirements and architectural standards:
- Monorepo structure exactly as defined (.spec-kit/, specs/, frontend/, backend/)
- Tech stack fixed: Next.js 16+ App Router • FastAPI • SQLModel • Neon PostgreSQL • Better Auth + JWT
- All API endpoints: /api/{user_id}/tasks/* with JWT required and user_id matching
- Dapr integration for all service communication, state management, pub/sub, and secrets
- Kafka/Redpanda for all event streaming and async communication
- Containerized deployment with Docker and orchestrated via Kubernetes
- CI/CD pipeline via GitHub Actions
- Monitoring with Prometheus + Grafana or cloud-native solutions
- Specs referenced via @specs/... syntax

## Constraints

The following constraints are non-negotiable and must be strictly adhered to:
- No manual coding — all code via Claude Code / Qwen CLI
- Build on Phase III & IV (same images, Helm chart base)
- Prefer Oracle OKE (always free) > Azure AKS ($200 credit) > GKE ($300 credit)
- Kafka via Redpanda Cloud (free serverless) or self-hosted Strimzi on K8s
- Dapr full mode (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- CI/CD via GitHub Actions only
- Monitoring: Prometheus + Grafana or Azure Monitor/GKE built-in
- No breaking changes to Phase III/IV
- All env vars/secrets via Dapr secrets or K8s Secrets
- All inter-service communication via Dapr service invocation

## Success Criteria

The project will be considered successful when it meets these criteria:
- Advanced features fully working (recurring, reminders, priorities, tags, search/filter/sort)
- App deployed on cloud K8s (AKS/GKE/OKE) with live URL
- Dapr full stack running (Pub/Sub, State, Jobs, Secrets)
- Kafka/Redpanda handling events (task-events, reminders, task-updates)
- GitHub Actions CI/CD pipeline (build → push images → deploy to K8s)
- Basic monitoring/logging (pods logs, Prometheus metrics)
- Complete documentation with architecture diagram, commands, and demo URL
- All code traceable to specs via agentic workflow
- Ready for production deployment

## High-Level Architecture (Phase V Target)

Frontend (Next.js) → Dapr Sidecar → Backend (FastAPI + MCP) → Dapr Sidecar → Kafka/Redpanda → Notification/Recurring/Audit Services → Dapr Sidecar → Neon DB (via Dapr State)

## Workflow for Phase V

1. Advanced Features Implementation (Part A)
2. Dapr & Kafka Setup on Minikube (Part B)
3. Cloud Cluster Creation (AKS/GKE/OKE)
4. Dapr & Kafka on Cloud
5. Helm Upgrade & Deployment
6. CI/CD Pipeline (GitHub Actions)
7. Monitoring & Logging
8. Final Demo & Documentation

## Governance

This constitution supersedes all other development practices. All pull requests and code reviews must verify compliance with these principles. Deviations from this constitution require explicit spec update and approval by project leadership. Amendments to this constitution require explicit documentation and approval following the same spec-driven process as other project changes.

**Version**: 3.0.0 | **Ratified**: 2025-01-01 | **Last Amended**: 2026-01-29