#! /bin/bash

sudo apt update && sudo apt upgrade -y
sudo apt install git build-essential libsdl2-dev make libasound2-dev libsdl2-image-dev libsdl2-ttf-dev mpv server-xorg xinit x11-xserver-utils xboxdrv -y

sudo apt install -y mednafen
cd ~
mkdir -p snes
cd snes
git clone https://github.com/snes9xgit/snes9x.git
cd snes9x/unix
./configure
make -j4

cd ~
git clone https://github.com/Blairi/consola-raspberry.git
cd consola-raspberry

sudo apt install python3-pygame

mkdir -p ~/roms
sudo mkdir -p /mnt/usb

cp src/.xinitrc ~/.xinitrc
chmod +x ~/.xinitrc
sudo cp /src/usb_detectada.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/usb_detectada.sh
sudo cp /src/boot-video.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/boot-video.sh
sudo cp /boot/firmware/cmdline.txt /boot/firmware/cmdline.txt.backup
sudo cp /src/cmdline.txt /boot/firmware/cmdline.txt

sudo cp /src/.bash_profile ~/
sudp cp /src/snes9x.config ~/snes/snes9x/unix
sudo cp /src/99-detectar-usb.rules /etc/udev/rules.d
sudo cp /src/boot-video.service  /etc/systemd/system/boot-video.service
sudo cp /src/override.conf /etc/systemd/system/getty@tty1.service.d/
cd ~/src
sudo systemctl daemon - reload
sudo systemctl enable boot - video . service

sudo reboot