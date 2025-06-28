import smbus
import time
import config

class LightSensor:
    def __init__(self, device_address=config.BH1750_DEVICE_ADDRESS, bus_number=config.I2C_BUS_NUMBER):
        self.device_address = device_address
        self.bus = smbus.SMBus(bus_number)

    def read_light_level(self):
        try:
            # Enviar comando de medición de una sola vez en alta resolución
            self.bus.write_byte(self.device_address, config.BH1750_ONE_TIME_HIGH_RES_MODE_1_CMD)

            # Esperar a que el sensor termine la medición
            time.sleep(config.BH1750_MEASUREMENT_DELAY_SEC)

            # Leer los datos del sensor (2 bytes)
            data = self.bus.read_i2c_block_data(self.device_address, 0x00, 2)

            # Convertir los bytes a valor en lux
            result = (data[0] << 8) | data[1]
            lux = result / 1.2  # Escalado según el datasheet del BH1750
            return lux
        except Exception as e:
            print(f"Error al leer el nivel de luz: {e}")
            return None
