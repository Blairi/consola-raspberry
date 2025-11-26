#!/bin/bash
# Script para lanzar Snes9x en tty3 de forma limpia
killall -9 python3
python3 GestorUSB.py &
# Cambiar a tty3
sudo chvt 3

# Lanzar Xorg en tty3 con configuración mínima
startx
killall -9 snes9x
chvt 1
killall -9 python3
killall -9 mednafen
python3 interfaz.py
