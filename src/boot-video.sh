#!/bin/bash
# Espera unos segundos a que cargue el framebuffer y el audio
sleep 3
# Reproduce el video en pantalla completa sin mostrar nada más
sudo mpv --vo=sdl --hwdec=auto --fullscreen --no-terminal --cursor-autohide=always /usr/local/share/bootanim/intro.mp4
clear > /dev/tty1
