#!/usr/bin/env bash
MESSAGE=${1}
echo ${MESSAGE:=''} > "$(pwd)/hpcc/message.txt" \
  && qsub boot.sh
