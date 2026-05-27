# VeriPhish Engine Makefile
.PHONY: init add-data train retrain-all update-model test clean

train:
	python3 src/train.py

update-model: retrain-all

init:
	python3 scripts/init_data.py

add-data:
	python3 scripts/add_data.py

retrain-all:
	@echo "--- [1/2] 正在檢查審核區 ---"
	python3 scripts/train_model.py
	@echo "--- [2/2] 正在重新訓練模型 ---"
	python3 src/train.py

test:
	pytest tests/

clean:
	rm -f models/*.joblib
	@echo "✅ 環境已清理，保留核心數據庫。"
