import board
import digitalio
import analogio
import time

# --- CÓDIGOS DE COLOR ANSI ---
COLOR_FONDO_NEGRO = "\033[40m" 
COLOR_ROJO_BRILLANTE = "\033[91m"
COLOR_VERDE_BRILLANTE = "\033[92m"
COLOR_AZUL_CLARO_BRILLANTE = "\033[96m"
COLOR_FIN = "\033[0m"

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

print("Sistema de Producción con Consola de Alto Contraste Activo.")
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
    
    
    # 3. SALIDA A CONSOLA (Fondo Negro Uniforme)
    
    # 3a. Construcción del mensaje de Obstáculos
    if deteccion_ir:
        # Texto en ROJO
        texto_estado = f"{COLOR_ROJO_BRILLANTE}🛑 OBJETO DETECTADO en {linea_produccion}"
    else:
        # Texto en VERDE
        texto_estado = f"{COLOR_VERDE_BRILLANTE}✅ NO HAY OBSTÁCULOS en {linea_produccion}"
    
    # Texto del valor del Potenciómetro en AZUL CLARO
    texto_pot = f"{COLOR_AZUL_CLARO_BRILLANTE}Valor Potenciómetro: {valor_pot:<5}"
    
    # 3c. IMPRESIÓN FINAL: Aplica el fondo negro al inicio de la línea.
    # Usamos f-string para concatenar las partes. 
    # El relleno de espacios (padding) en el centro de la cadena asegurará que se vea el fondo negro.
    mensaje_final = f"{COLOR_FONDO_NEGRO}{texto_estado:<55} | {texto_pot} {COLOR_FIN}"
    
    print(mensaje_final)
        
    time.sleep(0.5)