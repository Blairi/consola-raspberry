#!/bin/bash
killall snes9x
killall mednafen
killall python3
killall -HUP xinit
sudp chvt 1
sleep 1
python3 interfaz.py

