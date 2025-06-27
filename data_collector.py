# data_collector.py

import csv
import os
from datetime import datetime

DATA_FILE_PATH = "light_data.csv"

def setup_csv_file():
    try:
        with open(DATA_FILE_PATH, 'x', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "lux"])
            print(f"Archivo CSV '{DATA_FILE_PATH}' creado con éxito.")
    except FileExistsError:
        print(f"Archivo CSV '{DATA_FILE_PATH}' ya existe. No se requiere acción.")
        pass

def _log_data_locally(lux_value):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(DATA_FILE_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, lux_value])
        return timestamp, lux_value
    except Exception as e:
        print(f"Error al escribir en el archivo CSV: {e}")
        return None, None

def collect_and_log_single_reading(light_sensor):
    light_level = light_sensor.read_light_level()

    if light_level is None:
        print("No se pudo leer el nivel de luz del sensor.")
        return

    timestamp, lux = _log_data_locally(light_level)

    if timestamp:
        print(f"Dato guardado localmente: {timestamp} - {lux} lux")
    else:
        print("Error al guardar localmente.")

def clear_csv_file():
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "lux"])
            print(f"Archivo CSV '{DATA_FILE_PATH}' vaciado y encabezado recreado con éxito.")
        except Exception as e:
            print(f"Error al intentar vaciar el archivo CSV: {e}")
    else:
        print(f"El archivo CSV '{DATA_FILE_PATH}' no existe, no se requiere vaciado.")
        setup_csv_file()
