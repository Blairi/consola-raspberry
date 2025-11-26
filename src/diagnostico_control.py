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
import pygame
import time

# 1. Inicializar Pygame y el modulo de Joystick
pygame.init()
pygame.joystick.init()

# 2. Verificar si hay controles conectados
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
    print("Error: No se detecto ningun control.")
    print("Conecta un control USB y vuelve a ejecutar el script.")
    pygame.quit()
    exit()

# 3. Conectar al primer control (indice 0)
try:
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    print(f"Control detectado: {joystick.get_name()}")
    print(f"Numero de ejes (palancas): {joystick.get_numaxes()}")
    print(f"Numero de botones: {joystick.get_numbuttons()}")
    print(f"Numero de 'Hats' (crucetas): {joystick.get_numhats()}")
    print("\n--- MUEVE LAS PALANCAS Y PRESIONA BOTONES ---")
    print("(Presiona Ctrl+C en esta terminal para salir)")

except pygame.error as e:
    print(f"Error al iniciar el joystick: {e}")
    pygame.quit()
    exit()

# 4. Bucle principal para leer eventos
running = True
try:
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # --- Evento de Boton Presionado ---
            if event.type == pygame.JOYBUTTONDOWN:
                print(f"Boton presionado: {event.button}")
            
            # --- Evento de Boton Soltado ---
            if event.type == pygame.JOYBUTTONUP:
                print(f"Boton soltado: {event.button}")

            # --- Evento de Palanca (Eje) ---
            if event.type == pygame.JOYAXISMOTION:
                # Imprimir solo si el movimiento es significativo (mayor a 0.5)
                if abs(event.value) > 0.5:
                    print(f"Eje (Axis) {event.axis} movido. Valor: {event.value:.2f}")
            
            # --- Evento de Cruceta (Hat) ---
            if event.type == pygame.JOYHATMOTION:
                print(f"Cruceta (Hat) {event.hat} movida. Valor: {event.value}")
        
        # Pequeña pausa para no saturar la consola
        time.sleep(0.02)

except KeyboardInterrupt:
    print("\nPrueba de control finalizada.")
finally:

    pygame.quit()
