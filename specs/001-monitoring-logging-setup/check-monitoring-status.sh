# Script to check monitoring stack status
# This would normally be run after deploying the monitoring stack

#!/bin/bash

echo "Checking monitoring stack components..."

# Check if monitoring namespace exists
kubectl get namespace monitoring

# Check if Prometheus is running
kubectl get pods -n monitoring -l app.kubernetes.io/name=prometheus

# Check if Grafana is running
kubectl get pods -n monitoring -l app.kubernetes.io/name=grafana

# Check if Alertmanager is running
kubectl get pods -n monitoring -l app.kubernetes.io/name=alertmanager

# Check all services in monitoring namespace
kubectl get svc -n monitoring

echo "Monitoring stack status check completed"