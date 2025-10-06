import board
import digitalio
import analogio
import time

# --- CONFIGURACIÓN DE PINES ---
# Entrada Analógica: Potenciómetro (GP26 / ADC0)
POT_PIN = board.GP26
potenciometro = analogio.AnalogIn(POT_PIN)

# Entrada Digital: Sensor IR (GP16)
SENSOR_IR_PIN = board.GP16
sensor_ir = digitalio.DigitalInOut(SENSOR_IR_PIN)
sensor_ir.direction = digitalio.Direction.INPUT
sensor_ir.pull = digitalio.Pull.UP 

# Salidas Digitales: LEDs de Potencia (GP17, GP18, GP19)
# Estos pines están conectados a un LED cada uno con su respectiva resistencia.
LED_BAJO_PIN = board.GP17
led_bajo = digitalio.DigitalInOut(LED_BAJO_PIN)
led_bajo.direction = digitalio.Direction.OUTPUT

LED_MEDIO_PIN = board.GP18
led_medio = digitalio.DigitalInOut(LED_MEDIO_PIN)
led_medio.direction = digitalio.Direction.OUTPUT

LED_ALTO_PIN = board.GP19
led_alto = digitalio.DigitalInOut(LED_ALTO_PIN)
led_alto.direction = digitalio.Direction.OUTPUT

# Salida Digital: LED de Detección de Obstáculo (GP15)
LED_IR_PIN = board.GP15
led_ir = digitalio.DigitalInOut(LED_IR_PIN)
led_ir.direction = digitalio.Direction.OUTPUT


# Umbrales para los tres niveles de potencia (0 a 65535)
UMBRAL_BAJO = 21845  
UMBRAL_MEDIO = 43690 

estado_anterior_ir = False 

print("Sistema de Detección IR y Medición de Potencia Exclusiva Activo.")
print("V = Valor Analógico (0-65535)")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA Y CONTROL DEL POTENCIÓMETRO (Lógica Exclusiva)
    valor_pot = potenciometro.value
    nivel_potencia = ""
    
    # Reinicio Exclusivo: Asegura que todos los LEDs se apaguen antes de encender uno nuevo
    led_bajo.value = False
    led_medio.value = False
    led_alto.value = False
    
    # Control del único LED encendido
    if valor_pot <= UMBRAL_BAJO:
        # Activa SOLO el LED de BAJA (GP17)
        led_bajo.value = True
        nivel_potencia = "BAJA"
    elif valor_pot <= UMBRAL_MEDIO:
        # Activa SOLO el LED de MEDIA (GP18)
        led_medio.value = True
        nivel_potencia = "MEDIA"
    else: # valor_pot > UMBRAL_MEDIO
        # Activa SOLO el LED de ALTA (GP19)
        led_alto.value = True
        nivel_potencia = "ALTA"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    # Usamos la lógica de: BAJO (False) = Obstáculo
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # 3. SALIDA A CONSOLA 
    mensaje_pot = f"V={valor_pot:<5}" 

    if deteccion_ir != estado_anterior_ir:
        if deteccion_ir:
            print(f"IR: OBSTÁCULO DETECTADO 🛑 | {mensaje_pot} | POTENCIA: {nivel_potencia}")
        else:
            print(f"IR: Camino libre. ✅        | {mensaje_pot} | POTENCIA: {nivel_potencia}")
        
        estado_anterior_ir = deteccion_ir
    else:
        print(f"IR: Estado estable.          | {mensaje_pot} | POTENCIA: {nivel_potencia}")
        
    time.sleep(0.5)