# Robust REST API Testing Framework

A clean REST API testing framework built with **Pytest**, **FastAPI**, and **Pydantic**. 

This repository includes an embedded mock service to guarantee **deterministic state execution**, **strict schema validation**, and **zero external network flakiness** in CI/CD.

---

## Architecture & Design Trade-offs

| Engineering Choice | Motivation | Business / QA Value |
| :--- | :--- | :--- |
| **In-Memory Mock API (FastAPI)** | Decouples tests from external public APIs with rate limits. | 100% deterministic runs; total suite runtime under **0.5s**. |
| **Direct Memory Execution (`TestClient`)** | Runs HTTP assertions directly in-process via `httpx`. | Eliminates open port conflicts, process hanging, and OS socket leakage. |
| **Contract Validation via Pydantic** | Validates field types and required structures at the schema layer. | Fail-fast on protocol/format mismatches (HTTP 422) without fragile JSON key checks. |
| **Single Concept per Test** | Validates status code, payload contract, and data persistence in one flow. | Eliminates redundant network calls; reduces execution time and CI compute costs. |

---

## Getting started
### Prerequisites
Python 3.11 or higher

Git

### Clone & Set Up Environment

```text
git clone [https://github.com/TWOJ_USER/api-testing-framework.git](https://github.com/TWOJ_USER/api-testing-framework.git)
cd api-testing-framework

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Execute Test Suite

```text
# Run tests with short traceback output
pytest

# Run tests with standalone HTML report generation
pytest --html=reports/report.html --self-contained-html
```

### Run Standalone Mock Server (Optional)

To inspect the automatically generated interactive OpenAPI documentation:
```text
uvicorn mock_server.mock_app:app --reload --port 8000
```