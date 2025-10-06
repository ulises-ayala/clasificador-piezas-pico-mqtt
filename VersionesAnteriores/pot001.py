import board
import analogio
import digitalio
import time

# --- CONFIGURACIÓN DE PINES ---
# LED (Salida Digital) - Para encender/apagar el LED
LED_PIN = board.GP17
led = digitalio.DigitalInOut(LED_PIN)
led.direction = digitalio.Direction.OUTPUT

# Potenciómetro (Entrada Analógica) - Conectado al pin GP26 (ADC0)
POT_PIN = board.GP26
potenciometro = analogio.AnalogIn(POT_PIN)

# Umbral de activación (aproximadamente la mitad del giro del potenciómetro)
# El valor analógico va de 0 a 65535 en CircuitPython.
UMBRAL_ACTIVACION = 32768 

print("Sistema de control de LED por Potenciómetro iniciado.")

# --- BUCLE PRINCIPAL ---
while True:
    # Lee el valor del potenciómetro (valor de 0 a 65535)
    valor_pot = potenciometro.value
    
    # Comprobación de la condición
    if valor_pot > UMBRAL_ACTIVACION:
        # El potenciómetro ha superado el 50%
        print(f"Potencia ALTA: {valor_pot}. Encendiendo LED.")
        led.value = True       # Enciende el LED
    else:
        # El potenciómetro está por debajo del 50%
        print(f"Potencia BAJA: {valor_pot}. Apagando LED.")
        led.value = False      # Apaga el LED
    
    time.sleep(0.1)