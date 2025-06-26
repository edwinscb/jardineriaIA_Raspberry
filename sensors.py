import smbus
import time
import config

class LightSensor:
    def __init__(self, device_address=config.BH1750_DEVICE_ADDRESS, bus_number=config.I2C_BUS_NUMBER):
        self.device_address = device_address
        self.bus = smbus.SMBus(bus_number)
        self._power_on()

    def _power_on(self):
        try:
            self.bus.write_byte(self.device_address, config.BH1750_POWER_ON_CMD)
            self.bus.write_byte(self.device_address, config.BH1750_CONTINUOUS_HIGH_RES_MODE_1_CMD)
            time.sleep(config.BH1750_MEASUREMENT_DELAY_SEC)
        except Exception as e:
            print(f"Error al inicializar el sensor GY-30: {e}")

    def read_light_level(self):
        try:
            data = self.bus.read_i2c_block_data(self.device_address, 0x00, 2)
            
            raw_data = (data[0] << 8) | data[1]
            lux = round(raw_data / config.BH1750_LUX_CONVERSION_DIVIDER, 2)
            return lux
        except Exception as e:
            print(f"Error al leer el sensor GY-30: {e}")
            return None
