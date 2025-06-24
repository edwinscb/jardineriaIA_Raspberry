# actuators.py
import RPi.GPIO as GPIO
from config import RELAY_PINS

GPIO_SETUP_DONE = False

def setup_actuators():
    global GPIO_SETUP_DONE
    if not GPIO_SETUP_DONE:
        try:
            GPIO.setmode(GPIO.BCM)
            for pump_name, pin in RELAY_PINS.items():
                GPIO.setup(pin, GPIO.OUT)
                GPIO.output(pin, GPIO.HIGH)
            GPIO_SETUP_DONE = True
            print("Todos los GPIOs de actuadores configurados.")
        except RuntimeError as e:
            print(f"Error al configurar GPIOs: {e}. Intenta con 'sudo'.")
            GPIO_SETUP_DONE = False
        return GPIO_SETUP_DONE

def turn_pump_on(pump_id):
    if not GPIO_SETUP_DONE:
        if not setup_actuators():
            print(f"No se pudo encender la bomba {pump_id}: GPIOs no configurados.")
            return

    pin = RELAY_PINS.get(pump_id)
    if pin is not None:
        GPIO.output(pin, GPIO.LOW)
        print(f"Bomba '{pump_id}' (GPIO {pin}) ENCENDIDA.")
    else:
        print(f"Error: Bomba '{pump_id}' no encontrada.")

def turn_pump_off(pump_id):
    if not GPIO_SETUP_DONE:
        if not setup_actuators():
            print(f"No se pudo apagar la bomba {pump_id}: GPIOs no configurados.")
            return

    pin = RELAY_PINS.get(pump_id)
    if pin is not None:
        GPIO.output(pin, GPIO.HIGH)
        print(f"Bomba '{pump_id}' (GPIO {pin}) APAGADA.")
    else:
        print(f"Error: Bomba '{pump_id}' no encontrada.")

def cleanup_gpio():
    global GPIO_SETUP_DONE
    if GPIO_SETUP_DONE:
        GPIO.cleanup()
        print("GPIOs limpiados.")
        GPIO_SETUP_DONE = False
    else:
        print("No se configuraron GPIOs, no hay nada que limpiar.")
