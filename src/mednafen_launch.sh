#!/bin/bash
chvt 3
mednafen "/home/kat/roms/Super Mario Bros.nes"
chvt 1
killall python3
python3 interfaz.py
