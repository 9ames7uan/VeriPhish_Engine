# VeriPhish Engine Makefile
.PHONY: init add-data train retrain-all merge-only train-only test clean

init:
	python3 scripts/init_data.py

add-data:
	python3 scripts/add_data.py

retrain-all:
	@echo "--- [1/2] 正在檢查審核區 ---"
	@echo "請務必確保 data/pending_feedback.csv 已審核並更名為 data/approved_feedback.csv"
	python3 scripts/train_model.py
	@echo "--- [2/2] 正在重新訓練模型 ---"
	python3 src/train.py

train-only:
	python3 src/train.py

test:
	pytest tests/

clean:
	rm -f models/*.joblib
	@echo "✅ 環境已清理，保留核心數據庫。"
