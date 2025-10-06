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

print("Sistema de Producción Activo. La salida se actualiza continuamente.")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA Y CONTROL DEL POTENCIÓMETRO
    valor_pot = potenciometro.value
    linea_produccion = ""
    
    # Reinicio Exclusivo
    led_bajo.value = False
    led_medio.value = False
    led_alto.value = False
    
    # Control de LEDs y Asignación de Línea de Producción
    if valor_pot <= UMBRAL_BAJO:
        led_bajo.value = True
        linea_produccion = "LÍNEA 1 (BAJA)"
    elif valor_pot <= UMBRAL_MEDIO:
        led_medio.value = True
        linea_produccion = "LÍNEA 2 (MEDIA)"
    else: # valor_pot > UMBRAL_MEDIO
        led_alto.value = True
        linea_produccion = "LÍNEA 3 (ALTA)"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # 3. SALIDA A CONSOLA (Construcción del mensaje de una sola línea)
    
    # Define la parte del mensaje de Obstáculos
    if deteccion_ir:
        # Si hay detección (LED GP15 encendido)
        status_mensaje = f"🛑 OBJETO DETECTADO en {linea_produccion}"
    else:
        # Si NO hay detección (LED GP15 apagado)
        status_mensaje = f"✅ NO HAY OBSTÁCULOS en {linea_produccion}"
    
    # Imprime el mensaje completo y la lectura del potenciómetro
    print(f"{status_mensaje:<45} | Valor Potenciómetro: {valor_pot:<5}")
        
    time.sleep(0.5)