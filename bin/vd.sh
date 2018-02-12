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
    export PYTHONPATH="${APP_DIR}:${APP_DIR}/vccf"
    export TASK_OUTPUT="${LOG_DIR}/figure_${TASK_ID}.png"
  }

  __enq_mac() {
    #    export PATCH_MODE="RESERVED_WORD_ONLY"
    export PATCH_MODE="LINE_TYPE_SENSITIVE"
#    export PATCH_MODE="LINE_TYPE_INSENSITIVE"
    __mac-local-setup
    python ${APP_DIR}/vcc-combine.py -f ${TARGET_DATA} -o 1 -i "${TASK_ID}" -m "${PATCH_MODE}"
  }

  py() {
    __mac-local-setup && python $@
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

  __enq_linux() {
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

  q() {
    qstat -a | less
  }

  # General
  enq() {
      case "${OSTYPE}" in
      # macOS
      darwin*)
          __enq_mac
          ;;
      # Linux
      linux*)
          __enq_linux
          ;;
      esac
  }

  init() {
      if [[ "${PATH}" = *"$(pwd)"* ]]; then
        echo "NO UPDATE IS NEEDED: Target directory $(pwd) found in PATH"
        exit 0
      fi

      case "${SHELL}" in
      *zsh)
          TARGET_FILE="${HOME}/.zshrc"
          ;;
      *bash)
          TARGET_FILE="${HOME}/.bashrc"
          ;;
      *)
        echo 'Error: Supported shells are [BASH, ZSH]'
        echo 'Error: Add $(pwd) to your PATH'
        exit 1
        ;;
      esac

      if [[ $(grep $(pwd) ${TARGET_FILE} | wc -l) -le 0 ]] ; then
        echo "Adding $(pwd) to PATH in ${TARGET_FILE}"
        echo 'PATH=${PATH}'":$(pwd)" >> "${TARGET_FILE}"
      fi
      echo "ACTION REQUIRED: 'source ${TARGET_FILE}'"
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
    CALLEE=$1
    shift && ${CALLEE} $@
  else
    usage
  fi
}

vd $@
