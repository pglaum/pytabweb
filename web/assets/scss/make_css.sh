#!/usr/bin/env bash

DIR="$(dirname $0)"

sassc "${DIR}/base.scss" > "${DIR}/../../static/css/main.css"
