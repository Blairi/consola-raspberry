#!/bin/bash
# Script para lanzar Snes9x en tty3 de forma limpia

# Cambiar a tty3
chvt 3

# Limpiar variables de X del frontend
unset DISPLAY
unset XAUTHORITY

# Lanzar Xorg en tty3 con configuración mínima
startx -- :1
chvt 1
killall python3
python3 interfaz.py
