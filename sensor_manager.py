import time

from gpiozero import MCP3008
import config

class SensorManager:
    def __init__(self, name, channel):
        self.name = name
        self.adc = MCP3008(channel=channel)

    def read_temp(self):
        try:
            data_temp = []
            data_temp.append(self.adc.value)
            for i in range(1, 10):
                data_temp.append(self.adc.value)
                time.sleep(0.02)
            average_value = sum(data_temp) / len(data_temp)

            voltage = average_value * config.tension_rasp
            v_reel = voltage * config.pont_diviseur_ratio
            temp = (v_reel - config.offset_thermocouple) / 0.005
            return temp
        except Exception as e:
            print(f"Erreur capteur {self.name}: {e}")
            return None