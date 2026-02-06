# Deploying Your Application Using Google Cloud Free Tier (No Credit Card Required)

This guide will walk you through setting up and deploying your application using Google Cloud's free tier without requiring a credit card.

## Step 1: Create a Google Cloud Account Without a Credit Card

1. Go to https://console.cloud.google.com/
2. Click "Start Free" or "Sign up"
3. Follow the prompts to create your account
4. When prompted for payment information, look for an option to continue with the free tier only
   - Google allows you to sign up for the free tier without entering payment information
   - You may need to verify your phone number instead

## Step 2: Understanding Google Cloud Free Tier Benefits

With the free tier, you get:
- $300 in credits for the first 12 months (may require credit card)
- OR Always-Free tier with limited resources at no cost:
  - Compute Engine: 1 non-preemptible e2-micro VM instance (up to 720 hours/month)
  - Cloud Storage: 5 GB of regional storage
  - Cloud Functions: 2 million invocations per month
  - Many other services with limited usage

## Step 3: Deploy Your Application Using Free Resources

Since your application uses Kubernetes, you'll need to be mindful of the free tier limitations. Here's how to deploy using only free resources:

1. First, make sure you're logged in to gcloud:
```bash
gcloud auth login
```

2. Set your project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

3. For Kubernetes, note that GKE (Google Kubernetes Engine) is NOT part of the free tier. Instead, you can:

Option A: Use Google Cloud Run (Recommended for free tier)
- Cloud Run is part of the free tier
- It's serverless, so you only pay for what you use
- Has generous free limits

Option B: Use Compute Engine with container-optimized OS
- Limited to 1 e2-micro instance per month
- More restrictive but possible for small applications

## Step 4: Deploy Using Google Cloud Run (Recommended)

1. Build and push your containers to Google Container Registry:
```bash
# For the frontend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/todo-frontend ./frontend

# For the backend
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/todo-backend ./backend
```

2. Deploy to Cloud Run:
```bash
# Deploy the backend
gcloud run deploy todo-backend \
    --image gcr.io/YOUR_PROJECT_ID/todo-backend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated

# Deploy the frontend
gcloud run deploy todo-frontend \
    --image gcr.io/YOUR_PROJECT_ID/todo-frontend \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars="NEXT_PUBLIC_API_URL=https://todo-backend-[YOUR_REGION].a.run.app"
```

## Step 5: Alternative - Using Minikube Locally

If you can't access cloud resources, you can run your application locally with Minikube:

1. Install Minikube (already in your project folder as minikube-installer.exe)
2. Start Minikube:
```bash
minikube start
```

3. Install Dapr:
```bash
dapr init
```

4. Deploy your application locally:
```bash
kubectl apply -f dapr/components/
helm install todo-app ./charts/todo-app
```

## Important Notes

1. GKE (Google Kubernetes Engine) is NOT part of the free tier
2. For Kubernetes specifically, you may need to use your free trial credits ($300) if you want to use GKE
3. Cloud Run is the most cost-effective way to run containers on GCP for free
4. Always monitor your usage to stay within free limits
5. Remember to shut down resources when not in use to avoid charges

## Troubleshooting

If you encounter issues with the free tier:
- Check your quota usage: gcloud compute project-info describe
- Verify your billing status: gcloud billing accounts list
- Make sure you're only using free-tier eligible resources

## Next Steps

1. Create your Google Cloud account using the free tier
2. Follow the steps above to deploy using Cloud Run
3. Test your application
4. Monitor your usage to stay within free limits