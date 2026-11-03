#!bin/bash

## library bundle
curl -L -O https://github.com/adafruit/CircuitPython_Community_Bundle/releases/download/20261008/circuitpython-community-bundle-11.x-mpy-20261008.zip && unzip circuitpython-community-bundle-11.x-mpy-20261008.zip -d ./libs/circuitpython-community-bundle-11


## uf2 for xiao 
curl -L -O https://downloads.circuitpython.org/bin/Seeed_XIAO_nRF52840_Sense/en_US/adafruit-circuitpython-Seeed_XIAO_nRF52840_Sense-en_US-10.3.1.uf2 -d ./libs/board_load/
cp -r ./libs/circuitpython/frozen/Adafruit_CircuitPython_HID/ ./libs/

sudo mount -o uid=$(id -u),gid=$(id -g) /dev/sdb1 ./CIRCUITPY