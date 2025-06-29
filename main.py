import time
from sensors import LightSensor, HumiditySensor
import config
from actuators import setup_actuators, turn_pump_on, turn_pump_off, cleanup_gpio
from data_collector import setup_csv_file, collect_and_log_single_reading

def main():
    print("Iniciando prueba del sensor de luz GY-30, sensor de humedad y control de bombas...")
    light_sensor = None
    humidity_sensor = None

    try:
        if not setup_actuators():
            print("No se pudieron configurar los actuadores. Saliendo.")
            return

        setup_csv_file()

        light_sensor = LightSensor()
        print("Sensor de luz inicializado correctamente.")

        humidity_sensor = HumiditySensor()
        print("Sensor de humedad inicializado correctamente.")
        
        print("Leyendo niveles de luz y humedad, y controlando bombas...")

        current_pump_on = None

        while True:
            collect_and_log_single_reading(light_sensor, humidity_sensor)

            lux = light_sensor.read_light_level()

            if lux is not None:
                print(f"Nivel de luz para control: {lux} lux")

                if lux > 240:
                    if current_pump_on != 'bomba_2':
                        print("Luz alta ( > 240 lux). Activando bomba 2.")
                        turn_pump_off('bomba_1')
                        turn_pump_on('bomba_2')
                        current_pump_on = 'bomba_2'
                else:
                    if current_pump_on != 'bomba_1':
                        print("Luz baja ( <= 240 lux). Activando bomba 1.")
                        turn_pump_off('bomba_2')
                        turn_pump_on('bomba_1')
                        current_pump_on = 'bomba_1'
            else:
                print("No se pudo obtener el nivel de luz para la lógica de control.")
                
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nPrueba de sensores y control de bombas detenida por el usuario.")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado en el programa principal: {e}")
    finally:
        print("Apagando bombas y limpiando GPIOs...")
        turn_pump_off('bomba_1')
        turn_pump_off('bomba_2')
        cleanup_gpio()

if __name__ == "__main__":
    main()
