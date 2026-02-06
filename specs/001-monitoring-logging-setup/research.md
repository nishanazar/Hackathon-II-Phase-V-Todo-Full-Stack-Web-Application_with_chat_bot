# Research: Monitoring & Logging Setup for Phase V

## Decision: Monitoring Tool Selection
**Rationale**: Selected Prometheus + Grafana via kube-prometheus-stack Helm chart for open-source demonstration purposes, aligning with the constraint to prefer open-source solutions for demo.
**Alternatives considered**: 
- Cloud-native solutions (Azure Monitor, GKE Monitoring, AWS CloudWatch)
- Other open-source stacks (ELK Stack, Datadog agent)

## Decision: Grafana Access Method
**Rationale**: Using port-forwarding for simplicity and security during initial setup. For production, an ingress controller would be more appropriate.
**Alternatives considered**:
- Exposing Grafana via LoadBalancer service
- Setting up ingress with TLS

## Decision: Metrics Collection Approach
**Rationale**: Using kube-prometheus-stack which includes Prometheus, Grafana, Alertmanager, and node exporters out-of-the-box, simplifying deployment and configuration.
**Alternatives considered**:
- Individual deployments of each component
- Using managed services from cloud providers

## Decision: Log Aggregation Strategy
**Rationale**: Initially relying on kubectl logs for simplicity, with potential expansion to centralized logging solution like Loki-stack for more advanced log querying and correlation.
**Alternatives considered**:
- ELK Stack (Elasticsearch, Logstash, Kibana)
- Fluentd + Elasticsearch
- Cloud-native logging solutions

## Research Tasks Completed

1. **Prometheus + Grafana Helm Chart Options**
   - kube-prometheus-stack (includes Prometheus Operator, Grafana, Alertmanager, node exporters)
   - Prometheus community charts
   - Result: kube-prometheus-stack selected for comprehensive monitoring solution

2. **Cloud Native Monitoring Solutions**
   - Azure Monitor for AKS
   - Google Cloud Operations Suite for GKE
   - Oracle Cloud Infrastructure Monitoring for OKE
   - Result: Decided to stick with Prometheus + Grafana for open-source demo

3. **Grafana Dashboard Configuration**
   - Default dashboards included in kube-prometheus-stack
   - Custom dashboard creation process
   - Result: Will use default dashboards initially, customize as needed

4. **Log Aggregation Methods**
   - Centralized logging with Loki-stack
   - Using existing kubectl logs approach
   - Cloud-native logging solutions
   - Result: Starting with kubectl logs, with option to add Loki later

5. **Security Considerations for Monitoring Stack**
   - Securing Grafana access with strong credentials
   - Network policies to restrict access to monitoring components
   - Result: Will implement basic auth initially, enhance security in later phases

## Technical Unknowns Resolved

- **Q: How to install Prometheus and Grafana on Kubernetes?**
  A: Using kube-prometheus-stack Helm chart which provides a complete monitoring solution with pre-configured dashboards.

- **Q: How to access Grafana securely?**
  A: Initially using kubectl port-forward, with plans to implement ingress with authentication in production.

- **Q: How to collect application logs?**
  A: Starting with kubectl logs approach, with potential expansion to Loki-stack for centralized logging.

- **Q: How to configure alerting?**
  A: Using Alertmanager component of kube-prometheus-stack with custom alerting rules.