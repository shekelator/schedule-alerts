#!/usr/bin/env bash

rm ./function.zip
pip install --target ./package
pushd ./package
zip -r9 -q ../function.zip .
popd
zip -g ./function.zip ./schedule_alerts.py

aws lambda update-function-code --function-name schedule-alerts --zip-file fileb://function.zip
