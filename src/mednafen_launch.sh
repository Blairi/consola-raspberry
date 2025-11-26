#!/bin/bash

python3 GestorUSB.py &
chvt 3
mednafen "/home/kat/roms/The Flintstones - The Rescue of Dino & Hoppy.nes"
killall -9 snes9x
killall -9 mednafen
killall -9 python3
chvt 1
python3 interfaz.py
