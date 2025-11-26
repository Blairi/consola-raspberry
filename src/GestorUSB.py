'''
MIT License

Copyright (c) 2025 Nieto Rodríguez Tomás Andrés
Copyright (c) 2025 Guadarrama Herrera Ken Bryan
Copyright (c) 2025 Montiel Aviles Axel Fernando

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
import shutil
import time
import os
import subprocess
import sys
import time
# 1. BUCLE DE REVISIÓN DE PUERTO USB
def watcher_usb():
    archivo_evento = "/tmp/usb_event_detected"
    ultimo_evento = None
    while True:
        contenido = None
        time.sleep(1.5)
        if os.path.exists(archivo_evento):
            with open(archivo_evento, "r") as f:
                contenido = f.read().strip()

        if contenido and contenido != ultimo_evento:
            print("USB detectada por timestamp")
            ultimo_evento = contenido
            handle_usb_insertion()
# 2. REVISIÓN Y COPIADO DE ARCHIVOS (de ser necesario)
def handle_usb_insertion():
    print("USB detectada: copiando ROMS...")
    os.system("sudo mount /dev/sd*1 /mnt/usb")
    origen = "/mnt/usb/"
    destino = "/home/kat/roms/"
    archivos_copiados = 0
    for archivo in os.listdir(origen):
        if archivo.lower().endswith((".gba", ".sfc", ".nes")):
            ruta_destino = os.path.join(destino, archivo)

            if not os.path.exists(ruta_destino):
                shutil.copy(os.path.join(origen, archivo), destino)
                archivos_copiados += 1
                print(f"Copia: {archivo}")
            else:
                print(f"Omitido (ya existe): {archivo}")

    if archivos_copiados > 0:
        print(f"Se copiaron {archivos_copiados} archivos nuevos.")
        print("Desmontando USB...")
        os.system("sudo umount /mnt/usb")
        os.system("sudo rm -f /tmp/usb_event_detected")
        os.system("killall snes9x")
        os.system("killall mednafen")
        os.system("chvt 1")
        time.sleep(1)
        os.system("python3 interfaz.py")
        sys.exit(0)

    else:
        print("No había ROMs nuevas para copiar.")
        print(f"Se copiaron {archivos_copiados} archivos nuevos.")
        print("Desmontando USB...")
        os.system("sudo umount /mnt/usb")
        os.system("sudo rm -f /tmp/usb_event_detected")

if __name__ == "__main__":
    watcher_usb()
