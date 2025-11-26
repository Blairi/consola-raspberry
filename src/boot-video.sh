#!/bin/bash
# Esperar framebuffer/audio
sleep 3
# Reproducir el video en tty1
mpv --vo=sdl --hwdec=auto --fullscreen --no-terminal --cursor-autohide=always /usr/local/share/bootanim/intro.mp4
clear > /dev/tty1

