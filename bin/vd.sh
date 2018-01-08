#!/usr/bin/env bash

function vd() {
  set -u
  local SELF="$(basename $0)"
  local NAME="History-based Vulnerability Detector"
  local UTIME="$(date +'%Y%m%d')"
  local PID_PATH="tmp/.pids"
  local MODEL_DIR="playground/tmp/vcc_model/"
  local TARGET="s1510756@hpcc:/home/s1510756"

  start-notebook() {
    nohup bin/jupyter notebook >> "logs/${UTIME}_notebook.log" 2>&1 &
    echo $! >> "${PID_PATH}"
  }

  mac-local-setup() {
    export APP_DIR="$(pwd)/app"
    export TARGET_DATA="$(pwd)/notebooks/vcc_data_40x800.npz"
    export PYTHONPATH="$(pwd)/notebooks:$(pwd)/notebooks/vccf"
    pyenv activate tfvcc_3.6.3
  }

  enq-mac() {
    mac-local-setup
    python ${APP_DIR}/hd_rnn.py -f ${TARGET_DATA} -o 1
  }

  py() {
    mac-local-setup
    python
  }

  fig() {
    WORK_DIR="$(pwd)"
    open $(ls -t ${WORK_DIR}/logs/figure_*.png | head -1)
  }

  result() {
    WORK_DIR="$(pwd)"
    less $(ls -t ${WORK_DIR}/logs/*.log | head -1)
  }

  status() {
    [[ -f "${PID_PATH}" ]] && cat "${PID_PATH}"
  }

  terminate-processes() {
    if [[ -s "${PID_PATH}" ]]; then
      kill $(status)
      cat /dev/null > "${PID_PATH}"
    fi
  }

  clean() {
    rm -fr "${MODEL_DIR}/*"
  }

  logs() {
    tail -F logs/*.log
  }

  download() {
    WORK_DIR="$(pwd)"
    rsync -avzP --bwlimit=8000 \
      ${TARGET}/logs ${WORK_DIR}
  }

  upload() {
    WORK_DIR="$(pwd)"
    rsync -avzP --bwlimit=8000 \
      --exclude '.*' \
      --exclude '*.npz' \
      --exclude 'py27/' \
      ${WORK_DIR}/{hpcc,vccf,bin} ${TARGET}
  }


  ssh() {
    qsub -q G-SINGLE -I
  }

  enq() {
    bash ${HOME}/command/clean.bash
    qsub -q G-SINGLE ./command/boot.sh
  }

  deq() {
    if [[ -z "${JOB_ID}" ]]; then
      echo "Error: Environment value JOB_ID is required to dequeue the task."
      exit 1
    fi
    qdel "${JOB_ID}"
  }

  watch() {
    bash -c 'watch -n 5 qstat -a -u $USER'
  }

  usage() {
    echo -e "${SELF} -- ${NAME}
    \nUsage: ${SELF} [sub-command]
    \n[Sub-command Options]"
    declare -F | awk '{print "\t" $3}' | grep -v ${SELF} | grep -vE '^\t__[^_]+'
    echo ''
  }

  if [[ $# = 0 ]]; then
    usage
    echo "INFO: ${SELF} requires a sub-command"
  elif [[ "$(type -t $1)" = "function" ]]; then
    $1
  else
    usage
  fi
}

vd $1
