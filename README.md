# Deploy Firebase Python Functions

A GitHub Action for deploying Python-based Firebase Cloud Functions. This repository serves as both the action implementation and a live example of its usage.

## Features

- 🐍 Automatic Python version detection from pyproject.toml
- 📦 Dependency management using UV package manager
- 🔄 Environment-based deployments (staging/prod)
- 🔐 Secure handling of service account credentials
- 📝 Detailed deployment summaries
- 🧪 Self-testing repository structure

## Repository Structure

This repository is structured to serve two purposes:

1. Provide the composite action implementation
2. Serve as a live example and test environment

```
.
├── action.yml           # The composite action definition
├── .github/workflows/   # Contains workflow using the action
│   └── deploy-functions.yml
├── functions/          # Example Firebase Functions
│   ├── main.py
│   └── pyproject.toml
└── README.md          # Documentation
```

## Usage

The workflow in this repository (.github/workflows/deploy-functions.yml) demonstrates the recommended usage:

```yaml
name: Test & Deploy Python Functions

on:
  push:
    branches: [staging, prod]
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [staging, prod]
        description: 'Environment to deploy to'
        required: true

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - uses: ./ # Uses local action for testing
        with:
          environment: ${{ github.event_name == 'push' && github.ref_name || inputs.environment }}
          service_account_json: ${{ secrets[format('FIREBASE_{0}_SERVICE_ACCOUNT', github.event_name == 'push' && github.ref_name || inputs.environment)] }}
          project_id: ${{ vars[format('FIREBASE_{0}_PROJECT_ID', github.event_name == 'push' && github.ref_name || inputs.environment)] }}
```

When using in your own repository, reference a specific version:

```yaml
- uses: digital-wisdom/deploy-firebase-python@v1
  with:
    functions_dir: 'src/functions' # Default is 'functions'
    environment: staging
    service_account_json: ${{ secrets.FIREBASE_STAGING_SERVICE_ACCOUNT }}
    project_id: my-project-staging
```

## Inputs

| Input                  | Description                                       | Required | Default     |
| ---------------------- | ------------------------------------------------- | -------- | ----------- |
| `functions_dir`        | Directory containing functions and pyproject.toml | No       | `functions` |
| `environment`          | Environment to deploy to (staging/prod)           | Yes      | N/A         |
| `service_account_json` | Firebase service account JSON                     | Yes      | N/A         |
| `project_id`           | Firebase project ID                               | Yes      | N/A         |

## Prerequisites

1. **Firebase Project Setup**

   - Create Firebase projects for your environments
   - Generate service account keys
   - Store service account JSON in GitHub Secrets
   - Store project IDs in GitHub Variables

2. **Python Project Structure**
   - Valid pyproject.toml in your functions directory
   - Python version specified in requires-python
   - Dependencies listed in project dependencies

## Project Structure

Your project should look something like this:

```
.
├── .github
│   └── workflows
│       └── deploy.yml
├── functions
│   ├── main.py
│   ├── pyproject.toml
│   └── other_files.py
└── firebase.json
```

## Environment Variables

The action automatically sets up:

- `GOOGLE_APPLICATION_CREDENTIALS`: Points to the service account file
- Firebase project configuration via `firebase use`

## Security

- Service account credentials are securely handled and cleaned up
- Credentials file is automatically removed after deployment
- Uses GitHub's secure token handling

## Versioning

This action follows semantic versioning. You can use it in three ways:

- Major version: `@v1` - Recommended for stability
  ```yaml
  - uses: digital-wisdom/deploy-firebase-python@v1
  ```
- Specific version: `@v1.0.0` - Pinned to exact version
  ```yaml
  - uses: digital-wisdom/deploy-firebase-python@v1.0.0
  ```
- Branch: `@main` - Latest changes (not recommended for production)
  ```yaml
  - uses: digital-wisdom/deploy-firebase-python@main
  ```

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Use [Conventional Commits](https://www.conventionalcommits.org/) for commit messages:

   - `feat: add new feature`
   - `fix: resolve bug`
   - `docs: update documentation`
   - `chore: maintenance tasks`

2. Changes will automatically:
   - Generate release notes
   - Update the changelog
   - Create a new version
   - Update major version tag

## License

This project is licensed under the MIT License - see the LICENSE file for details.
