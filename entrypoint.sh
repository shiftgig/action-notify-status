#!/bin/sh

set -eu

# Lowercase job status
JOB_STATUS=$(echo "$1" | tr '[:upper:]' '[:lower:]')
SLACK_TOKEN=$2
CHANNEL_ID=$3

python /usr/src/app/application/send_status.py --token $SLACK_TOKEN --channel $CHANNEL_ID --job-status $JOB_STATUS
