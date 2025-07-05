#!/bin/bash

if [ $# -ne 2 ]; then
  echo "Usage: $0 <pid> <mem limit(MB)>"
  exit 1
fi

PROCESS_ID="$1"
MAX_MEM_MB="$2"
MAX_MEM_KB=$((MAX_MEM_MB * 1024))  # 转换为KB

while true; do
    MEM_USAGE=$(ps -p "$PROCESS_ID" -o rss=)
    if [[ "$MEM_USAGE" -gt "$MAX_MEM_KB" ]]; then
        kill -9 "$PROCESS_ID"
    fi
    if [[ "$MEM_USAGE" = "" ]]; then
        exit
    fi
    sleep 5 # Retry every 5 seconds
done
