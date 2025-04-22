# Vulnerable FastAPI App with OWASP ZAP Scan

This project demonstrates a FastAPI application with intentional security vulnerabilities that can be detected by OWASP ZAP security scanning. It includes a GitHub Actions workflow to automate the scanning process.

## Project Structure

```
fastapi-zap-scan/
├── main.py                     # FastAPI application with vulnerabilities
├── requirements.txt            # Python dependencies
├── .github/
│   └── workflows/
│       └── zap-scan.yml        # GitHub Actions workflow for ZAP scanning
└── .zap-report/                # Directory for ZAP scan reports (after running locally)
```

## Vulnerabilities

The application contains the following intentional vulnerabilities:

1. **SQL Injection**: The user search functionality is vulnerable to SQL injection attacks
2. **Sensitive Data Exposure**: Hardcoded credentials and sensitive information
3. **Security Misconfiguration**: Insecure HTTP headers

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Docker (for running OWASP ZAP locally)
- Git (for version control)

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-zap-scan.git
   cd fastapi-zap-scan
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the FastAPI application:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

5. Access the application at http://localhost:8000

## Running OWASP ZAP Scan Locally

To run the ZAP scan locally and generate reports:

1. Ensure your FastAPI application is running on port 8000

2. Run OWASP ZAP using Docker:
   ```bash
   mkdir -p .zap-report
   docker run --rm -v $(pwd):/zap/wrk/:rw -t owasp/zap2docker-stable:latest \
   zap-full-scan.py -t http://host.docker.internal:8000 -g gen.conf -r .zap-report/zap-report.html -x .zap-report/zap-report.xml -J .zap-report/zap-report.json
   ```

3. View the generated reports in the `.zap-report` directory

## GitHub Actions Workflow

The included GitHub Actions workflow automates the OWASP ZAP scanning process.

### Triggering the Workflow

The workflow can be triggered in three ways:

1. **Automatically on push**: When code is pushed to the `main` branch
2. **Automatically on pull request**: When a pull request is created against the `main` branch
3. **Manually**: Using the GitHub Actions workflow dispatch feature

To trigger the workflow manually:
1. Go to your GitHub repository
2. Click on the "Actions" tab
3. Select the "OWASP ZAP Security Scan" workflow
4. Click "Run workflow" and select the branch to run it on

### Viewing Workflow Results

After the workflow runs:

1. Go to the "Actions" tab in your GitHub repository
2. Click on the completed workflow run
3. Scroll down to the "Artifacts" section
4. Download the artifacts:
   - `zap-html-report`: HTML report with detailed findings
   - `zap-json-report`: JSON report for programmatic analysis
   - `zap-xml-report`: XML report for integration with other tools

### Understanding the Reports

The ZAP scan reports contain:

1. **Alerts**: Security issues found in the application
2. **Risk Levels**: High, Medium, Low, or Informational
3. **Evidence**: Details about how the vulnerability was detected
4. **Solutions**: Recommendations for fixing the issues

## Testing the Vulnerabilities

### SQL Injection

1. Go to http://localhost:8000/user-search
2. Enter `admin' OR '1'='1` in the search field
3. Submit the form
4. You should see all users in the database, demonstrating the SQL injection vulnerability

### Sensitive Data Exposure

1. Go to http://localhost:8000/sensitive-data
2. You'll see exposed API keys, passwords, and internal server information

## Security Best Practices

In a real-world application, you should:

1. Use parameterized queries or an ORM to prevent SQL injection
2. Never expose sensitive data in the application
3. Implement proper security headers
4. Regularly scan your application for vulnerabilities

## Disclaimer

This application contains intentional security vulnerabilities for educational purposes. Do not use any part of this code in production environments.
