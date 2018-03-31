#!/usr/bin/env bash

#PBS -j oe -l select=1 -M s1510756@jaist.ac.jp -m e
cd $PBS_O_WORKDIR

conda create --yes --prefix $HOME/py27 python=2.7
source activate $HOME/py27

APP_DIR="${HOME}/hpcc"
LOG_DIR="${HOME}/logs"
TARGET_DATA="vcc_data.npz"
#TARGET_DATA="vcc_data_40x800.npz"

[[ -d "${LOG_DIR}" ]] || mkdir ${LOG_DIR}

TASK_ID="$(date +%s)"
TASK_OUTPUT="figure_${TASK_ID}_pr.png"

#PATCH_MODE="RESERVED_WORD_ONLY"
#PATCH_MODE="LINE_TYPE_SENSITIVE"
PATCH_MODE="LINE_TYPE_INSENSITIVE"

cat ${APP_DIR}/message.txt \
  && echo '' > ${APP_DIR}/message.txt \
  && pip install -qr ${APP_DIR}/requirements.txt \
  && time python ${APP_DIR}/vcc-combine.py -f ${TARGET_DATA} -o 1 -i "${TASK_ID}" -m "${PATCH_MODE}" \
  && sh ${HOME}/bin/clean.sh

if [[ $(find "${LOG_DIR}" -type f -name "${TASK_OUTPUT}" | wc -l) -ge 1 ]]; then
  ${HOME}/pushbullet-bash/pushbullet push all file "${LOG_DIR}/${TASK_OUTPUT}" "Task #${TASK_ID} completed"
else
  ${HOME}/pushbullet-bash/pushbullet push all note "History-based Vulnerability Detector" "Task #${TASK_ID} completed"
fi
