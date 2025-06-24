# main.py
import time
from actuators import setup_actuators, turn_pump_on, turn_pump_off, cleanup_gpio
from config import RELAY_PINS

def activate_pump_by_id(pump_id_str, duration_seconds=5):
    """
    Activa una bomba específica por su ID (ej. 'bomba_1', 'bomba_2').
    :param pump_id_str: String con el ID de la bomba (ej. 'bomba_1', 'bomba_2').
    :param duration_seconds: Duración en segundos que la bomba estará encendida.
    """
    if pump_id_str not in RELAY_PINS:
        print(f"Error: La bomba '{pump_id_str}' no es un ID de bomba válido.")
        print(f"IDs válidos son: {', '.join(RELAY_PINS.keys())}")
        return False # Indica que la operación no fue exitosa

    print(f"Intentando activar {pump_id_str} por {duration_seconds} segundos...")
    turn_pump_on(pump_id_str)
    time.sleep(duration_seconds)
    turn_pump_off(pump_id_str)
    print(f"Bomba {pump_id_str} desactivada.")
    return True # Indica que la operación fue exitosa

if __name__ == '__main__':
    print("Iniciando programa de prueba de bombas interactivo...")
    # Configura los GPIOs al inicio del programa principal
    setup_actuators()

    if not setup_actuators: # Si setup falló, salimos
        print("No se pudieron configurar los actuadores. Saliendo.")
        exit()

    try:
        while True:
            # Mostrar opciones al usuario
            print("\n-------------------------------------------")
            print("Motores disponibles:")
            for key in RELAY_PINS.keys():
                print(f"- {key}")
            print("-------------------------------------------")

            user_input = input("Introduce el ID del motor a probar (ej. bomba_1) o 'q' para salir: ").lower().strip()

            if user_input == 'q':
                break # Salir del bucle

            # Puedes pedir la duración también si quieres
            try:
                duration_input = input("Duración en segundos (por defecto 3): ")
                duration = int(duration_input) if duration_input else 3
            except ValueError:
                print("Duración inválida. Usando 3 segundos por defecto.")
                duration = 3

            activate_pump_by_id(user_input, duration)

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    finally:
        # Asegúrate de limpiar los GPIOs al finalizar el programa
        cleanup_gpio()
        print("Programa finalizado.")
