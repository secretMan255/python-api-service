#!/bin/bash

# Define environment variables
GOOGLE_PROJECT_ID=
CLOUD_RUN_SERVICE=
ALLOWED_ORIGINS=
SECRET_KEY=
DB_HOST=
DB_PORT=
DB_USER=
DB_PASS=
DB_NAME=
INSTANCE_CONNECTION_NAME=
BUCKET=

# Step 1: Deploy to Google Cloud Run using your Docker Hub image
gcloud run deploy $CLOUD_RUN_SERVICE \
     --image=docker.io/yapyiliang2001/python-api-service:latest \
     --add-cloudsql-instances=$INSTANCE_CONNECTION_NAME \
     --update-env-vars=ALLOWED_ORIGINS=$ALLOWED_ORIGINS,SECRET_KEY=$SECRET_KEY,DB_HOST=$DB_HOST,DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_NAME=$DB_NAME,INSTANCE_CONNECTION_NAME=$INSTANCE_CONNECTION_NAME,BUCKET=$BUCKET \
     --platform=managed \
     --region=asia-southeast1 \
     --allow-unauthenticated \
     --project=$GOOGLE_PROJECT_ID \
     # --set-secrets GOOGLE_APPLICATION_CREDENTIALS=google-service-account:latest \
    
