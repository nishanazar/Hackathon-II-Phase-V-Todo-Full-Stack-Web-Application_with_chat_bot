@echo off
REM Batch script to deploy the Todo application to Google Cloud Run (free tier option)

echo Starting deployment to Google Cloud Run...

REM Variables - Update these with your values
set PROJECT_ID=gen-lang-client-0071684271
set REGION=us-central1
set IMAGE_NAME_FRONTEND=todo-frontend
set IMAGE_NAME_BACKEND=todo-backend
set IMAGE_TAG=latest

REM Set the project
gcloud config set project %PROJECT_ID%

REM Enable required APIs for Cloud Run
echo Enabling required APIs for Cloud Run...
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
gcloud services enable cloudbuild.googleapis.com

REM Build and push Docker images to Google Container Registry using Cloud Build
echo Building and pushing Docker images using Cloud Build...
gcloud builds submit --tag gcr.io/%PROJECT_ID%/%IMAGE_NAME_FRONTEND%:%IMAGE_TAG% ./frontend
gcloud builds submit --tag gcr.io/%PROJECT_ID%/%IMAGE_NAME_BACKEND%:%IMAGE_TAG% ./backend

REM Deploy the backend service to Cloud Run
echo Deploying backend service to Cloud Run...
gcloud run deploy %IMAGE_NAME_BACKEND% ^
    --image gcr.io/%PROJECT_ID%/%IMAGE_NAME_BACKEND%:%IMAGE_TAG% ^
    --platform managed ^
    --region %REGION% ^
    --allow-unauthenticated ^
    --port 8000 ^
    --memory 512Mi ^
    --cpu 1

REM Get the backend service URL
for /f %%i in ('gcloud run services list --platform managed --region %REGION% --format="value(status.url)" --filter="metadata.name=%IMAGE_NAME_BACKEND%"') do set BACKEND_URL=%%i
echo Backend service deployed at: %BACKEND_URL%

REM Deploy the frontend service to Cloud Run
echo Deploying frontend service to Cloud Run...
gcloud run deploy %IMAGE_NAME_FRONTEND% ^
    --image gcr.io/%PROJECT_ID%/%IMAGE_NAME_FRONTEND%:%IMAGE_TAG% ^
    --platform managed ^
    --region %REGION% ^
    --allow-unauthenticated ^
    --port 3000 ^
    --memory 512Mi ^
    --cpu 1 ^
    --set-env-vars="NEXT_PUBLIC_API_URL=%BACKEND_URL%"

REM Get the frontend service URL
for /f %%i in ('gcloud run services list --platform managed --region %REGION% --format="value(status.url)" --filter="metadata.name=%IMAGE_NAME_FRONTEND%"') do set FRONTEND_URL=%%i
echo Frontend service deployed at: %FRONTEND_URL%

echo Deployment completed successfully!
echo Your application is available at: %FRONTEND_URL%
echo.
echo Note: As part of the free tier, your services may experience some limitations:
echo - Cloud Run offers 2 million requests per month for free
echo - Services may sleep after periods of inactivity
echo - Limited CPU and memory resources
echo.
echo To avoid charges, delete the services when not in use:
echo gcloud run services delete %IMAGE_NAME_FRONTEND% --platform managed --region %REGION%
echo gcloud run services delete %IMAGE_NAME_BACKEND% --platform managed --region %REGION%