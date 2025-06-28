import time
from sensors import LightSensor # Asume que LightSensor está en un archivo llamado sensors.py
import config # Asegúrate de que tu archivo config.py exista y tenga los valores correctos
from actuators import setup_actuators, turn_pump_on, turn_pump_off, cleanup_gpio
from data_collector import setup_csv_file, collect_and_log_single_reading # Importar funciones del data_collector

def main():
    print("Iniciando prueba del sensor de luz GY-30 y control de bombas...")
    sensor = None
    try:
        # Configurar los actuadores (bombas)
        if not setup_actuators():
            print("No se pudieron configurar los actuadores. Saliendo.")
            return

        # Configurar el archivo CSV para guardar datos
        setup_csv_file()

        # Inicializar el sensor de luz
        sensor = LightSensor()
        print("Sensor inicializado correctamente. Leyendo niveles de luz y controlando bombas...")

        # Variables para controlar el estado actual de las bombas
        current_pump_on = None # 'bomba_1', 'bomba_2', or None

        while True:
            # Leer el nivel de luz y guardarlo
            lux = sensor.read_light_level()
            if lux is not None:
                print(f"Nivel de luz: {lux} lux")

                # Log the data to CSV
                # Note: collect_and_log_single_reading already prints the "Dato guardado" message
                collect_and_log_single_reading(sensor)


                if lux > 240:
                    # Si la luz es mayor a 240 y la bomba 2 no está encendida
                    if current_pump_on != 'bomba_2':
                        print("Luz alta ( > 240 lux). Activando bomba 2.")
                        turn_pump_off('bomba_1') # Asegúrate de apagar la bomba 1 si estaba encendida
                        turn_pump_on('bomba_2')
                        current_pump_on = 'bomba_2'
                else:
                    # Si la luz es menor o igual a 240 y la bomba 1 no está encendida
                    if current_pump_on != 'bomba_1':
                        print("Luz baja ( <= 240 lux). Activando bomba 1.")
                        turn_pump_off('bomba_2') # Asegúrate de apagar la bomba 2 si estaba encendida
                        turn_pump_on('bomba_1')
                        current_pump_on = 'bomba_1'
            else:
                print("No se pudo leer el nivel de luz.")
            time.sleep(2) # Lee cada 2 segundos
    except KeyboardInterrupt:
        print("\nPrueba de sensor y control de bombas detenida por el usuario.")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado en el programa principal: {e}")
    finally:
        # Asegurarse de apagar ambas bombas y limpiar los GPIOs al salir
        print("Apagando bombas y limpiando GPIOs...")
        turn_pump_off('bomba_1')
        turn_pump_off('bomba_2')
        cleanup_gpio()

if __name__ == "__main__":
    main()
