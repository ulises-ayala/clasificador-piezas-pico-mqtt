import board
import digitalio
import analogio
import time

# --- CONFIGURACIÓN DE PINES ---
# Entrada Analógica: Potenciómetro (GP26 / ADC0)
# tres lecturas de señales del potenciometro 
POT_PIN = board.GP26
potenciometro = analogio.AnalogIn(POT_PIN)

# Entrada Digital: Sensor IR (GP16)
SENSOR_IR_PIN = board.GP16
sensor_ir = digitalio.DigitalInOut(SENSOR_IR_PIN)
sensor_ir.direction = digitalio.Direction.INPUT
sensor_ir.pull = digitalio.Pull.UP 

# Salidas Digitales: LEDs de Potencia (GP17, GP18, GP19)
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


# Umbrales para los tres LEDs (valores de 0 a 65535)
UMBRAL_BAJO = 21845  
UMBRAL_MEDIO = 43690 

# Variable para registrar el estado anterior del IR y evitar saturar la consola
estado_anterior_ir = False 

print("Sistema de Detección IR y Medición de Potencia Activo.")
print("V = Valor Analógico (0-65535)")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA Y CONTROL DEL POTENCIÓMETRO
    valor_pot = potenciometro.value
    nivel_potencia = ""
    
    # Control de los 3 LEDs de potencia (Lógica en Cascada)
    if valor_pot <= UMBRAL_BAJO:
        led_bajo.value = True
        led_medio.value = False
        led_alto.value = False
        nivel_potencia = "BAJA"
    elif valor_pot <= UMBRAL_MEDIO:
        led_bajo.value = True
        led_medio.value = True
        led_alto.value = False
        nivel_potencia = "MEDIA"
    else: # valor_pot > UMBRAL_MEDIO
        led_bajo.value = True
        led_medio.value = True
        led_alto.value = True
        nivel_potencia = "ALTA"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    # Usamos la lógica que te funcionó (not sensor_ir.value, asumiendo BAJO = Obstáculo)
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # 3. SALIDA A CONSOLA (Reportando ambos estados)
    
    # Preparamos el mensaje del potenciómetro
    mensaje_pot = f"V={valor_pot:<5}" 

    # Reportamos la detección IR solo cuando el estado CAMBIA
    if deteccion_ir != estado_anterior_ir:
        if deteccion_ir:
            print(f"IR: OBSTÁCULO DETECTADO 🛑 | {mensaje_pot} | POTENCIA: {nivel_potencia}")
        else:
            print(f"IR: Camino libre. ✅        | {mensaje_pot} | POTENCIA: {nivel_potencia}")
        
        # Actualizamos el estado
        estado_anterior_ir = deteccion_ir
    else:
        # Si el estado del IR no cambió, mostramos el valor del potenciómetro para actualizar la consola
        print(f"IR: Estado estable.          | {mensaje_pot} | POTENCIA: {nivel_potencia}")
        
    time.sleep(0.5) # Pausa para legibilidad