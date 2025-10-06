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

estado_anterior_ir = False 

print("Sistema de Producción con Control de Potencia Activo.")
print("V = Valor Analógico (0-65535)")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA Y CONTROL DEL POTENCIÓMETRO (Lógica Exclusiva)
    valor_pot = potenciometro.value
    
    # Variables para los mensajes
    mensaje_potencia_habilitada = ""
    mensaje_deteccion_linea = ""
    
    # Reinicio Exclusivo: Asegura que todos los LEDs se apaguen
    led_bajo.value = False
    led_medio.value = False
    led_alto.value = False
    
    # Control de LEDs y Asignación de Mensajes de Línea de Producción
    if valor_pot <= UMBRAL_BAJO:
        led_bajo.value = True
        mensaje_potencia_habilitada = "Linea de producción 1 habilitada"
        mensaje_deteccion_linea = "objeto detectado en linea de producción 1"
    elif valor_pot <= UMBRAL_MEDIO:
        led_medio.value = True
        mensaje_potencia_habilitada = "Linea de producción 2 habilitada"
        mensaje_deteccion_linea = "objeto detectado en linea de producción 2"
    else: # valor_pot > UMBRAL_MEDIO
        led_alto.value = True
        mensaje_potencia_habilitada = "Linea de producción 3 habilitada"
        mensaje_deteccion_linea = "objeto detectado en linea de producción 3"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # 3. SALIDA A CONSOLA (Reporte Dinámico)
    mensaje_pot = f"V={valor_pot:<5}" 

    if deteccion_ir != estado_anterior_ir:
        if deteccion_ir:
            # Reporta la detección con el mensaje específico de la línea
            print(f"IR: 🛑 {mensaje_deteccion_linea:<40} | {mensaje_pot}")
        else:
            # Reporta que la línea está libre con el mensaje de habilitación
            print(f"IR: ✅ {mensaje_potencia_habilitada:<40} | {mensaje_pot}")
        
        estado_anterior_ir = deteccion_ir
    else:
        # Si el estado es estable, reporta el estado de habilitación
        print(f"IR: Estable. {mensaje_potencia_habilitada:<40} | {mensaje_pot}")
        
    time.sleep(0.5)