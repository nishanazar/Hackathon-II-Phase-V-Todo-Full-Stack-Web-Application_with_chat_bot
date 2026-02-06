#!/bin/bash
# Deployment verification script for Helm chart on Minikube

echo "Verifying Helm deployment..."

# Check if Helm release is active
echo "Checking Helm releases..."
helm list

# Check pods status
echo "Checking pods..."
kubectl get pods

# Check services
echo "Checking services..."
kubectl get svc

# More detailed pod information
echo "Detailed pod information..."
kubectl describe pods

echo "Verification complete."