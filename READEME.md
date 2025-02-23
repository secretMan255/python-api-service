# Introduce

This is a python Quart api backend service that connect with mysql databse [frontend](https://github.com/secretMan255/hardware-admin-portal)

#Setup Instructions

Create store procedure sql query and create database and table [srcipt](https://github.com/secretMan255/python-api-service/tree/master/db)

Set environment variable

-    HOST: API host
-    PORT: API port
-    ALLOWED_ORIGINS: cros origins
-    SECRET_KEY: API secret

-    DB_HOST: Database host
-    DB_PORT: Database port
-    DB_USER: Database user
-    DB_PASS: Database pass
-    DB_NAME: Database user
-    INSTANCE_CONNECTION_NAME: Database sql connection instance
-    BUCKET: Google storage bucket name

Install Dependencies
Dependencies is in the requirements.txt

```
pip install
```

Start the Project
cd to src

```
python3 app.service.py
```

# Deployment

Create a Dockerfile in root path (already provided)

```
# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app/src

# Copy dependency file
COPY requirements.txt /app/src/requirements.txt

# Copy application files (fixing the issue)
COPY src/ /app/src/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your application runs on
EXPOSE 8080

# Command to run the application (update to match your file)
CMD ["python", "app.service.py"]
```

Create script (googleDeploy.sh) at root path if u want to deploy on google cloud run
Start Deploy

```
./googleDeploy.sh
```

Script

```
#!/bin/bash

# Define environment variables
GOOGLE_PROJECT_ID=""
CLOUD_RUN_SERVICE=""
ALLOWED_ORIGINS=''
SECRET_KEY=''
DB_HOST=''
DB_PORT=''
DB_USER=''
DB_PASS=''
DB_NAME=''
INSTANCE_CONNECTION_NAME=""
BUCKET=''

# Step 1: Deploy to Google Cloud Run using your Docker Hub image
gcloud run deploy $CLOUD_RUN_SERVICE \
     --image= \
     --add-cloudsql-instances=$INSTANCE_CONNECTION_NAME \
     --update-env-vars=ALLOWED_ORIGINS=$ALLOWED_ORIGINS,SECRET_KEY=$SECRET_KEY,DB_HOST=$DB_HOST,DB_USER=$DB_USER,DB_PASS=$DB_PASS,DB_NAME=$DB_NAME,DB_POST=$DB_PORT,INSTANCE_CONNECTION_NAME=$INSTANCE_CONNECTION_NAME,BUCKET=$BUCKET \
     --platform=managed \
     --region=asia-southeast1 \
     --allow-unauthenticated \
     --project=$GOOGLE_PROJECT_ID \
     # --set-secrets GOOGLE_APPLICATION_CREDENTIALS=google-service-account:latest \
```
