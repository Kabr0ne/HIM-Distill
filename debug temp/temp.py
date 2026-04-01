from gpiozero import MCP3008
import time

t1 = MCP3008(channel=1)
t2 = MCP3008(channel=2)


def get_temp(sensor):
    voltage = sensor.value * 3.3
    temperature = (voltage - 1.25) / 0.005
    return temperature

while True:
    print(f"Température T1 : {get_temp(t1):.2f}°C")
    print(f"Température T2 : {get_temp(t2):.2f}°C")

    time.sleep(1)