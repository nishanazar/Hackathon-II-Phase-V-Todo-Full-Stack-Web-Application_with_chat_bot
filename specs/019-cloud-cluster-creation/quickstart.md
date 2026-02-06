# Quickstart Guide: Cloud Cluster Creation for Phase V Advanced Cloud Deployment

## Overview
This guide provides a step-by-step process to create a production-grade Kubernetes cluster on Oracle OKE (Oracle Kubernetes Engine) to host the Todo AI Chatbot application. The setup leverages Oracle's Always Free tier to avoid any costs.

## Prerequisites
- Oracle Cloud account with Always Free tier enabled
- OCI CLI installed and configured
- kubectl installed
- Internet connection

## Step-by-Step Instructions

### 1. Sign Up for Oracle Cloud (if needed)
1. Visit https://www.oracle.com/cloud/free/
2. Click "Start for Free"
3. Enter your email and create an account
4. Verify your email address
5. Add your phone number for verification
6. Complete the identity verification process
7. Note: No credit card is required for the Always Free tier

### 2. Install and Configure OCI CLI
1. Download and install OCI CLI from https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm
2. Run `oci setup config` to create a configuration file
3. Follow the prompts to enter your tenancy OCID, user OCID, region, and generate an API key
4. Save the config file at `~/.oci/config`

### 3. Create Compartment (Optional but Recommended)
1. Log in to Oracle Cloud Console
2. Navigate to Identity & Security → Compartments
3. Click "Create Compartment"
4. Enter a name and description for your compartment
5. Click "Create Compartment"

### 4. Create Virtual Cloud Network (VCN)
1. In the Oracle Cloud Console, navigate to Networking → Virtual Cloud Networks
2. Click "Create Virtual Cloud Network"
3. Select your compartment
4. Choose "VCN with Internet Connectivity" as the template
5. Enter a name for your VCN
6. Click "Create Virtual Cloud Network"

### 5. Create Kubernetes Cluster
1. In the Oracle Cloud Console, navigate to Developer Services → Kubernetes Clusters (OKE)
2. Click "Create Cluster"
3. Select "Quick Create" for a simple setup
4. Enter a name for your cluster
5. Select your compartment
6. Choose "Custom" for the Kubernetes version (select the latest stable version)
7. Select your VCN created in step 4
8. For the "Always Free" option, ensure you select shapes that qualify for the free tier:
   - Node Pool: Use VM.Standard.E2.1.Micro (1 OCPU, 1 GB memory) - eligible for Always Free
   - Kubernetes version: Latest stable version
9. Configure the node pool with 1-2 nodes (within free tier limits)
10. Click "Create Cluster"

### 6. Wait for Cluster Creation
1. Monitor the cluster creation progress in the console
2. The process typically takes 10-15 minutes
3. The cluster status should change to "Active"

### 7. Configure kubectl
1. Once the cluster is active, click on the cluster name in the console
2. Click "Access Cluster" button
3. Copy the command under "Option 3: Cloud Shell" or "Manual" method
4. Run the command in your terminal to download the kubeconfig file
5. The command typically looks like: `oci ce cluster create-kubeconfig --cluster-id <cluster-ocid> --file ~/.kube/config --region <region> --token-version 2.0.0`

### 8. Verify Connection
1. Set the KUBECONFIG environment variable:
   ```bash
   export KUBECONFIG=~/.kube/config
   ```
2. Verify the connection:
   ```bash
   kubectl get nodes
   ```
3. You should see your cluster nodes listed with "Ready" status

### 9. Verify Cluster Health
1. Check all system pods are running:
   ```bash
   kubectl get pods --all-namespaces
   ```
2. Verify cluster info:
   ```bash
   kubectl cluster-info
   ```
3. Check cluster health:
   ```bash
   kubectl get cs
   ```

### 10. Prepare for Dapr and Helm
1. Verify that your cluster meets the minimum requirements for Dapr:
   - Kubernetes version 1.22 or higher
   - RBAC enabled (standard in OKE)
2. Install Helm (if not already installed):
   ```bash
   curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
   ```
3. Verify Helm installation:
   ```bash
   helm version
   ```

## Troubleshooting Tips
- If you encounter permission errors, ensure your OCI CLI is properly configured with the correct user and permissions
- If kubectl commands fail, verify that the KUBECONFIG environment variable points to the correct file
- If cluster creation fails, check that you're using Always Free eligible shapes and staying within free tier limits
- If nodes don't become ready, check the node pool configuration and ensure sufficient resources are allocated

## Next Steps
1. Verify that your cluster is ready for Dapr and Helm deployment
2. Proceed with installing Dapr on your cluster
3. Prepare Helm charts for your Todo AI Chatbot application
4. Set up monitoring and logging for your cluster