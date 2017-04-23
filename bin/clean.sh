#!/usr/bin/env bash
WORK_DIR="$(pwd)"
LOG_DIR="${WORK_DIR}/logs"
LIST=("figure_*.png" "boot.sh.o*")

[[ ! -f "${LOG_DIR}" ]] && mkdir -p ${LOG_DIR}

for TARGET in "${LIST[@]}";
do
  if [[ -n "$(find ${WORK_DIR} -maxdepth 1 -name "${TARGET}" -print -quit)" ]]
  then
    echo "Moving" ${TARGET} "to ${LOG_DIR}"
    mv -t ${LOG_DIR} ${TARGET}
  fi
done

echo "Cleaned up: ${LIST[@]}"
