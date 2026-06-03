import pandas as pd
import os
import shutil

def approve_feedback():
    pending_path = "data/pending_feedback.csv"
    approved_path = "data/approved_feedback.csv"

    if not os.path.exists(pending_path):
        print("ℹ️ 目前沒有待審核的回饋。")
        return

    df = pd.read_csv(pending_path)
    
    to_keep = []
    
    print(f"--- 開始審核 (共 {len(df)} 筆資料) ---")
    
    for index, row in df.iterrows():
        print(f"\n[訊息內容]: {row['message']}")
        print(f"[類型]: {row['input_type']} | [預測]: {row['predicted_label']} -> [實際]: {row['correct_label']}")
        print(f"[原因]: {row['reason']}")
        
        choice = input("是否批准加入訓練集？(y/n/q): ").lower()
        
        if choice == 'y':
            to_keep.append(row)
            print("✅ 已加入核准清單。")
        elif choice == 'q':
            print("🛑 審核中止。")
            return
        else:
            print("🗑️ 已忽略該筆回饋。")

    if to_keep:
        new_approved_df = pd.DataFrame(to_keep)
        
        if os.path.exists(approved_path):
            existing_approved = pd.read_csv(approved_path)
            new_approved_df = pd.concat([existing_approved, new_approved_df]).drop_duplicates()
            
        new_approved_df.to_csv(approved_path, index=False, encoding="utf-8-sig")
        print(f"\n🎉 審核完成！共 {len(new_approved_df)} 筆資料已儲存至 approved_feedback.csv。")
    
    with open(pending_path, 'w', encoding='utf-8-sig') as f:
        pd.DataFrame(columns=["timestamp", "message", "input_type", "predicted_label", "correct_label", "reason"]).to_csv(f, index=False)
    print(f"🧹 已清空 {pending_path}，檔案結構已保留。")

if __name__ == "__main__":
    approve_feedback()
