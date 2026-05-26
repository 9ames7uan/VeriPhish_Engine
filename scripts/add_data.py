import pandas as pd
import os

def add_new_data():
    path = "data/phishing_training_data.csv"

    if not os.path.exists(path):
        print(f"❌ 找不到檔案: {path}，請先執行 make init")
        return

    df = pd.read_csv(path)

    new_data = [
        {"message": "您的信用卡付款失敗，請立即點擊 http://secure-card-update.com 更新卡號與CVV。", "input_type": "SMS", "label": "RED", "scam_type": "信用卡釣魚"},
        {"message": "檢察官通知您涉及洗錢案件，請保持通話並依照指示轉帳到安全帳戶。", "input_type": "LINE", "label": "RED", "scam_type": "假檢警詐騙"},
        {"message": "您好，明天課程改到線上，連結稍後由老師公告。", "input_type": "LINE", "label": "GREEN", "scam_type": "正常課程通知"},
        {"message": "您的會員資料可能需要更新，請留意官方通知。", "input_type": "Email", "label": "YELLOW", "scam_type": "疑似資料更新通知"}
    ]

    df_new = pd.DataFrame(new_data)

    existing_messages = df["message"].tolist()
    df_new = df_new[~df_new["message"].isin(existing_messages)]

    if not df_new.empty:
        df = pd.concat([df, df_new], ignore_index=True)
        df.to_csv(path, index=False, encoding="utf-8-sig")
        print(f"✅ 成功新增 {len(df_new)} 筆新資料。")
    else:
        print("ℹ️ 沒有新資料需要加入 (資料已存在)。")

if __name__ == "__main__":
    add_new_data()
