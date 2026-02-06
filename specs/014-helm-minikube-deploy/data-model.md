# Data Model: Helm Chart Deployment on Minikube for Phase IV

## Key Entities

### Helm Chart
- **Name**: todo-chart
- **Location**: ./helm/todo-chart
- **Components**: Contains manifests for frontend and backend deployments, services, and configurations
- **Validation**: Must be installable on Minikube without errors

### Minikube Cluster
- **State**: Must be running before deployment
- **Resources**: Sufficient CPU and memory for frontend and backend pods
- **Access**: Available via kubectl commands

### Kubernetes Pods
- **Frontend Pod**:
  - Image: todo-frontend:latest
  - Status: Must reach Running state
  - Resources: Configured via Helm chart
- **Backend Pod**:
  - Image: todo-backend:latest
  - Status: Must reach Running state
  - Resources: Configured via Helm chart

### Kubernetes Services
- **todo-frontend Service**:
  - Type: Determined by Helm chart (likely ClusterIP or LoadBalancer)
  - Port: Configured via Helm chart
  - Access: Via minikube service or port-forward
- **todo-backend Service**:
  - Type: Determined by Helm chart (likely ClusterIP)
  - Port: Configured via Helm chart
  - Access: Internal to cluster or via port-forward

### Deployment Verification
- **Pod Status**: All pods must show "Running" status
- **Service Creation**: Both frontend and backend services must be created
- **Application Accessibility**: Frontend must be accessible via minikube service or port-forward