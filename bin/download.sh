#!/usr/bin/env bash
WORK_DIR="$(pwd)"

rsync -avzP --bwlimit=8000 \
--exclude '.*' \
--exclude '*.npz' \
--exclude 'py27/' \
s1510756@hpcc:/home/s1510756/* ${WORK_DIR}
