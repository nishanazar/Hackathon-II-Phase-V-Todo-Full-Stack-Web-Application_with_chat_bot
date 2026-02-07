#!/bin/bash
# Script to deploy the Todo application to Google Kubernetes Engine

set -e  # Exit on any error

echo "Starting deployment to Google Kubernetes Engine..."

# Variables - Update these with your values
PROJECT_ID="gen-lang-client-0071684271"  # Replace with your GCP project ID
GKE_CLUSTER="todo-app-cluster"
GKE_ZONE="us-central1"
IMAGE_NAME="todo-app"
IMAGE_TAG="latest"

# Authenticate with Google Cloud
echo "Authenticating with Google Cloud..."
gcloud auth login

# Set the project
if [ -z "$PROJECT_ID" ]; then
    echo "Please set your PROJECT_ID variable in the script."
    echo "Go to https://console.cloud.google.com/ to find your project ID."
    exit 1
fi

gcloud config set project $PROJECT_ID

# Enable required APIs
echo "Enabling required APIs..."
gcloud services enable container.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Create GKE cluster if it doesn't exist
echo "Creating GKE cluster..."
gcloud container clusters create $GKE_CLUSTER \
    --zone=$GKE_ZONE \
    --num-nodes=3 \
    --machine-type=e2-medium \
    --disk-size=100GB \
    --enable-autoscaling \
    --min-nodes=1 \
    --max-nodes=5

# Get cluster credentials
echo "Getting cluster credentials..."
gcloud container clusters get-credentials $GKE_CLUSTER --zone=$GKE_ZONE

# Build and push Docker images to Google Container Registry
echo "Building and pushing Docker images..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/todo-frontend:$IMAGE_TAG ./frontend
gcloud builds submit --tag gcr.io/$PROJECT_ID/todo-backend:$IMAGE_TAG ./backend

# Update the values.yaml file with the correct image paths
echo "Updating Helm values with GCP image paths..."
sed -i "s|repository: todo-frontend|repository: gcr.io/$PROJECT_ID/todo-frontend|" ./charts/todo-app/values.yaml
sed -i "s|tag: \"latest\"|tag: \"$IMAGE_TAG\"|" ./charts/todo-app/values.yaml
sed -i "s|repository: todo-backend|repository: gcr.io/$PROJECT_ID/todo-backend|" ./charts/todo-app/values.yaml

# Install/update the application using Helm
echo "Deploying application with Helm..."
helm upgrade --install todo-app ./charts/todo-app --namespace default --create-namespace

# Wait for deployments to be ready
echo "Waiting for deployments to be ready..."
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-frontend --timeout=300s
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=todo-backend --timeout=300s

# Expose services if needed
echo "Checking services..."
kubectl get services

echo "Deployment completed successfully!"
echo "To access your application, run:"
echo "kubectl get services"