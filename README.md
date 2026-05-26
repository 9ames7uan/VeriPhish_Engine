# 🐟 VeriPhish Engine

VeriPhish Engine is a high-performance web service designed for real-time phishing message detection. It leverages a hybrid approach, combining **Rule-based Agents** with a **Machine Learning Classifier (TF-IDF + Logistic Regression)**, to provide multi-layered risk identification and assessment.

## 🚀 System Architecture

The project follows a modular design, ensuring the separation of data ingestion, model training, and API serving.

## 🛠 Tech Stack

* **Backend:** FastAPI
* **ML:** Scikit-learn (TF-IDF, Logistic Regression), Joblib
* **Data Management:** Pandas, CSV-based ingestion
* **Deployment:** Docker, Fedora Linux
* **Testing:** Pytest

## 📂 Project Structure

```text
.
├── data/               # Training datasets and user feedback logs
├── models/             # Exported .joblib ML models
├── scripts/            # Automation scripts (data init/augmentation)
├── src/                # Core business logic
│   ├── app.py          # FastAPI application entry point
│   ├── ml_engine.py    # ML inference engine
│   └── agents.py       # Rule-based agent system
├── tests/              # Unit tests (pytest)
└── Makefile            # Automation pipeline management

```

## ⚡ Quick Start

### 1. Setup Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

```

### 2. Initialize & Train

Use the `Makefile` to handle the training pipeline:

```bash
# Initialize data and train the model
make train

# Add new data and re-train
make update-model

```

### 3. Run Tests

Ensure the core logic is functioning correctly:

```bash
make test

```

### 4. Launch API

```bash
uvicorn src.app:app --reload

```

## 💡 Key Features

* **Multi-Layered Risk Assessment:** Blends heuristic rule-based agents with ML confidence scores.
* **Closed-Loop Learning:** Supports a `/api/feedback` endpoint to capture misclassified samples for future model refinement.
* **Automated MLOps:** Streamlined data management via Makefile, ensuring consistency between development and production environments.

