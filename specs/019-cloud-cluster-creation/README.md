# Cloud Cluster Environment Setup

## Current Environment

- kubectl: Installed (v1.34.1)
- Helm: Installed (v4.1.0)
- OCI CLI: Not installed (needs manual installation on Windows)

## Manual Setup Steps

1. Install OCI CLI manually by downloading from Oracle's website:
   - Go to https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm
   - Download the appropriate installer for your OS
   - Follow the installation instructions
2. Configure OCI CLI after account setup:
   - Run `oci setup config` to create a configuration file
   - Follow the prompts to enter your tenancy OCID, user OCID, region, and generate an API key
   - Save the config file at `~/.oci/config`
3. Create Oracle Cloud account (free tier):
   - Visit https://www.oracle.com/cloud/free/
   - Click "Start for Free"
   - Enter email and create account
   - Verify email address
   - Add phone number for verification
   - Complete identity verification (no credit card required for Always Free tier)
4. Log in to Oracle Cloud Console and verify account status
5. Navigate to Kubernetes services section in the console to confirm access
6. Check billing dashboard to confirm free tier status and zero charges
7. Create a dedicated compartment for the cluster (recommended practice)
8. Create a Virtual Cloud Network (VCN) with internet connectivity
9. Create Kubernetes cluster using Oracle OKE Quick Create option
10. Configure cluster with free tier eligible settings:
    - Name: todo-cluster
    - Shape: VM.Standard.E2.1.Micro (1 OCPU, 1GB memory - eligible for Always Free)
    - Node pool: 1-2 nodes (within free tier limits)
    - Region: ap-mumbai-1 (closest to Karachi)
11. Monitor cluster creation progress until status shows "Active"
12. Document cluster details (OCID, region, configuration) in README.md
13. Verify cluster accessibility via Oracle Cloud Console

## Next Steps

1. Complete manual account setup steps above
2. Continue with cluster creation once account is verified
3. After cluster is created, configure kubectl:
   - Generate kubeconfig file using OCI CLI command: `oci ce cluster create-kubeconfig --cluster-id <cluster-ocid> --file ~/.kube/config --region <region> --token-version 2.0.0`
   - Set KUBECONFIG environment variable: `export KUBECONFIG=~/.kube/config`
   - Test kubectl connection: `kubectl cluster-info`
   - Verify kubectl can list nodes: `kubectl get nodes`
   - Verify kubectl can list namespaces: `kubectl get namespaces`
   - Document kubectl configuration steps and verification results
   - Create backup of kubeconfig file in secure location
4. After kubectl is configured, verify cluster health:
   - Run `kubectl get nodes` to verify all nodes are in Ready state
   - Run `kubectl get pods --all-namespaces` to verify system pods are running
   - Run `kubectl get cs` (componentstatuses) to check cluster components
   - Check cluster resource utilization with `kubectl top nodes`
   - Verify cluster version compatibility with Dapr and Helm requirements
   - Document health check results and cluster status
   - Create cluster health verification script for future use
5. Prepare for Dapr and Helm deployment:
   - Verify Helm installation with `helm version` command
   - Check cluster RBAC configuration to ensure it supports Dapr
   - Verify Kubernetes version meets Dapr requirements (1.22+)
   - Test cluster admin privileges with `kubectl auth can-i '*' '*' --as=admin`
   - Document Dapr and Helm prerequisites verification
   - Prepare Dapr and Helm installation commands for next phase
   - Create checklist for next phase deployment preparation
6. Final verification and cleanup:
   - Verify all acceptance scenarios from user stories are satisfied
   - Update main project README with cloud provider setup instructions
   - Create troubleshooting guide based on potential issues encountered
   - Document cost management practices to stay within free tier
   - Perform final verification that no changes were made to Phase V Step 1/2 code
   - Clean up temporary files and configurations if any
   - Run final end-to-end test: kubectl get nodes (should show Ready status)
   - Archive configuration files and access details securely