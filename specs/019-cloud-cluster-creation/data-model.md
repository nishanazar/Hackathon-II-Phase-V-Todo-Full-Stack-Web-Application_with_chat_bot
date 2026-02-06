# Data Model: Cloud Cluster Creation for Phase V Advanced Cloud Deployment

## Entities

### Cloud Account
- **Fields**:
  - account_id: String (unique identifier for the cloud account)
  - provider: String (Oracle OKE, Azure AKS, or Google GKE)
  - region: String (geographic region where resources are hosted)
  - free_tier_status: Boolean (indicates if account is using free tier)
  - billing_status: String (active, suspended, etc.)
  - created_date: DateTime (timestamp of account creation)
  - api_endpoint: String (URL for cloud provider's API)

- **Validation rules**:
  - account_id must be unique across all cloud accounts
  - provider must be one of: "Oracle OKE", "Azure AKS", "Google GKE"
  - region must be a valid region for the selected provider
  - free_tier_status must be verified against provider's free tier policy

### Kubernetes Cluster
- **Fields**:
  - cluster_id: String (unique identifier for the cluster)
  - name: String (human-readable name for the cluster)
  - provider: String (Oracle OKE, Azure AKS, or Google GKE)
  - region: String (geographic region where cluster is hosted)
  - status: String (Active, Creating, Failed, etc.)
  - kubernetes_version: String (version of Kubernetes running on the cluster)
  - node_count: Integer (number of worker nodes in the cluster)
  - cpu_cores: Integer (total CPU cores across all nodes)
  - memory_gb: Integer (total memory in GB across all nodes)
  - created_date: DateTime (timestamp of cluster creation)
  - endpoint: String (API server endpoint URL)
  - ca_certificate: String (base64-encoded CA certificate)

- **Validation rules**:
  - cluster_id must be unique within the cloud account
  - status must be one of: "Active", "Creating", "Failed", "Terminating", "Terminated"
  - kubernetes_version must be a supported version for the provider
  - node_count must be within free tier limits
  - cpu_cores and memory_gb must be within free tier limits

### kubectl Configuration
- **Fields**:
  - config_file_path: String (path to the kubeconfig file)
  - cluster_context: String (name of the cluster context in kubeconfig)
  - cluster_name: String (name of the cluster being connected to)
  - user_credentials: Object (authentication information for the cluster)
  - namespace: String (default namespace for kubectl commands)
  - last_updated: DateTime (timestamp of last configuration update)

- **Validation rules**:
  - config_file_path must be a valid file path
  - cluster_context must match an existing cluster
  - user_credentials must contain valid authentication information
  - namespace must be a valid Kubernetes namespace name

### Cluster Health Status
- **Fields**:
  - cluster_id: String (identifier of the cluster being checked)
  - check_timestamp: DateTime (timestamp of the health check)
  - overall_status: String ("Healthy", "Degraded", "Unhealthy")
  - node_statuses: Array (list of statuses for individual nodes)
  - system_pod_statuses: Array (list of statuses for system pods)
  - api_response_time_ms: Integer (response time for cluster API calls)
  - error_messages: Array (list of any error messages from the check)

- **Validation rules**:
  - cluster_id must correspond to an existing cluster
  - overall_status must be one of: "Healthy", "Degraded", "Unhealthy"
  - node_statuses must contain valid Kubernetes node status values
  - system_pod_statuses must contain valid Kubernetes pod status values
  - api_response_time_ms must be a positive integer

## Relationships

- Cloud Account (1) → (Many) Kubernetes Clusters
- Kubernetes Cluster (1) → (1) kubectl Configuration
- Kubernetes Cluster (1) → (Many) Cluster Health Status (over time)

## State Transitions

### Kubernetes Cluster
- Creating → Active (when cluster is successfully provisioned)
- Creating → Failed (when cluster provisioning fails)
- Active → Terminating (when cluster deletion is initiated)
- Terminating → Terminated (when cluster is fully deleted)
- Active → Degraded (when cluster experiences issues)
- Degraded → Active (when cluster recovers from issues)

### Cluster Health Status
- Healthy → Degraded (when health checks detect issues)
- Degraded → Unhealthy (when critical issues are detected)
- Unhealthy → Degraded (when critical issues are resolved but minor issues remain)
- Degraded → Healthy (when all issues are resolved)