# 🐟 VeriPhish Engine

VeriPhish Engine is an industrial-grade, high-performance web service engineered for real-time phishing detection. It utilizes a **Hybrid Detection Architecture** that integrates **Heuristic Rule-based Agents** with a **Machine Learning Classifier (TF-IDF + Logistic Regression)** to deliver multi-layered risk identification and continuous learning capabilities.

## ⚙️ Engineering Philosophy

This project adheres to professional software engineering standards, prioritizing:

* **Clean Architecture:** Strict separation between Data Engineering (`scripts/`) and ML Engineering (`src/`).
* **Closed-Loop Learning:** A Human-in-the-Loop (HITL) pipeline that enables manual verification of model feedback before model retraining.
* **MLOps Automation:** Leveraging a `Makefile` as a **Declarative Pipeline**, ensuring system reproducibility, automatic data archival, and database self-recovery.

## 🛠 Tech Stack

* **Core:** Python 3.14+, FastAPI
* **ML Pipeline:** Scikit-learn (TF-IDF, Logistic Regression), Joblib
* **Data Ops:** Pandas, Persistent Staging-to-Production pipeline
* **DevOps:** Fedora Workstation, Makefile automation
* **Quality Assurance:** Pytest

## 📂 Project Structure

```text
VeriPhish_Engine/
├── data/               # Persistent data hub (Archive, Pending/Approved Feedback, Gold Standard)
├── models/             # Serialized ML model artifacts (.joblib)
├── scripts/            # ETL pipeline, Data Engineering, and Training scripts
├── src/                # Core business logic and FastAPI service
├── tests/              # Automated regression testing (Pytest)
└── Makefile            # Declarative automation pipeline entry point

```

## ⚡ Quick Start

### 1. Automation Pipeline (Makefile)

The project encapsulates complex data workflows into simple commands:

| Command | Description |
| --- | --- |
| `make init` | Initializes project data and recovers state from archives/approved feedback |
| `make add-data` | Ingests new data samples from staging (`new_data.csv`) into the pipeline |
| `make approve-feedback` | Interactively reviews and approves pending user feedback |
| `make merge-and-train` | Merges approved feedback into the training set and re-trains the model |
| `make test` | Executes regression tests to ensure system stability |

### 2. Launch Service

```bash
# Start the API service
uvicorn src.app:app --reload
```
