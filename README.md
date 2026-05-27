# 🐟 VeriPhish Engine

VeriPhish Engine is an industrial-grade, high-performance web service engineered for real-time phishing detection. It utilizes a **Hybrid Detection Architecture** that integrates **Heuristic Rule-based Agents** with a **Machine Learning Classifier (TF-IDF + Logistic Regression)** to deliver multi-layered risk identification and continuous learning capabilities.

## ⚙️ Engineering Philosophy

This project adheres to professional software engineering standards, prioritizing:

* **Decoupling:** Strict separation of concerns between business logic, model inference, and data processing.
* **Closed-Loop Learning:** A Human-in-the-Loop (HITL) pipeline that translates user feedback into actionable model improvements.
* **MLOps Automation:** Leveraging a `Makefile` to implement a **Declarative Pipeline**, ensuring environment parity and system reproducibility.

## 🛠 Tech Stack

* **Core:** Python 3.11+, FastAPI
* **ML Pipeline:** Scikit-learn (TF-IDF, Logistic Regression), Joblib
* **Data Ops:** Pandas, CSV-based Staging & Gold Standard architecture
* **DevOps:** Docker, Fedora Workstation (Intel-based), Makefile automation
* **Quality Assurance:** Pytest

## 📂 Project Structure

```text
VeriPhish_Engine/
├── data/               # Data management hub (Staging and Gold Standard)
├── models/             # Serialized ML model artifacts (.joblib)
├── scripts/            # Automation and data engineering scripts
├── src/                # Core business logic and API service
├── tests/              # Automated regression testing (Pytest)
├── Makefile            # Declarative automation pipeline entry point
└── Dockerfile          # OCI-compliant container configuration

```

## ⚡ Quick Start

### 1. Environment Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 2. Automation Pipeline (Makefile)

The project utilizes `Makefile` to encapsulate complex workflows:

```bash
# Initialize project data
make init

# Execute regression tests
make test

# Train the model (standardized pipeline)
make train

# Merge verified feedback and re-train (closed-loop)
make update-model

```

### 3. Launch Service

```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000

```

## 💡 Key Features

* **Hybrid Defense Mechanism:** Blends the immediate logic of rule-based agents with the statistical pattern recognition of ML models to improve resilience against novel phishing tactics.
* **HITL Data Integrity Pipeline:** Implements a dual-stage data handling process (Staging vs. Gold Standard) to mitigate overfitting and data poisoning risks.
* **Operational Reproducibility:** Through Docker and dynamic path resolution, the engine maintains high portability across Fedora and other Linux distributions.

