#!/bin/sh
# MIT License

# Copyright (c) 2025 Nieto Rodríguez Tomás Andrés
# Copyright (c) 2025 Guadarrama Herrera Ken Bryan
# Copyright (c) 2025 Montiel Aviles Axel Fernando

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
xset -dpms
xset s off
xset s noblank
xrandr --output HDMI-1 --mode 640x480
sleep 3

cd /home/kat/snes/snes9x/unix && ./snes9x -paddev1 /dev/input/js0 -conf snes9x.conf "/home/kat/roms/Super Mario World.sfc"
