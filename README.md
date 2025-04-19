# Deploy Python Firebase Functions with GitHub Actions
This project contains a sample workflow for automating the deployment of a Python Firebase Function with GitHub Actions. The Firebase files and Python code deploy a simple hello world function with Flask as a Firebase serverless Function. Note that Python 3.11 is the latest version supported by Python Firebase Functions v2 as of April 2025.

# GitHub Actions Trigger
The action is triggered from any push to the feature branch `add-deploy-workflow` or a manual trigger. The default for the feature branch is `staging`. The manual trigger allows the user to select a GitHub branch and Firebase alias `staging`/`prod`.

# Python package manager
The project uses `uv`, a modern package manager, which creates a virtual environment named `.venv`. Firebase expects a virtual environment named `venv` with `pip` installed. We can use `uv` commands to do so. Note that we are running `uv sync` with the `--active` flag because we need to maintain two virtual environments: `venv` for Firebase and the default `.venv` for uv.

# GCP Service Account
Deployment depends upon a Google Cloud service account for authentication. Set this up in the GCP console by creating a dedicated service account for GitHub Actions. You'll need to do this for each Firebase project.

GCP console > IAM & Admin > Service Accounts > Create Service Account
Name: github-actions-deploy-staging
Description: Deploy to Firebase with GitHub Actions
Roles:
- Firebase Admin SDK Admin
- Cloud Functions Admin
- Service Account User
Skip granting users access and click Done.

Alternatively, use `gcloud` CLI for each project:

`gcloud config set project PROJECT_ID`

`gcloud iam service-accounts create github-actions-deploy \`
`  --description="Deploy to Firebase project with GitHub Actions" \`

`gcloud projects add-iam-policy-binding $(gcloud config get-value project) \`
`  --member="serviceAccount:github-actions-deploy@$(gcloud config get-value project).iam.gserviceaccount.com" \`
`  --role="roles/firebase.admin"`

`gcloud projects add-iam-policy-binding $(gcloud config get-value project) \`
`  --member="serviceAccount:github-actions-deploy@$(gcloud config get-value project).iam.gserviceaccount.com" \`
`  --role="roles/cloudfunctions.admin"`

`gcloud projects add-iam-policy-binding $(gcloud config get-value project) \`
`  --member="serviceAccount:github-actions-deploy@$(gcloud config get-value project).iam.gserviceaccount.com" \`
`  --role="roles/iam.serviceAccountUser"`

`gcloud projects add-iam-policy-binding $(gcloud config get-value project) \`
`  --member="serviceAccount:github-actions-deploy@$(gcloud config get-value project).iam.gserviceaccount.com" \`
`  --role="roles/serviceusage.serviceUsageConsumer"`

`gcloud projects add-iam-policy-binding $(gcloud config get-value project) \`
`  --member="serviceAccount:github-actions-deploy@$(gcloud config get-value project).iam.gserviceaccount.com" \`
`  --role="roles/cloudruntimeconfig.admin"`

# GCP Authentication Keys
Each Firebase project requires a service account key. Download keys from Google and remember to exclude them from version control.

Store the keys as secrets in your repo:
GitHub repo → Settings → Secrets and variables → Actions
FIREBASE_PROD_SERVICE_ACCOUNT
FIREBASE_STAGING_SERVICE_ACCOUNT

Alternatively, use GitHub CLI:
`gh secret set FIREBASE_STAGING_SERVICE_ACCOUNT --repo user/repo-name < key-staging.json`
`gh secret set FIREBASE_PROD_SERVICE_ACCOUNT --repo user/repo-name < key-prod.json`

# Firebase CLI
It’s important to use the latest version of `firebase-tools`, which will automatically enable the correct APIs for the Python Firebase Function in the corresponding GCP project.

# Debugging and Credential Verification
The steps labeled (Debug) are for debugging, verifying credentials, and checking settings, so they can be omitted. The `firebase deploy` command uses a `--debug` flag that isn't strictly necessary. The GitHub Actions workflow would run faster without the debugging steps and flags.