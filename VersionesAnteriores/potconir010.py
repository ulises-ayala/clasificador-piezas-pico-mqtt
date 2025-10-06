import board
import digitalio
import analogio
import time

# --- CÓDIGOS DE COLOR ANSI ---
# Definimos los códigos de color para hacer el script más limpio
COLOR_ROJO = "\033[91m"     # Para alertas (Detección)
COLOR_VERDE = "\033[92m"    # Para éxito/estado normal (No obstáculo)
COLOR_AZUL_CLARO = "\033[96m" # Para valores numéricos
COLOR_FIN = "\033[0m"       # Código para RESETEAR el color a lo normal

# --- CONFIGURACIÓN DE PINES (Se mantiene igual) ---
POT_PIN = board.GP26
potenciometro = analogio.AnalogIn(POT_PIN)
SENSOR_IR_PIN = board.GP16
sensor_ir = digitalio.DigitalInOut(SENSOR_IR_PIN)
sensor_ir.direction = digitalio.Direction.INPUT
sensor_ir.pull = digitalio.Pull.UP 

LED_BAJO_PIN = board.GP17
led_bajo = digitalio.DigitalInOut(LED_BAJO_PIN)
led_bajo.direction = digitalio.Direction.OUTPUT
LED_MEDIO_PIN = board.GP18
led_medio = digitalio.DigitalInOut(LED_MEDIO_PIN)
led_medio.direction = digitalio.Direction.OUTPUT
LED_ALTO_PIN = board.GP19
led_alto = digitalio.DigitalInOut(LED_ALTO_PIN)
led_alto.direction = digitalio.Direction.OUTPUT
LED_IR_PIN = board.GP15
led_ir = digitalio.DigitalInOut(LED_IR_PIN)
led_ir.direction = digitalio.Direction.OUTPUT


# Umbrales
UMBRAL_BAJO = 21845  
UMBRAL_MEDIO = 43690 

print("Sistema de Producción Activo con Salida de Consola a Color.")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA Y CONTROL DEL POTENCIÓMETRO
    valor_pot = potenciometro.value
    linea_produccion = ""
    
    led_bajo.value = False; led_medio.value = False; led_alto.value = False
    
    # Lógica de Potencia y Asignación de Línea
    if valor_pot <= UMBRAL_BAJO:
        led_bajo.value = True; linea_produccion = "LÍNEA 1 (BAJA)"
    elif valor_pot <= UMBRAL_MEDIO:
        led_medio.value = True; linea_produccion = "LÍNEA 2 (MEDIA)"
    else: 
        led_alto.value = True; linea_produccion = "LÍNEA 3 (ALTA)"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # 3. SALIDA A CONSOLA (¡A COLOR!)
    
    # Construcción del mensaje de Obstáculos
    if deteccion_ir:
        # Mensaje de Alerta (ROJO)
        status_mensaje = f"{COLOR_ROJO}🛑 OBJETO DETECTADO en {linea_produccion}{COLOR_FIN}"
    else:
        # Mensaje Normal (VERDE)
        status_mensaje = f"{COLOR_VERDE}✅ NO HAY OBSTÁCULOS en {linea_produccion}{COLOR_FIN}"
    
    # Mensaje del valor del Potenciómetro (AZUL CLARO)
    mensaje_pot = f"{COLOR_AZUL_CLARO}Valor Potenciómetro: {valor_pot:<5}{COLOR_FIN}"
    
    # Imprime el mensaje completo en una sola línea
    print(f"{status_mensaje:<70} | {mensaje_pot}")
        
    time.sleep(0.5)