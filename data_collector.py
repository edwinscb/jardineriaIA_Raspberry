# data_collector.py

import csv
import os
from datetime import datetime

DATA_FILE_PATH = "sensor_data.csv"

def setup_csv_file():
    try:
        with open(DATA_FILE_PATH, 'x', newline='') as f:
            writer = csv.writer(f)
            # Added "humidity_raw" and "humidity_voltage" to the header
            writer.writerow(["timestamp", "lux", "humidity_raw", "humidity_voltage"])
            print(f"Archivo CSV '{DATA_FILE_PATH}' creado con éxito.")
    except FileExistsError:
        print(f"Archivo CSV '{DATA_FILE_PATH}' ya existe. No se requiere acción.")
        pass

def _log_data_locally(lux_value, humidity_raw_value, humidity_voltage_value):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        with open(DATA_FILE_PATH, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, lux_value, humidity_raw_value, humidity_voltage_value])
        return timestamp, lux_value, humidity_raw_value, humidity_voltage_value
    except Exception as e:
        print(f"Error al escribir en el archivo CSV: {e}")
        return None, None, None, None

def collect_and_log_single_reading(light_sensor, humidity_sensor):
    light_level = light_sensor.read_light_level()
    humidity_raw, humidity_voltage = humidity_sensor.read_data()

    if light_level is None:
        print("No se pudo leer el nivel de luz del sensor.")
        return
    
    if humidity_raw is None or humidity_voltage is None:
        print("No se pudieron leer los datos del sensor de humedad.")
        return

    timestamp, lux, hum_raw, hum_voltage = _log_data_locally(light_level, humidity_raw, humidity_voltage)

    if timestamp:
        print(f"Dato guardado localmente: {timestamp} - {lux} lux, Humedad (raw): {hum_raw}, Humedad (voltaje): {hum_voltage:.4f}V")
    else:
        print("Error al guardar localmente.")

def clear_csv_file():
    if os.path.exists(DATA_FILE_PATH):
        try:
            with open(DATA_FILE_PATH, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "lux", "humidity_raw", "humidity_voltage"])
            print(f"Archivo CSV '{DATA_FILE_PATH}' vaciado y encabezado recreado con éxito.")
        except Exception as e:
            print(f"Error al intentar vaciar el archivo CSV: {e}")
    else:
        print(f"El archivo CSV '{DATA_FILE_PATH}' no existe, no se requiere vaciado.")
        setup_csv_file()
