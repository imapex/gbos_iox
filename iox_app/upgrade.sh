#!/usr/bin/env bash

# Usage: bash deploy.sh <APPLICATION NAME>

APP_NAME=$1
ioxclient package .

ioxclient application stop $APP_NAME
ioxclient application deactivate $APP_NAME

ioxclient application upgrade $APP_NAME ./package.tar
ioxclient application activate $APP_NAME --payload device_mapping.json
ioxclient application start $APP_NAME