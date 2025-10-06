import board
import digitalio
import analogio
import time

# --- CÓDIGOS DE COLOR ANSI ---
COLOR_FONDO_NEGRO = "\033[40m" 
COLOR_ROJO_BRILLANTE = "\033[91m"
COLOR_VERDE_BRILLANTE = "\033[92m"
COLOR_AZUL_CLARO_BRILLANTE = "\033[96m"
COLOR_AMARILLO_BRILLANTE = "\033[93m"
COLOR_FIN = "\033[0m"

# --- CONTADORES DE ITEMS (Se inicializan fuera del bucle) ---
item_count_line1 = 0
item_count_line2 = 0
item_count_line3 = 0

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

print("Sistema de Producción con Bloqueo de Conteo por Obstáculo Activo.")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA DEL POTENCIÓMETRO y DEFINICIÓN DE LÍNEA
    valor_pot = potenciometro.value
    linea_produccion = ""
    
    led_bajo.value = False; led_medio.value = False; led_alto.value = False
    
    # Lógica de Potencia y Asignación de Línea (Solo enciende el LED y define la línea)
    if valor_pot <= UMBRAL_BAJO:
        led_bajo.value = True
        linea_produccion = "LÍNEA 1 (Tamaño CHI)"
    elif valor_pot <= UMBRAL_MEDIO:
        led_medio.value = True
        linea_produccion = "LÍNEA 2 (Tamaño MED)"
    else: 
        led_alto.value = True
        linea_produccion = "LÍNEA 3 (Tamaño GRA)"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # 3. LÓGICA DE CONTEO (SOLO SI NO HAY OBSTÁCULO)
    if not deteccion_ir: # Si NO hay obstáculo (deteccion_ir es False)
        # Solo se permite contar si la línea está libre
        if valor_pot <= UMBRAL_BAJO:
            item_count_line1 += 1
        elif valor_pot <= UMBRAL_MEDIO:
            item_count_line2 += 1
        else:
            item_count_line3 += 1
    
    
    # 4. SALIDA A CONSOLA (Fondo Negro Uniforme)
    
    # Construcción del mensaje de Obstáculos
    if deteccion_ir:
        # Texto en ROJO si hay obstáculo
        texto_estado = f"{COLOR_ROJO_BRILLANTE}🛑 OBJETO DETECTADO en {linea_produccion}"
    else:
        # Texto en VERDE si NO hay obstáculo
        texto_estado = f"{COLOR_VERDE_BRILLANTE}✅ CONTEO ACTIVO en {linea_produccion}"
    
    # Mensaje de CONTADORES (Amarillo)
    texto_contadores = f"{COLOR_AMARILLO_BRILLANTE}C1:{item_count_line1:<4} C2:{item_count_line2:<4} C3:{item_count_line3:<4}"
    
    # Mensaje del valor del Potenciómetro (Azul Claro)
    texto_pot = f"{COLOR_AZUL_CLARO_BRILLANTE}V:{valor_pot:<5}"
    
    # IMPRESIÓN FINAL: Aplica el fondo negro a toda la línea
    mensaje_final = f"{COLOR_FONDO_NEGRO}{texto_estado:<55} | {texto_contadores} | {texto_pot} {COLOR_FIN}"
    
    print(mensaje_final)
        
    time.sleep(0.)