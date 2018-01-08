.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: clean
clean:
	@echo "$(shell ./bin/clean.sh)"

.PHONY: vcc_all
vcc_all:
	python hpcc/vcc-combine.py 'vcc_data.npz'

.PHONY: vcc_debug
vcc_debug:
	python hpcc/vcc-combine.py

default:
	python hpcc/vcc-combine.py
