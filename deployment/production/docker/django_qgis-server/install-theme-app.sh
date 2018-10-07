#!/usr/bin/env bash

echo "Checking Custom theme app settings"

if [ ! -z "$CUSTOM_THEME_APP_PIP_URL" ]; then

	echo "Install custom theme: $CUSTOM_THEME_APP_PIP_URL"

	pip install --upgrade $CUSTOM_THEME_APP_PIP_URL
fi
