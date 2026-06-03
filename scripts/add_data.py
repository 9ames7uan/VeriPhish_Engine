import pandas as pd
import os
import shutil
import sys
import glob
from datetime import datetime

def add_new_data(input_csv_path="data/new_data.csv"):
    main_path = "data/phishing_training_data.csv"
    archive_dir = "data/archive"

    if not os.path.exists(main_path):
        print(f"❌ 找不到主資料檔案: {main_path}")
        return

    if not os.path.exists(input_csv_path):
        print(f"❌ 找不到來源檔案: {input_csv_path}")
        return

    backup_path = f"data/phishing_training_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.bak"
    shutil.copy(main_path, backup_path)
    print(f"📦 已建立資料備份: {backup_path}")

    backups = sorted(glob.glob("data/phishing_training_data_*.bak"), reverse=True)
    if len(backups) > 3:
        for old_backup in backups[3:]:
            os.remove(old_backup)
            print(f"🧹 已刪除舊備份: {old_backup}")

    df_main = pd.read_csv(main_path)
    df_new = pd.read_csv(input_csv_path)

    existing_messages = df_main["message"].tolist()
    df_new_filtered = df_new[~df_new["message"].isin(existing_messages)]

    if not df_new_filtered.empty:
        df_combined = pd.concat([df_main, df_new_filtered], ignore_index=True)
        df_combined.to_csv(main_path, index=False, encoding="utf-8-sig")
        print(f"✅ 成功新增 {len(df_new_filtered)} 筆新資料。")
        
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
            
        archive_name = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        shutil.copy(input_csv_path, os.path.join(archive_dir, archive_name))
        
        with open(input_csv_path, 'w', encoding='utf-8-sig') as f:
            f.truncate()
            df_new.head(0).to_csv(f, index=False, encoding='utf-8-sig')
            
        print(f"📂 資料已歸檔至: {os.path.join(archive_dir, archive_name)}，並已清空 new_data.csv")
    else:
        print("ℹ️ 沒有新資料需要加入 (資料已存在)。")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_new_data(sys.argv[1])
    else:
        add_new_data()
