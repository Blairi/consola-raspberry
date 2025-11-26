# Consola Raspberry 

Consola de videojuegos retro para Raspberry Pi 3 con interfaz gráfica personalizada y soporte para múltiples emuladores (GBA, NES, SNES).

## Características

- Interfaz gráfica personalizada con Pygame
- Soporte para 3 consolas: Game Boy Advance, NES y Super Nintendo
- Hot-swap de ROMs mediante USB (conecta y copia automáticamente)
- Control completo por joystick/gamepad USB

---

## Requisitos

### Hardware
- **Raspberry Pi 3** (Model B o B+)
- Tarjeta microSD (mínimo 16GB)
- Control USB (compatible con Linux)
- Monitor HDMI
- Fuente de alimentación 5V/2.5A

### Software
- Raspberry Pi OS Lite
- Python 3.7+
- Pygame
- Mednafen (emulador NES/GBA)
- Snes9x (emulador SNES)

---

## Inicio Rápido

### 1. Preparar la Raspberry Pi

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar dependencias del sistema
sudo apt install git build-essential libsdl2-dev make libasound2-dev libsdl2-image-dev libsdl2-ttf-dev mpv server-xorg xinit x11-xserver-utils xboxdrv -y
```

### 2. Instalar Emuladores

#### Mednafen (NES y GBA)
```bash
sudo apt install -y mednafen
```

#### Snes9x (SNES)
```bash
# Clonar y compilar Snes9x
cd ~
mkdir -p snes
cd snes
git clone https://github.com/snes9xgit/snes9x.git
cd snes9x/unix
./configure
make -j4
```

### 3. Clonar este Repositorio

```bash
cd ~
git clone https://github.com/Blairi/consola-raspberry.git
cd consola-raspberry
```

### 4. Instalar Dependencias de Python

```bash
sudo apt install python3-pygame
```

### 5. Configurar el Sistema

#### a) Crear directorios necesarios
```bash
# Crear carpeta para ROMs
mkdir -p ~/roms

# Crear punto de montaje para USB
sudo mkdir -p /mnt/usb
```

#### b) Copiar archivos de configuración
```bash
# Copiar archivos al directorio home del usuario 'kat'
# (Ajusta el usuario según tu configuración)
cp src/.xinitrc ~/.xinitrc
chmod +x ~/.xinitrc

# Copiar scripts ejecutables
sudo cp src/usb_detectada.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/usb_detectada.sh
sudo cp src/boot-video.sh /usr/local/bin/
sudo chmod +x /usr/local/bin/boot-video.sh
```

#### c) Configurar parámetros de arranque
```bash
# Copiar contenido del archivo config/cmdline.txt a /boot/firmware/cmdline.txt
# Esto configura el arranque silencioso y la terminal
sudo cp /boot/firmware/cmdline.txt /boot/firmware/cmdline.txt.backup
sudo cp src/cmdline.txt /boot/firmware/cmdline.txt
```

### 6. Configurar Rutas en el Código

Edita los archivos para ajustar las rutas según tu usuario (por defecto usa `kat`):

```bash
# Editar interfaz.py
nano src/interfaz.py
# Cambiar todas las rutas /home/kat/ por /home/TU_USUARIO/

# Editar scripts
nano src/mednafen_launch.sh
nano src/x_snes.sh
nano src/restart.sh
# Ajustar rutas en cada script
```

### 7. Preparar Assets

```bash
# Los archivos de recursos (imágenes y audio) deben estar en el directorio src del proyecto:
# - logo.png
# - fondo.png
# - background.mp3
# - move.mp3

# Si tienes estos archivos en otra ubicación, cópialos al directorio src del proyecto
cd ~/src
# Ejemplo: cp /ruta/a/tus/archivos/*.png .
#          cp /ruta/a/tus/archivos/*.mp3 .
```

### 8. Agregar ROMs

```bash
# Copiar tus ROMs a la carpeta
cp tus_juegos/*.sfc ~/roms/  # SNES
cp tus_juegos/*.gba ~/roms/  # Game Boy Advance
cp tus_juegos/*.nes ~/roms/  # NES
```

### 9. Configurar Arranque Automático

```bash
# Editar el archivo .bash_profile para iniciar la consola automáticamente
nano ~/.bash_profile

# Agregar las siguientes líneas al final del archivo:
if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
    cd ~/consola-raspberry/src
    python3 interfaz.py
fi

# Guardar y cerrar (Ctrl+O, Enter, Ctrl+X)
```

### 10. Reiniciar el Sistema

```bash
# Reiniciar para que los cambios surtan efecto
sudo reboot
```

La consola se iniciará automáticamente después del arranque.

---

## Uso

### Agregar Juegos por USB
1. Copia tus ROMs (`.sfc`, `.gba`, `.nes`) en una memoria USB
2. Conecta el USB a la Raspberry Pi mientras la consola está corriendo
3. El sistema detectará automáticamente, copiará las ROMs nuevas y reiniciará
4. Los juegos aparecerán en el menú

## Estructura del Proyecto

```
consola-raspberry/
├── config/              # Archivos de configuración del sistema
│   ├── cmdline.txt
│   └── .xinitrc
├── scripts/             # Scripts de utilidad
│   ├── mednafen_launch.sh
│   ├── restart.sh
│   └── x_snes.sh
├── src/                 # Código fuente
│   ├── interfaz.py      # Interfaz principal
│   ├── GestorUSB.py     # Gestor de ROMs por USB
│   └── diagnostico_control.py
├── LICENSE
└── README.md
```


## Créditos
- Montiel Aviles Axel Fernando
- Nieto Rodríguez Tomás Andrés
- []
- **Emuladores**: Mednafen, Snes9x
- **Framework gráfico**: Pygame
- **Hardware**: Raspberry Pi Foundation
