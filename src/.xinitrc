#!/bin/sh
xset -dpms
xset s off
xset s noblank
xrandr --output HDMI-1 --mode 640x480
sleep 3

cd /home/kat/snes/snes9x/unix && ./snes9x -paddev1 /dev/input/js0 -conf snes9x.conf "/home/kat/roms/Super Mario World.sfc"

