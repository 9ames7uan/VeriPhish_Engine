# VeriPhish Engine Makefile
.PHONY: init add-data train approve-feedback merge-and-train test clean

# 初始化資料庫
init:
	python3 scripts/init_data.py

# 從外部 CSV 新增資料
add-data:
	python3 scripts/add_data.py data/new_data.csv

# 審核回饋資料
approve-feedback:
	python3 scripts/approve_feedback.py

# 執行審核後的合併與重訓流程 (一鍵閉環)
merge-and-train:
	python3 scripts/merge_feedback.py
	python3 scripts/train.py

# 純訓練指令
train:
	python3 scripts/train.py

# 執行測試
test:
	PYTHONPATH=. pytest tests/

# 清理模型檔案
clean:
	rm -f models/*.joblib
	@echo "✅ 環境已清理，模型檔案已移除。"
