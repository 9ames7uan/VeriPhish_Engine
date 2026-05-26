.PHONY: init train clean test

init:
	python3 scripts/init_data.py

add-data:
	python3 scripts/add_data.py

train: init
	python3 src/train.py

update-model: add-data train

test:
	pytest tests/

clean:
	rm -rf models/*.joblib data/*.csv
