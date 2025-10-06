import board
import digitalio
import analogio
import time

# --- CONFIGURACIÓN DE PINES ---

# 1. Entrada Analógica: Potenciómetro (GP26 / ADC0)
POT_PIN = board.GP26
potenciometro = analogio.AnalogIn(POT_PIN)

# 2. Entrada Digital: Sensor IR (GP16)
SENSOR_IR_PIN = board.GP16
sensor_ir = digitalio.DigitalInOut(SENSOR_IR_PIN)
sensor_ir.direction = digitalio.Direction.INPUT
sensor_ir.pull = digitalio.Pull.UP 

# 3. Salidas Digitales: LEDs (con resistencia de 220 Ohm)
LED_IR_PIN = board.GP15  # LED que indica la detección del obstáculo
led_ir = digitalio.DigitalInOut(LED_IR_PIN)
led_ir.direction = digitalio.Direction.OUTPUT

LED_POT_PIN = board.GP17 # LED que indica el estado del potenciómetro
led_pot = digitalio.DigitalInOut(LED_POT_PIN)
led_pot.direction = digitalio.Direction.OUTPUT


# Umbral de activación para el LED del potenciómetro (Mitad de giro)
UMBRAL_ACTIVACION = 32768 
# Umbral para la sensibilidad del IR (Podríamos usarlo para lógica avanzada, pero aquí es solo indicador)

print("Sistema IR y Potenciómetro Activo.")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. Leer el Potenciómetro
    valor_pot = potenciometro.value
    
    # 2. Controlar el LED del Potenciómetro (GP17)
    if valor_pot > UMBRAL_ACTIVACION:
        led_pot.value = True       # ENCIENDE el LED (Indica "Alto")
        # print(f"Potenciómetro Alto: {valor_pot}")
    else:
        led_pot.value = False      # APAGA el LED (Indica "Bajo")
        # print(f"Potenciómetro Bajo: {valor_pot}")


    # 3. Controlar el LED del Sensor IR (GP15)
    
    # Si detecta True/HIGH (Usando la lógica que te funcionó):
    if sensor_ir.value:
        # Indica detección
        print("¡OBSTÁCULO DETECTADO! 🛑")
        led_ir.value = True       
        
    else:
        # Indica camino libre
        print("Camino libre. ✅")
        led_ir.value = False      
        
    time.sleep(0.1)