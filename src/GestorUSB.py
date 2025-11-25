import shutil
import time
import os
import subprocess
import sys
import time

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
