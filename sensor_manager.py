from gpiozero import MCP3008
import config

class SensorManager:
    def __init__(self, name, channel):
        self.name = name
        self.adc = MCP3008(channel=channel)

    def read_temp(self):
        try:
            voltage = self.adc.value * config.tension_rasp
            v_reel = voltage * config.pont_diviseur_ratio
            temp = (v_reel - config.offset_thermocouple) / 0.005
            return temp
        except Exception as e:
            print(f"Erreur capteur {self.name}: {e}")
            return None