#!/usr/bin/env bash

pip install --target ./package
pushd ./package
zip -r9 ../function.zip .
popd
zip -g ./function.zip ./schedule-alerts.py

aws lambda update-function-code --function-name schedule-alerts --zip-file fileb://function.zip
