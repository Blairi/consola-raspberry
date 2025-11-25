import time
import os
import subprocess
import sys

sys.stdout = open(os.devnull, "w")
sys.stderr = open(os.devnull, "w")

import pygame

# --- CONFIGURACION ---
ANCHO, ALTO = 800, 600
PANTALLA_COMPLETA = False 
COLOR_FONDO = (0, 0, 0)       # Negro Puro
COLOR_TEXTO = (255, 255, 255) # Blanco
COLOR_GRIS = (100, 100, 100)  # Para lo no seleccionado
COLOR_RESALTADO = (0, 255, 255) # Cyan/Azul neon para destacar

# CONFIGURACION FONDO
VELOCIDAD_FONDO = 0.5 
NOMBRE_ARCHIVO_FONDO = "fondo.png" 
POS_FONDO_X = 0 

# CONFIGURACION AUDIO
NOMBRE_MUSICA_FONDO = "background.mp3" 
NOMBRE_SONIDO_MOVER = "move.mp3"      
RUTA_ROMS = "/home/kat/roms"


class InterfazKat:

    def __init__(self):
        # 1. Inicializar modulos basicos
        os.system("sudo rm -f /tmp/usb_event_detected")
        pygame.init()
        pygame.font.init()

        # 2. Inicializar el mezclador de audio
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        except Exception as e:
            print(f"Error al iniciar el audio: {e}")
        
        # Config pantalla
        flags = pygame.FULLSCREEN if PANTALLA_COMPLETA else 0
        self.pantalla = pygame.display.set_mode((ANCHO, ALTO), flags)
        pygame.display.set_caption("Retro Station KAT")
        
        pygame.mouse.set_visible(False)
            
        self.ancho, self.alto = self.pantalla.get_size()
        
        # --- FUENTES ---
        self.fuente_titulo = pygame.font.SysFont('Arial Black', 40)
        self.fuente_consola = pygame.font.SysFont('Arial', 24, bold=True)
        self.fuente_lista = pygame.font.SysFont('Consolas', 28)
        self.fuente_normal = pygame.font.SysFont('Arial', 18) 
        
        self.reloj = pygame.time.Clock()
        
        # --- LOGO ---
        self.logo_img = None
        nombre_archivo_logo = "logo.png"
        
        if os.path.exists(nombre_archivo_logo):
            try:
                imagen = pygame.image.load(nombre_archivo_logo).convert_alpha()
                alto_deseado = 80
                factor = alto_deseado / imagen.get_height()
                ancho_nuevo = int(imagen.get_width() * factor)
                self.logo_img = pygame.transform.smoothscale(imagen, (ancho_nuevo, alto_deseado))
            except Exception as e:
                print(f"Error cargando logo.png: {e}")

        # --- FONDO MOVIL ---
        self.fondo_img = None
        if os.path.exists(NOMBRE_ARCHIVO_FONDO):
            try:
                fondo_cargado = pygame.image.load(NOMBRE_ARCHIVO_FONDO).convert()
                self.fondo_img = pygame.transform.scale(fondo_cargado, (int(fondo_cargado.get_width() * (self.alto / fondo_cargado.get_height())), self.alto))
                self.fondo_ancho_real = self.fondo_img.get_width()
            except Exception as e:
                print(f"Error cargando fondo.png: {e}")
        
        # --- CARGAR AUDIO ---
        self.snd_move = None
        try:
            self.snd_move = pygame.mixer.Sound(NOMBRE_SONIDO_MOVER)
            self.snd_move.set_volume(0.6) # Volumen del efecto
        except Exception as e:
            print(f"Error: No se pudo cargar el sonido '{NOMBRE_SONIDO_MOVER}'. {e}")

        try:
            pygame.mixer.music.load(NOMBRE_MUSICA_FONDO)
            pygame.mixer.music.set_volume(0.4) # Musica de fondo mas baja
            pygame.mixer.music.play(loops=-1) # loops=-1 = bucle infinito
        except Exception as e:
            print(f"Error: No se pudo cargar la musica '{NOMBRE_MUSICA_FONDO}'. {e}")

        # --- SISTEMA DE MENU ---
        self.consolas = ["GBA", "NES", "SNES"] 
        self.idx_consola = 0 
        self.idx_juego = 0   
        self.actualizar_lista_juegos()

    def actualizar_lista_juegos(self):
        consola_actual = self.consolas[self.idx_consola]
        self.idx_juego = 0 
        
        self.juegos_actuales = []
        if os.path.exists(RUTA_ROMS):
            archivos = os.listdir(RUTA_ROMS)
            if consola_actual == "SNES":
                self.juegos_actuales = [os.path.splitext(f)[0] for f in archivos if f.lower().endswith(".sfc")]
            elif consola_actual == "GBA":
                self.juegos_actuales = [os.path.splitext(f)[0] for f in archivos if f.lower().endswith(".gba")]
            elif consola_actual == "NES":
                self.juegos_actuales = [os.path.splitext(f)[0] for f in archivos if f.lower().endswith(".nes")]
            else:
                self.juegos_actuales = ["No hay ROMs para esta consola"]
        else:
           self.juegos_actuales = ["No se encontró carpeta de ROMs"]

        self.juegos_actuales.sort()

    def dibujar(self):
        global POS_FONDO_X
        
        # 1. DIBUJAR FONDO
        if self.fondo_img:
            self.pantalla.blit(self.fondo_img, (POS_FONDO_X, 0))
            self.pantalla.blit(self.fondo_img, (POS_FONDO_X + self.fondo_ancho_real, 0))
            
            POS_FONDO_X -= VELOCIDAD_FONDO
            if POS_FONDO_X <= -self.fondo_ancho_real:
                POS_FONDO_X = 0
        else:
            self.pantalla.fill(COLOR_FONDO)
        
        # Capa oscura semitransparente para leer mejor
        s = pygame.Surface((self.ancho, self.alto), pygame.SRCALPHA)
        s.fill((0,0,0,150)) 
        self.pantalla.blit(s, (0,0))
        
        # 2. CABECERA
        pos_logo_x, pos_logo_y = 30, 20
        inicio_titulo_x = 120 
        
        if self.logo_img:
            self.pantalla.blit(self.logo_img, (pos_logo_x, pos_logo_y))
            inicio_titulo_x = pos_logo_x + self.logo_img.get_width() + 20
        else:
            pygame.draw.rect(self.pantalla, COLOR_TEXTO, (pos_logo_x, pos_logo_y, 80, 80), 2)
            inicio_titulo_x = 130

        titulo = self.fuente_titulo.render("RETRO STATION KAT", True, COLOR_TEXTO)
        self.pantalla.blit(titulo, (inicio_titulo_x, pos_logo_y + 15))
        
        # 3. BARRA DE CONSOLAS
        y_consolas = 120 
        pygame.draw.line(self.pantalla, COLOR_GRIS, (20, y_consolas + 35), (self.ancho - 20, y_consolas + 35), 2)
        
        margen_x = 120
        for i, consola in enumerate(self.consolas):
            es_actual = (i == self.idx_consola)
            color = COLOR_RESALTADO if es_actual else COLOR_GRIS
            
            texto = f"< {consola} >" if es_actual else consola
            render = self.fuente_consola.render(texto, True, color)
            
            self.pantalla.blit(render, (margen_x, y_consolas))
            margen_x += 180 

        # 4. LISTA DE JUEGOS
        y_lista = 160
        max_items_lista = 9 
        
        inicio_visible = max(0, self.idx_juego - max_items_lista // 2)
        fin_visible = min(len(self.juegos_actuales), inicio_visible + max_items_lista)
        
        if fin_visible - inicio_visible < max_items_lista:
            inicio_visible = max(0, fin_visible - max_items_lista)

        for i, juego in enumerate(self.juegos_actuales[inicio_visible:fin_visible]):
            indice_real = inicio_visible + i
            es_seleccionado = (indice_real == self.idx_juego)
            
            color = COLOR_TEXTO if es_seleccionado else COLOR_GRIS
            offset_x = 20 if es_seleccionado else 0
            
            texto_juego = self.fuente_lista.render(juego, True, color)
            
            if es_seleccionado:
                pygame.draw.rect(self.pantalla, COLOR_RESALTADO, (40, y_lista + (i*40), 10, 25))
            
            self.pantalla.blit(texto_juego, (60 + offset_x, y_lista + (i * 40)))

        # 5. PIE DE PAGINA (Corregidos espacios raros)
        pie = self.fuente_normal.render("[A] Seleccionar juego   [JOYSTICK / DPAD] Moverse   [B] Apagar", True, (150, 150, 150))
        self.pantalla.blit(pie, (50, self.alto - 40))

        pygame.display.flip()

    def preparar_gba(self, ruta_rom):
        nombre_juego = os.path.splitext(os.path.basename(ruta_rom))[0]
        sav_dir = os.path.expanduser("~/.mednafen/sav")
        os.makedirs(sav_dir, exist_ok=True)
        type_path = os.path.join(sav_dir, nombre_juego + ".type")

        if os.path.exists(type_path):
           print(f"[Mednafen] Archivo .type ya existe: {type_path}")
           return

        with open(type_path, "w") as f:
           f.write("flash 128\n")

        print(f"[Mednafen] Archivo .type creado: {type_path}")

    def seleccionar_juego(self, indice):
        juego = self.juegos_actuales[indice]
        consola = self.consolas[self.idx_consola]
        xinitrc_path = os.path.expanduser("~/.xinitrc")

        if consola == "SNES":
           extension = ".sfc"
        elif consola == "GBA":
           extension = ".gba"
        elif consola == "NES":
           extension = ".nes"
        else:
           print("Consola no reconocida")
           return
        
        ruta_rom = os.path.join(RUTA_ROMS, juego + extension)
        print(f"Lanzando ROM: {ruta_rom}")

        if consola == "SNES":
           self.joystick = None
           emu_path = "/home/kat/snes/snes9x/unix/snes9x"
           conf_path = "/home/kat/snes/snes9x/unix/snes9x.conf"

           with open(xinitrc_path, "r") as f:
              lineas = f.readlines()

           while len(lineas) < 8:
              lineas.append("\n")

           cmd = f'cd /home/kat/snes/snes9x/unix && ./snes9x -paddev1 /dev/input/js0 -conf snes9x.conf "{ruta_rom}"\n'
           lineas[7] = cmd

           with open(xinitrc_path, "w") as f:
              f.writelines(lineas)

           pygame.mixer.music.pause()
           pygame.quit()
           os.system("./x_snes.sh")
        
        elif consola == "GBA" or consola == "NES":
           self.joystick = None
           script_path = "/home/kat/src/mednafen_launch.sh"
           
           with open(script_path, "r") as f:
              lineas = f.readlines()
           
           while len(lineas) < 5:
              lineas.append("\n")

           cmd = f'mednafen "{ruta_rom}"\n'
           lineas[4] = cmd

           with open(script_path, "w") as f:
              f.writelines(lineas)

           if consola == "GBA":
              self.preparar_gba(ruta_rom)

           pygame.mixer.music.pause()
           pygame.quit()
           os.system("./mednafen_launch.sh")

        else:
          print("Consola no reconocida")

    def correr(self):
        corriendo = True
        ultimo_input = 0
        
        while corriendo:
            ahora = time.time()

            for evento in pygame.event.get():
                pass

            if self.joystick:
                try:
                    eje_x = self.joystick.get_axis(0) 
                    eje_y = self.joystick.get_axis(1) 
                    
                    if ahora - ultimo_input > 0.2:
                        movimiento_detectado_joy = False
                        
                        if eje_x > 0.5:
                            self.idx_consola = (self.idx_consola + 1) % len(self.consolas)
                            self.actualizar_lista_juegos()
                            movimiento_detectado_joy = True
                        elif eje_x < -0.5:
                            self.idx_consola = (self.idx_consola - 1) % len(self.consolas)
                            self.actualizar_lista_juegos()
                            movimiento_detectado_joy = True
                            
                        elif eje_y > 0.5 and self.idx_juego < len(self.juegos_actuales) - 1:
                            self.idx_juego += 1
                            movimiento_detectado_joy = True
                        elif eje_y < -0.5 and self.idx_juego > 0:
                            self.idx_juego -= 1
                            movimiento_detectado_joy = True
                        
                        if movimiento_detectado_joy:
                            if self.snd_move:
                                self.snd_move.play()
                            ultimo_input = ahora
                        
                        hats = self.joystick.get_numhats()
                        for i in range(hats):
                            hat_x, hat_y = self.joystick.get_hat(i)
                            if hat_x == 1:
                                self.idx_consola = (self.idx_consola + 1) % len(self.consolas)
                                self.actualizar_lista_juegos()
                                movimiento_detectado_joy = True
                            elif hat_x == -1:
                                self.idx_consola = (self.idx_consola - 1) % len(self.consolas)
                                self.actualizar_lista_juegos()
                                movimiento_detectado_joy = True
                            elif hat_y == 1 and self.idx_juego > 0:
                                self.idx_juego -= 1
                                movimiento_detectado_joy = True
                            elif hat_y == -1 and self.idx_juego < len(self.juegos_actuales) - 1:
                                self.idx_juego += 1
                                movimiento_detectado_joy = True
                            
                            if movimiento_detectado_joy:
                                if self.snd_move:
                                    self.snd_move.play()
                                ultimo_input = ahora

                        if self.joystick.get_button(0):
                            print(f"Lanzando: {self.juegos_actuales[self.idx_juego]}")
                            self.seleccionar_juego(self.idx_juego)
                            ultimo_input = ahora 
                        elif self.joystick.get_button(1):
                            print(f"Apagando...")
                            os.system("sudo shutdown -h now")

                except pygame.error: 
                    # Se desconecto el control
                    self.joystick = None
                    print("Joystick desconectado.")
                    pass
            

            self.dibujar()
            self.reloj.tick(24)
            
        pygame.quit()






# --- ARRANQUE PRINCIPAL ---
pygame.init()
pygame.font.init()
pygame.joystick.init()

if __name__ == "__main__":
    try:
        os.system("python3 GestorUSB.py &")
        app = InterfazKat()
        if pygame.joystick.get_count() > 0:
            app.joystick = pygame.joystick.Joystick(0)
            app.joystick.init()
            print(f"Joystick detectado: {app.joystick.get_name()}")
        else:
            app.joystick = None
        
        app.correr()
    except Exception as e:
        print(f"Ocurrio un error fatal: {e}")
        pygame.quit()
