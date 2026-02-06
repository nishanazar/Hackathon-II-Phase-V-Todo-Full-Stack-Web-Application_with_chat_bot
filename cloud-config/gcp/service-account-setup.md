# Creating a GCP Service Account for GitHub Actions

To deploy your application to Google Kubernetes Engine (GKE) using GitHub Actions, you need to create a service account with appropriate permissions.

## Steps to Create a Service Account

1. **Open Google Cloud Console**:
   - Go to https://console.cloud.google.com/
   - Select your project

2. **Navigate to IAM & Admin**:
   - In the left sidebar, click on "IAM & Admin"
   - Select "Service Accounts"

3. **Create a New Service Account**:
   - Click "Create Service Account"
   - Enter a name (e.g., "github-actions-gke")
   - Add a description (optional)
   - Click "Create and Continue"

4. **Assign Roles**:
   - Click "Select a role" dropdown
   - Add these roles:
     - Kubernetes Engine Admin
     - Storage Admin (for container registry access)
     - Service Account User
   - Click "Continue" and then "Done"

5. **Create and Download Key**:
   - Find your newly created service account in the list
   - Click on it to open the details
   - Go to the "Keys" tab
   - Click "Add Key" > "Create new key"
   - Select "JSON" as the key type
   - Click "Create"
   - The JSON key file will be downloaded to your computer

6. **Add Key to GitHub Secrets**:
   - Go to your GitHub repository
   - Navigate to Settings > Secrets and variables > Actions
   - Click "New repository secret"
   - Name it "GCP_CREDENTIALS"
   - Paste the entire content of the downloaded JSON file
   - Click "Add secret"

## Required Permissions Explained

- **Kubernetes Engine Admin**: Allows managing GKE clusters and deployments
- **Storage Admin**: Required for pushing images to Google Container Registry
- **Service Account User**: Allows impersonating service accounts if needed

## Security Best Practices

- Limit the service account's permissions to only what's necessary
- Regularly rotate the service account keys
- Use separate service accounts for different environments (dev, staging, prod)
- Monitor the service account's activity in Cloud Audit Logs