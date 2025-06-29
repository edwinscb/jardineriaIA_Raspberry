# config.py

RELAY_PINS = {
    "bomba_1": 14,
    "bomba_2": 15,
    "bomba_3": 18,
    "bomba_4": 4
}
# Dirección del sensor BH1750 (puede ser 0x23 o 0x5C dependiendo del módulo)
BH1750_DEVICE_ADDRESS = 0x23

# Número de bus I2C (normalmente 1 en Raspberry Pi)
I2C_BUS_NUMBER = 1

# Comando para modo de alta resolución, medición única
BH1750_ONE_TIME_HIGH_RES_MODE_1_CMD = 0x20

# Tiempo que tarda el sensor en hacer la medición
BH1750_MEASUREMENT_DELAY_SEC = 0.2

PUMP_ACTIVATION_DURATION_SEC = 3 # Duración de activación de bomba de ejemplo

# --- Configuraciones para el Sensor de Humedad (ADS1115) ---
ADS1115_DEVICE_ADDRESS = 0x48 # Dirección I2C del ADS1115 (verifica si es diferente en tu configuración)
ADS1115_ANALOG_PIN = 0 # El pin analógico del ADS1115 al que está conectado el sensor de humedad (P0, P1, P2, P3)
