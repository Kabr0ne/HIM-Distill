import mcp3008
import time

adc = mcp3008.MCP3008()
CORRECTION_PONT = 1.555
OFFSET_CAPTEUR = 1.25  
VOLT_REF_ADC = 3.3      

def lire_temp(canal):
    raw_val = adc.read([canal])[0]

    v_mcp = (raw_val * VOLT_REF_ADC) / 1023.0
    
    v_reel = v_mcp * CORRECTION_PONT
    
    temp = (v_reel - OFFSET_CAPTEUR) / 0.005
    return raw_val, v_reel, temp

while True:
    raw1, v1, t1 = lire_temp(mcp3008.CH0)
    raw2, v2, t2 = lire_temp(mcp3008.CH1)
    
    print("-" * 40)
    print(f"SONDE 1 (CH0) | Brut: {raw1:4} | V: {v1:.2f}V | Temp: {t1:6.2f} °C")
    print(f"SONDE 2 (CH1) | Brut: {raw2:4} | V: {v2:.2f}V | Temp: {t2:6.2f} °C")
    
    time.sleep(1.5)