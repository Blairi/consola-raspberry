#!/bin/bash
pkill -f snes9x
pkill -f mednafen
chvt 1
pkill -f interfaz.py
sleep 1
python3 interfaz.py

