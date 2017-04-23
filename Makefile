LOG_DIR = "logs"

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: clean
clean:
	[[ ! -d "${LOG_DIR}" ]] && mkdir -p ${LOG_DIR}
	[[ -e "figure_*.png" ]] && mv -f {figure_*.png} ${LOG_DIR}
	[[ -e "boot.sh.o*" ]] && mv -f {boot.sh.o*} ${LOG_DIR}

.PHONY: vcc_all
vcc_all:
	python hpcc/vcc-combine.py 'vcc_data.npz'

.PHONY: vcc_debug
vcc_debug:
	python hpcc/vcc-combine.py

default:
	python hpcc/vcc-combine.py
