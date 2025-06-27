# main.py

import time
from sensors import LightSensor
from data_collector import setup_csv_file, collect_and_log_single_reading

def main():
    print("Iniciando aplicación de monitoreo de luz...")

    # 1. Configurar el archivo CSV
    setup_csv_file()

    # 2. Inicializar el sensor de luz
    # Recuerda que la luz podría variar por la fuente que es una ventana,
    # por lo que las lecturas serán dinámicas.
    light_sensor = LightSensor()

    # 3. Bucle principal para recolectar y loguear datos
    try:
        while True:
            collect_and_log_single_reading(light_sensor)
            # Esperar un tiempo antes de la siguiente lectura (ej. 5 segundos)
            time.sleep(5)
    except KeyboardInterrupt:
        print("\nPrograma terminado por el usuario.")
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
    finally:
        print("Aplicación de monitoreo de luz finalizada.")

if __name__ == "__main__":
    main()
