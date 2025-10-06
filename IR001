import board
import digitalio
import time

# --- CONFIGURACIÓN DE PINES ---

# Pin para el LED externo (Salida digital)
LED_EXTERNO_PIN = board.GP15
led = digitalio.DigitalInOut(LED_EXTERNO_PIN)
led.direction = digitalio.Direction.OUTPUT

# Pin para el Sensor IR (Entrada digital)
SENSOR_IR_PIN = board.GP16
sensor_ir = digitalio.DigitalInOut(SENSOR_IR_PIN)
sensor_ir.direction = digitalio.Direction.INPUT

# La mayoría de los sensores IR digitales necesitan un pull-up interno 
# para funcionar correctamente como entrada digital.
sensor_ir.pull = digitalio.Pull.UP 

print("Sistema de detección IR con LED externo iniciado.")

# --- BUCLE PRINCIPAL ---
while True:
    # El sensor IR (configurado con pull-up) devuelve:
    # False (LOW) cuando detecta un objeto.
    # True (HIGH) cuando no detecta nada.
    
    # Comprobamos si NO se detecta un objeto (sensor_ir.value es True)
    if not sensor_ir.value:
        # 1. OBSTÁCULO DETECTADO (valor es False)
        print("¡OBSTÁCULO DETECTADO! 🛑")
        led.value = True       # Enciende el LED
        
    else:
        # 2. CAMINO LIBRE (valor es True)
        print("Camino libre. ✅")
        led.value = False      # Apaga el LED
        
    time.sleep(0.1) # Pausa corta para una detección rápida