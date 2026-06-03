import csv
import os
from datetime import datetime

FEEDBACK_PATH = "data/pending_feedback.csv"

def save_feedback(content: str, input_type: str, predicted_label: str, correct_label: str, reason: str):
    file_exists = os.path.exists(FEEDBACK_PATH)

    with open(FEEDBACK_PATH, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "message", "input_type", "predicted_label", "correct_label", "reason"
        ])
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "message": content,
            "input_type": input_type,
            "predicted_label": predicted_label,
            "correct_label": correct_label,
            "reason": reason
        })
