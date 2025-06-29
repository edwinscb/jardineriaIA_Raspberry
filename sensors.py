import smbus
import time
import config
import adafruit_ads1x15.ads1115 as ADS
import board

from adafruit_ads1x15.analog_in import AnalogIn

class HumiditySensor:
    def __init__(self, i2c_bus=None, device_address=None, analog_pin_index=None):
        if device_address is None:
            import config
            device_address = config.ADS1115_DEVICE_ADDRESS
        if analog_pin_index is None:
            import config
            analog_pin_index = config.ADS1115_ANALOG_PIN

        if i2c_bus is None:
            self.i2c = board.I2C()
        else:
            self.i2c = i2c_bus
        
        self.ads = ADS.ADS1115(self.i2c, address=device_address)

        ads_pins = [ADS.P0, ADS.P1, ADS.P2, ADS.P3]
        if 0 <= analog_pin_index <= 3:
            self.channel = AnalogIn(self.ads, ads_pins[analog_pin_index])
        else:
            raise ValueError("ADS1115_ANALOG_PIN must be between 0 and 3.")

        print(f"[OK] Convertidor ADS1115 en 0x{device_address:x} inicializado en pin P{analog_pin_index}.")

    def read_data(self):
        try:
            raw_value = self.channel.value
            voltage = self.channel.voltage
            return raw_value, voltage
        except Exception as e:
            print(f"Error al leer los datos del sensor de humedad: {e}")
            return None, None

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
