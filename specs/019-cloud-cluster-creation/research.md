# Research: Cloud Cluster Creation for Phase V Advanced Cloud Deployment

## Decision: Cloud Provider Selection
**Rationale**: Oracle OKE was selected as the primary option due to its Always Free tier which perfectly aligns with the requirement to incur no costs. Oracle's free tier includes a 2-node Kubernetes cluster with 10GB memory and 4 OCPUs, which is sufficient for hosting the Todo AI Chatbot application during development and testing phases.

**Alternatives considered**:
- Azure AKS: Offers $200 credit for new accounts but requires credit card for signup
- Google GKE: Offers $300 credit for new accounts but requires credit card for signup
- AWS EKS: Has limited free tier and requires credit card for signup

## Decision: Cluster Configuration
**Rationale**: For the free tier, Oracle OKE provides a minimal cluster configuration with 1 node pool containing 2 worker nodes. This configuration balances cost (free) with functionality needed to host the Todo AI Chatbot application and prepare for Dapr and Helm deployments.

**Alternatives considered**:
- Smaller configurations: Would limit deployment capabilities
- Larger configurations: Would exceed free tier limits and incur costs

## Decision: Region Selection
**Rationale**: For optimal latency for users in Karachi, the Mumbai region (ap-mumbai-1) is recommended as it's geographically closest to Karachi among Oracle's free tier regions. If Mumbai is unavailable, Frankfurt (eu-frankfurt-1) is the next best option.

**Alternatives considered**:
- Ashburn (us-ashburn): Farther from Karachi but reliable
- Phoenix (us-phoenix-1): Farther from Karachi but reliable
- Toronto (ca-toronto-1): Farther from Karachi but reliable

## Decision: kubectl Configuration Approach
**Rationale**: Using the cloud provider's CLI tool to generate the kubeconfig file and setting the KUBECONFIG environment variable is the standard approach for connecting to managed Kubernetes services. This ensures secure access with proper authentication and authorization.

**Alternatives considered**:
- Manual configuration: More error-prone and complex
- Third-party tools: Adds unnecessary complexity for a basic connection

## Decision: Cluster Health Verification Method
**Rationale**: Using standard kubectl commands like `kubectl get nodes` and `kubectl get pods --all-namespaces` provides a simple and effective way to verify cluster health. These commands directly show the status of nodes and system pods.

**Alternatives considered**:
- Cloud provider console: Less automated and harder to script
- Third-party monitoring tools: Overkill for basic health verification

## Decision: Dapr and Helm Preparation
**Rationale**: Ensuring the cluster meets minimum requirements for Dapr and Helm installation includes verifying kubectl access, checking for required RBAC permissions, and ensuring the cluster version is compatible with the latest Dapr and Helm releases.

**Alternatives considered**:
- Installing Dapr/Helm immediately: Premature without verifying cluster health first
- Skipping verification: Could lead to deployment issues in later phases