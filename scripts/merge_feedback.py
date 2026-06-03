import pandas as pd
import os

def merge_approved_feedback():
    training_path = "data/phishing_training_data.csv"
    approved_path = "data/approved_feedback.csv"

    if not os.path.exists(approved_path):
        print("ℹ️ 沒有已批准的回饋資料，跳過合併。")
        return

    training_df = pd.read_csv(training_path)
    approved_df = pd.read_csv(approved_path)

    new_data = pd.DataFrame({
        "message": approved_df["message"],
        "input_type": approved_df["input_type"],
        "label": approved_df["correct_label"],
        "scam_type": approved_df["reason"]
    })

    combined_df = pd.concat([training_df, new_data], ignore_index=True)
    combined_df = combined_df.drop_duplicates(subset=["message", "input_type", "label"])

    combined_df.to_csv(training_path, index=False, encoding="utf-8-sig")
    print(f"✅ 已將 {len(new_data)} 筆審核通過的資料合併。目前總筆數：{len(combined_df)}")

if __name__ == "__main__":
    merge_approved_feedback()
