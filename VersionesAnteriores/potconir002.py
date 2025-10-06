import board
import digitalio
import analogio
import time

# --- CONFIGURACIÓN DE PINES ---
# ... [El resto de la configuración de Pines permanece igual] ...

# Entrada Analógica: Potenciómetro (GP26 / ADC0)
POT_PIN = board.GP26
potenciometro = analogio.AnalogIn(POT_PIN)

# Entrada Digital: Sensor IR (GP16)
SENSOR_IR_PIN = board.GP16
sensor_ir = digitalio.DigitalInOut(SENSOR_IR_PIN)
sensor_ir.direction = digitalio.Direction.INPUT
sensor_ir.pull = digitalio.Pull.UP 

# Salidas Digitales: LEDs 
LED_IR_PIN = board.GP15  # LED que indica la detección del obstáculo
led_ir = digitalio.DigitalInOut(LED_IR_PIN)
led_ir.direction = digitalio.Direction.OUTPUT

LED_POT_PIN = board.GP17 # LED que indica el estado del potenciómetro
led_pot = digitalio.DigitalInOut(LED_POT_PIN)
led_pot.direction = digitalio.Direction.OUTPUT


UMBRAL_ACTIVACION = 32768 

print("Sistema IR y Potenciómetro Activo. Compruebe la detección.")

# --- BUCLE PRINCIPAL CON LÓGICA INVERTIDA ---
while True:
    # 1. Leer el Potenciómetro y Controlar su LED (GP17)
    valor_pot = potenciometro.value
    led_pot.value = valor_pot > UMBRAL_ACTIVACION
    # La línea de arriba es una forma más concisa de hacer el if/else

    # 2. Controlar el LED del Sensor IR (GP15)
    
    # LA CORRECCIÓN CLAVE: Usamos 'not' para que el sistema funcione si 
    # el sensor envía BAJO (False) al detectar un obstáculo.
    if not sensor_ir.value:
        # Si el valor es False (BAJO), entonces hay un objeto
        print("¡OBSTÁCULO DETECTADO! 🛑")
        led_ir.value = True       
        
    else:
        # Si el valor es True (ALTO), entonces está despejado
        print("Camino libre. ✅")
        led_ir.value = False      
        
    time.sleep(0.1)