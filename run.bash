#!/usr/bin/env bash
# -*- coding: utf-8 -*-

main=resistance.py

processes=$(pgrep -u "$USER" -f "$main")
xargs kill -9 <<< "$processes" > /dev/null 2>&1
printf "\033[97mkilled processes:\033[0m\n%s\n\n" "$processes"

python3 "$main" "$@" > bot.log 2>&1 &
