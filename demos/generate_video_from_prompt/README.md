## VEO Demo (Vertex AI) — Simple Text-to-Video

This demo generates a basic video from a text prompt using Google Veo on Vertex AI.

### Prerequisites
- GCP project with billing enabled
- Vertex AI API enabled: `gcloud services enable aiplatform.googleapis.com`
- Access to Veo models in your region (allowlist/eligibility may be required)
- Python 3.9+

### Install tools
- Install gcloud CLI:
  - Windows (winget): `winget install -e --id Google.CloudSDK --accept-package-agreements --accept-source-agreements --silent`
  - Windows (Chocolatey): `choco install googlecloudsdk -y`
  - macOS (Homebrew): `brew install --cask google-cloud-sdk`
  - Linux: follow `https://cloud.google.com/sdk/docs/install`

### Python deps
```bash
pip install -r requirements.txt
```

### Authenticate
```bash
# Sign in to gcloud (opens browser)
gcloud auth login

# Set up Application Default Credentials (opens browser)
gcloud auth application-default login

# (Optional) ensure Vertex AI API is enabled
gcloud services enable aiplatform.googleapis.com
```

### Configure defaults in gcloud (optional)
```bash
# Set default project and region (so you don’t have to pass them each time)
gcloud config set project YOUR_PROJECT_ID
gcloud config set ai/region us-central1

# If you see a quota project warning, set quota project for ADC:
gcloud auth application-default set-quota-project YOUR_PROJECT_ID

# Verify
gcloud config list
```

### Run
```bash
python demos/veo/generate_video.py --prompt "A cinematic drone shot over snowy mountains at sunrise" --count 3
```


