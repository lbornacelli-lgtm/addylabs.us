#!/bin/bash
# Copy any file to the on-prem shared reports folder
# Usage: ./deliver_report.sh /path/to/file.pdf
FILE=$1
if [ -z "$FILE" ]; then
    echo "Usage: $0 /path/to/file"
    exit 1
fi
scp "$FILE" lawborn@10.0.0.1:/home/lawborn/shared/reports/
echo "Delivered $(basename $FILE) to shared reports folder"
