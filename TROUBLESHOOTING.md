# Troubleshooting Guide: CI/CD Pipeline

## Overview
This guide provides solutions to common issues that may arise during the CI/CD pipeline execution for the Todo AI Chatbot application.

## Common Issues and Solutions

### 1. GitHub Actions Workflow Fails During Docker Build

**Symptoms**: 
- Error during the "Build and push Docker image" steps
- Message: "failed to solve: unexpected status: 401 Unauthorized"

**Solution**:
- Verify that the `REGISTRY_TOKEN` secret is correctly set in your GitHub repository settings
- Ensure the token has the required permissions (`write:packages` scope)
- Regenerate the token if it has expired

### 2. KUBECONFIG Secret Issues

**Symptoms**:
- Error during the "Set up KUBECONFIG" step
- Message: "Error from server (Forbidden)" or "Unable to connect to the server"

**Solution**:
- Verify that the KUBECONFIG secret contains the correct base64-encoded kubeconfig file
- Check that the Kubernetes cluster credentials are still valid
- Ensure the GitHub Actions runner has the necessary permissions to access the cluster

### 3. Helm Deployment Failures

**Symptoms**:
- Error during the "Deploy to Kubernetes using Helm" step
- Messages indicating resource conflicts or insufficient permissions

**Solution**:
- Check that the Helm chart is valid by running `helm lint charts/todo-ai-chatbot`
- Verify that the GitHub Actions runner has sufficient RBAC permissions in the cluster
- Ensure the namespace exists or allow the workflow to create it (`--create-namespace` flag)

### 4. Pod Startup Failures

**Symptoms**:
- Error during the "Verify deployment" step
- Message: "timed out waiting for the condition"

**Solution**:
- Check the pod logs: `kubectl logs -l app.kubernetes.io/instance=todo-ai-chatbot-release -n default`
- Verify that the Docker images were pushed successfully to the registry
- Check that the image tags in the Helm values match the ones built in the workflow

### 5. Timeout Issues

**Symptoms**:
- Workflow fails due to timeout
- Message: "The operation was canceled"

**Solution**:
- Increase the timeout values in the workflow for longer-running operations
- Check if the cloud cluster is responding slowly due to resource constraints
- Verify network connectivity between GitHub Actions runners and your cloud cluster

## Best Practices

### 1. Secret Management
- Regularly rotate your secrets (tokens, certificates)
- Use the minimum required permissions for each secret
- Never hardcode secrets in the workflow files

### 2. Image Tagging
- Use semantic versioning for production releases
- Include commit SHAs for traceability
- Clean up old images periodically to save registry space

### 3. Monitoring
- Set up notifications for workflow failures
- Monitor deployment metrics
- Keep logs for debugging purposes

## Debugging Tips

### 1. Enable Debug Logging
Add the following step to your workflow to enable debug logging for kubectl:
```yaml
- name: Enable kubectl debug mode
  run: |
    kubectl config set-credentials --username=debug
    export KUBECONFIG=~/.kube/config
```

### 2. Manual Verification
If the workflow fails, you can manually verify each step:
- Check Docker images in the registry
- Verify Helm release status: `helm status todo-ai-chatbot-release -n default`
- Check pod statuses: `kubectl get pods -n default`

### 3. Rollback Procedures
If a deployment causes issues:
- Use Helm to rollback: `helm rollback todo-ai-chatbot-release -n default`
- Or redeploy a previous version by triggering the workflow with a previous commit

## Support Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Helm Documentation](https://helm.sh/docs/)
- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Docker Documentation](https://docs.docker.com/)