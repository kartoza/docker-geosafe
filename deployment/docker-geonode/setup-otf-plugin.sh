#!/usr/bin/env bash

cd /opt/qgis-server/plugins
git clone https://github.com/kartoza/otf-project.git
cd otf-project/ && git checkout 0a44fa4ccc40a5645af7d4349c63b9bb2f995595 && cd ..
