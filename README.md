# DeployMind Mini Agent System
A simplified deployment-error analysis system built with Google ADK and Gemini 2.5 Flash. This project uses a Sequential Agent workflow to automatically analyze logs, classify errors, suggest fixes, and validate them.

## What it does
Given raw deployment logs, the system performs the following steps automatically:
1. Analyzes the logs to extract key errors and summarize the issue.
2. Classifies the issue into a predefined category (Dependency, Build, Runtime, or Configuration Error).
3. Suggests potential fixes along with the reasoning behind them.
4. Validates the fixes to ensure they are relevant and not hallucinated, approving or rejecting them.

## Architecture
This project uses a `SequentialAgent` as the Orchestrator. The Orchestrator automatically runs the four `LlmAgents` in order and passes the data between them using ADK's session state (`output_key`).

The sequence is: log analysis -> issue classification -> fix suggestion -> validation

## Setup and Installation
Install Google ADK: pip install google-adk
Set env variable: $env:GOOGLE_API_KEY="YOUR_API_KEY" (windows powershell)
                  export GOOGLE_API_KEY="YOUR_API_KEY"

## To run:
1. Open terminal inside the root folder
2. run 'adk web' in your terminal
3. A browser interface will launch (usually hosted at http://localhost:8000)
4. Select deploymind as your target agent from the dropdown menu in the top-left corner.
5. Paste any deployment log into the chat box and press enter to start the analysis

## Sample logs for testing:
1. Dependency error
```
[2024-06-12 10:14:01] INFO  Starting deployment pipeline...
[2024-06-12 10:14:02] INFO  Installing Python dependencies from requirements.txt
[2024-06-12 10:14:08] ERROR Could not find a version that satisfies the requirement pandas==2.0.1
[2024-06-12 10:14:08] ERROR No matching distribution found for pandas==2.0.1
[2024-06-12 10:14:09] ERROR pip install failed with exit code 1
[2024-06-12 10:14:09] FATAL Build step 'install_dependencies' failed
```

2. Build error
```
[2024-06-12 11:02:33] INFO  Running TypeScript build...
[2024-06-12 11:02:34] INFO  tsc -p tsconfig.json
src/index.ts(15,7): error TS2322: Type 'string' is not assignable to type 'number'.
src/utils.ts(28,12): error TS2304: Cannot find name 'process'.
[2024-06-12 11:02:35] ERROR npm run build exited with code 2
[2024-06-12 11:02:35] FATAL Build step 'compile_frontend' failed
```

3. Configuration error
```
[2024-06-12 12:30:11] INFO  Starting application server...
[2024-06-12 12:30:11] INFO  Loading configuration from .env
[2024-06-12 12:30:12] ERROR Missing required environment variable: DATABASE_URL
[2024-06-12 12:30:12] ERROR Config validation failed
Traceback (most recent call last):
  File "app/config.py", line 42, in load_config
    raise ValidationError("Missing required environment variable: DATABASE_URL")
[2024-06-12 12:30:13] FATAL Application failed to start
```

