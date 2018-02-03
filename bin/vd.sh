#!/usr/bin/env bash

function vd() {
  set -u
  local SELF="$(basename $0)"
  local NAME="History-based Vulnerability Detector"
  local UTIME="$(date +'%Y%m%d')"
  local TARGET="s1510756@hpcc:/home/s1510756"

  # Local
  __mac-local-setup() {
    export APP_DIR="$(pwd)/hpcc"
    export TARGET_DATA="$(pwd)/vcc_data_40x800.npz"
    export LOG_DIR="$(pwd)/logs"
    export TASK_ID="$(date +%s)"
    export TASK_OUTPUT="${LOG_DIR}/figure_${TASK_ID}.png"
  }

  __enq-mac() {
    #    export PATCH_MODE="RESERVED_WORD_ONLY"
    export PATCH_MODE="LINE_TYPE_SENSITIVE"
#    export PATCH_MODE="LINE_TYPE_INSENSITIVE"
    __mac-local-setup
    python ${APP_DIR}/vcc-combine.py -f ${TARGET_DATA} -o 1 -i "${TASK_ID}" -m "${PATCH_MODE}"
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
      ${WORK_DIR}/{vd,hpcc,vccf,bin} ${TARGET}
  }

  # Remote
  ssh() {
    qsub -q SINGLE -I
  }

  __enq-linux() {
    bash $(pwd)/bin/clean.sh
    qsub -q SINGLE ${HOME}/bin/boot.sh
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

  # General
  enq() {
      case "${OSTYPE}" in
      # macOS
      darwin*)
          __enq-mac
          ;;
      # Linux
      linux*)
          __enq-linux
          ;;
      esac
  }

  q() {
    qstat -a | less
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
