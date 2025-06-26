import time
from actuators import setup_actuators, turn_pump_on, turn_pump_off, cleanup_gpio
from sensors import LightSensor
from config import RELAY_PINS, BH1750_MAX_LUX_ADJUSTED, PUMP_ACTIVATION_DURATION_SEC

def activate_pump_by_id(pump_id_str, duration_seconds):
    """
    Activa una bomba específica por su ID.
    Controla que solo una bomba esté activa a la vez para evitar conflictos si se llama automáticamente.
    """
    if pump_id_str not in RELAY_PINS:
        print(f"Error: La bomba '{pump_id_str}' no es un ID de bomba válido.")
        print(f"IDs válidos son: {', '.join(RELAY_PINS.keys())}")
        return False

    # Asegura que las demás bombas estén apagadas antes de encender la deseada
    for pump_name in RELAY_PINS.keys():
        if pump_name != pump_id_str:
            turn_pump_off(pump_name) # Apaga las otras bombas

    print(f"Activando {pump_id_str} por {duration_seconds} segundos...")
    turn_pump_on(pump_id_str)
    time.sleep(duration_seconds)
    turn_pump_off(pump_id_str)
    print(f"Bomba {pump_id_str} desactivada.")
    return True

def control_pumps_by_light(current_lux, pump_names):
    """
    Activa una bomba específica en función del nivel de luz actual.
    Divide el rango de luz total (hasta BH1750_MAX_LUX_ADJUSTED) en 4 segmentos para 4 bombas.
    """
    num_pumps = len(pump_names)
    if num_pumps != 4:
        print("Advertencia: Esta función está diseñada para 4 bombas. Ajusta la lógica si tienes un número diferente.")
        return

    # Definir los umbrales para 4 segmentos basados en el rango ajustado (0 a BH1750_MAX_LUX_ADJUSTED)
    segment_size = BH1750_MAX_LUX_ADJUSTED // num_pumps

    pump_to_activate = None
    action_message = ""

    if current_lux is not None:
        if current_lux < 0: # Para manejar posibles lecturas negativas o anómalas
            action_message = f"Luz fuera de rango ({current_lux} Lux). No se activa ninguna bomba."
        elif current_lux < segment_size:
            pump_to_activate = pump_names[0] # Bomba 1 para el rango más bajo
            action_message = f"Luz muy baja ({current_lux} Lux). Activar {pump_to_activate}."
        elif current_lux < (segment_size * 2):
            pump_to_activate = pump_names[1] # Bomba 2 para el segundo rango
            action_message = f"Luz baja ({current_lux} Lux). Activar {pump_to_activate}."
        elif current_lux < (segment_size * 3):
            pump_to_activate = pump_names[2] # Bomba 3 para el tercer rango
            action_message = f"Luz media ({current_lux} Lux). Activar {pump_to_activate}."
        else: # current_lux >= (segment_size * 3)
            pump_to_activate = pump_names[3] # Bomba 4 para el rango más alto
            action_message = f"Luz alta ({current_lux} Lux). Activar {pump_to_activate}."
        
        print(action_message)

        # Automatización: Activa la bomba automáticamente si se ha determinado una
        if pump_to_activate:
            activate_pump_by_id(pump_to_activate, PUMP_ACTIVATION_DURATION_SEC)
    else:
        print("No se pudo leer el sensor de luz para control automático.")

if __name__ == '__main__':
    print("Iniciando programa de gestión de jardinería inteligente...")

    if not setup_actuators():
        print("No se pudieron configurar los actuadores. Saliendo.")
        exit()

    light_sensor = LightSensor()
    print("Sensor de luz inicializado.")

    # Aseguramos que tenemos los nombres de las bombas ordenados para la lógica de segmentos
    # Esto asume que los nombres de las bombas tienen un formato que permite el ordenamiento lógico (ej. 'bomba_1', 'bomba_2')
    ordered_pump_names = sorted(list(RELAY_PINS.keys()))
    if len(ordered_pump_names) != 4:
        print("Error: El número de bombas configuradas no es 4. Esta lógica requiere 4 bombas.")
        cleanup_gpio()
        exit()

    try:
        while True:
            # --- Lectura y control automático basado en el sensor ---
            current_lux = light_sensor.read_light_level()
            
            # Llama a la función para controlar las bombas automáticamente por rango de luz
            control_pumps_by_light(current_lux, ordered_pump_names)

            time.sleep(PUMP_ACTIVATION_DURATION_SEC + 5) # Espera la duración de la bomba + 5 segundos antes de la siguiente lectura y control automático

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
    finally:
        cleanup_gpio()
        print("Programa finalizado. GPIOs liberados.")
