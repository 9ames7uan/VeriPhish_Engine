# VeriPhish Engine: Multi-Agent Neural Scam Detection

## Project Overview
VeriPhish Engine is an automated cybersecurity platform designed to detect and mitigate social engineering threats. It leverages a **Multi-Agent Architecture** combined with machine learning classification to analyze suspicious messages (LINE, SMS, Email) for potential phishing risks in real-time.



## Key Features
- **Source Identifier Agent:** Analyzes sender authenticity and impersonation attempts.
- **Semantic Analyzer Agent:** Uses NLP to detect urgency, threat, or financial manipulation patterns.
- **Link Validator Agent:** Parses URLs and identifies suspicious domains or sensitive data requests.
- **Orchestrator:** Integrates multi-agent analysis to output a standardized risk score (Red/Yellow/Green).
- **Feedback Loop:** Enables continuous model improvement through user-contributed labels.

## System Architecture
The system employs a layered defense strategy:
1. **Heuristic Layer:** Rule-based detection for immediate threat signals.
2. **Neural Layer:** Scikit-learn Logistic Regression trained on categorized phishing datasets.
3. **API Layer:** FastAPI-powered asynchronous backend for low-latency analysis.

## License

This project is licensed under the MIT License. See `LICENSE.md` for details.

```
