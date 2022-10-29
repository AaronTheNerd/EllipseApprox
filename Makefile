PY := pipenv run python
SRC_DIR := perimeter_approximation
WARN_FLAGS := -W error::RuntimeWarning


all: data configs approximates test_approx plot


run:
	$(PY) $(WARN_FLAGS) $(SRC_DIR)/main.py


data:
	$(PY) $(SRC_DIR)/data.py


configs:
	$(PY) $(SRC_DIR)/configs.py


approximates:
	$(PY) $(SRC_DIR)/approximates.py


test_approx:
	$(PY) $(SRC_DIR)/test_approx.py


plot:
	$(PY) $(SRC_DIR)/plot.py


clean:
	rm output/*
