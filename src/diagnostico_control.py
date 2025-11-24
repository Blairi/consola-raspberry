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