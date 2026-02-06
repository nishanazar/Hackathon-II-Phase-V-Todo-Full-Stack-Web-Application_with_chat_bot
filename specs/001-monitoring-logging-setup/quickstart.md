# Quickstart: Monitoring & Logging Setup for Phase V

## Prerequisites

- Kubernetes cluster (cloud deployment)
- Helm 3.x installed
- kubectl configured to connect to your cluster
- Access to the repository containing the monitoring charts

## Installation Steps

### 1. Add Prometheus Helm Repository

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
```

### 2. Install kube-prometheus-stack

```bash
helm install monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  --create-namespace \
  --set prometheus.prometheusSpec.podMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.serviceMonitorSelectorNilUsesHelmValues=false \
  --set prometheus.prometheusSpec.retention=24h \
  --set grafana.adminPassword='prom-operator' \
  --set grafana.service.type=ClusterIP
```

### 3. Access Grafana Dashboard

```bash
kubectl port-forward -n monitoring svc/monitoring-grafana 3000:80
```

Then open your browser to `http://localhost:3000` and log in with:
- Username: `admin`
- Password: `prom-operator`

### 4. Access Prometheus

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
```

Then open your browser to `http://localhost:9090`

### 5. Access Alertmanager

```bash
kubectl port-forward -n monitoring svc/monitoring-kube-alertmanager 9093:9093
```

Then open your browser to `http://localhost:9093`

### 6. View Application Logs

To view logs for your Todo AI Chatbot application:

```bash
# List all pods in the application namespace
kubectl get pods -n <your-app-namespace>

# View logs for a specific pod
kubectl logs -n <your-app-namespace> <pod-name>

# Follow logs in real-time
kubectl logs -f -n <your-app-namespace> <pod-name>
```

## Useful Commands

### Check Monitoring Stack Status

```bash
kubectl get all -n monitoring
```

### Upgrade Monitoring Stack

```bash
helm upgrade monitoring prometheus-community/kube-prometheus-stack \
  --namespace monitoring \
  -f values.yaml
```

### Uninstall Monitoring Stack

```bash
helm uninstall monitoring -n monitoring
kubectl delete ns monitoring
```

## Default Dashboards

Once Grafana is accessible, you can view several pre-configured dashboards:

1. **Kubernetes App Metrics** - Shows metrics for your applications
2. **Kubernetes Cluster Monitoring** - Overview of cluster health
3. **Prometheus Performances** - Performance metrics of Prometheus itself
4. **Node Exporter Full** - Detailed metrics about nodes

## Creating Custom Dashboards

1. Log into Grafana
2. Click the "+" icon in the left sidebar and select "Dashboard"
3. Click "Add new panel"
4. In the query editor, enter a PromQL query to visualize your metrics
5. Customize the visualization and click "Apply"
6. Save the dashboard with a descriptive name

## Configuring Alerts

Alerts are configured in the `values.yaml` file when installing the chart. You can define alerting rules based on PromQL queries. Example:

```yaml
prometheus:
  additionalPrometheusRules:
    - name: custom-alerts
      groups:
        - name: example
          rules:
            - alert: HighCPUUsage
              expr: 100 - (avg by(instance) (irate(node_cpu_seconds_total{mode="idle"}[5m])) * 100) > 80
              for: 2m
              labels:
                severity: warning
              annotations:
                summary: "High CPU usage detected"
                description: "Instance {{ $labels.instance }} has had high CPU usage for more than 2 minutes"
```

## Troubleshooting

### Grafana is not accessible

1. Verify the service is running:
   ```bash
   kubectl get svc -n monitoring
   ```
2. Check if the pod is running:
   ```bash
   kubectl get pods -n monitoring
   ```
3. Look at pod logs:
   ```bash
   kubectl logs -n monitoring <grafana-pod-name>
   ```

### No metrics are appearing

1. Verify Prometheus is scraping targets:
   ```bash
   kubectl port-forward -n monitoring svc/monitoring-kube-prometheus-prometheus 9090:9090
   ```
   Then visit `http://localhost:9090/targets` to see if targets are healthy.

2. Check if your application exposes metrics at the expected endpoint.

### Memory/CPU limits

The default installation sets conservative resource limits. Adjust them in your values file if needed:

```yaml
prometheus:
  prometheusSpec:
    resources:
      requests:
        memory: 1Gi
        cpu: 500m
      limits:
        memory: 2Gi
        cpu: 1000m
```