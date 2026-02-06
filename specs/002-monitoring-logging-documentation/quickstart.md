# Quickstart Guide: Monitoring, Logging & Documentation for Phase V

## Overview
This guide provides quick instructions to set up monitoring, logging, and documentation for the cloud deployment.

## Prerequisites
- Access to the cloud Kubernetes cluster (OKE/AKS/GKE)
- Helm 3.x installed locally
- kubectl configured to access the cluster
- Administrative privileges on the cluster

## Installing Monitoring Stack

### Step 1: Add Prometheus Helm Repository
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### Step 2: Create Monitoring Namespace
```bash
kubectl create namespace monitoring
```

### Step 3: Install Prometheus and Grafana
```bash
helm install prometheus-grafana prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --set grafana.adminPassword=your_secure_password \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false
```

### Step 4: Access Grafana Dashboard
```bash
kubectl port-forward -n monitoring svc/prometheus-grafana 3000:80
```
Then navigate to http://localhost:3000 and log in with username "admin" and the password set in Step 3.

## Accessing Application Logs

### View All Application Logs
```bash
kubectl get pods
kubectl logs <pod-name> -n <namespace>
```

### View Real-time Logs
```bash
kubectl logs -f <pod-name> -n <namespace>
```

### View Logs from Last Hour
```bash
kubectl logs --since=1h <pod-name> -n <namespace>
```

## Verifying Application Status

### Check if Application is Running
```bash
kubectl get pods -n <application-namespace>
kubectl get services -n <application-namespace>
kubectl get ingress -n <application-namespace>  # if using ingress
```

### Test Application Endpoints
```bash
# Get the external IP or hostname
kubectl get svc <frontend-service-name> -n <application-namespace>

# Or if using ingress
kubectl get ingress <ingress-name> -n <application-namespace>
```

## Updating Documentation

### Architecture Diagram
The architecture diagram should show:
- Frontend (Next.js) → Dapr Sidecar → Backend (FastAPI + MCP) → Dapr Sidecar → Kafka/Redpanda → Notification/Recurring/Audit Services → Dapr Sidecar → Neon DB (via Dapr State)
- Monitoring stack (Prometheus + Grafana) collecting metrics from all components
- Logging infrastructure collecting logs from all components

### Deployment Commands
Include these commands in your README:
```bash
# Deploy the application
helm upgrade --install <release-name> ./charts/<chart-name> --namespace <namespace> --create-namespace

# Install monitoring stack
helm install prometheus-grafana prometheus-community/kube-prometheus-stack --namespace monitoring --create-namespace

# Check application status
kubectl get pods,services,ingress -n <application-namespace>

# Access application
kubectl port-forward svc/<service-name> 3000:<port> -n <application-namespace>
```

## Demo Preparation

### Live Demo Checklist
- [ ] Verify all application features work (login, AI chat, task management)
- [ ] Access Grafana dashboard and show real-time metrics
- [ ] Demonstrate log access via kubectl
- [ ] Show updated documentation with architecture diagram
- [ ] Confirm live cloud URL is accessible and functional

### Presentation Materials
Prepare slides covering:
1. System architecture overview
2. Implementation approach
3. Key technical achievements
4. Monitoring and logging setup
5. Demo of live application