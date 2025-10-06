import board
import digitalio
import analogio
import time

# --- CÓDIGOS DE COLOR ANSI ---
# Se utilizan para formatear el mensaje de salida en la consola de Thonny
COLOR_FONDO_NEGRO = "\033[40m" 
COLOR_ROJO_BRILLANTE = "\033[91m"
COLOR_VERDE_BRILLANTE = "\033[92m"
COLOR_AZUL_CLARO_BRILLANTE = "\033[96m"
COLOR_AMARILLO_BRILLANTE = "\033[93m"
COLOR_FIN = "\033[0m"

# --- CONTADORES DE ITEMS ---
# Se incrementan solo cuando la línea está activa y libre de obstáculos.
item_count_line1 = 0
item_count_line2 = 0
item_count_line3 = 0

# --- CONFIGURACIÓN DE PINES ---
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

print("Sistema de Producción (AJUSTE FINAL de Salida).")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA DEL POTENCIÓMETRO y DEFINICIÓN DE LÍNEA (Control Exclusivo de LEDs)
    valor_pot = potenciometro.value
    linea_produccion = ""
    
    led_bajo.value = False; led_medio.value = False; led_alto.value = False
    
    if valor_pot <= UMBRAL_BAJO:
        led_bajo.value = True
        linea_produccion = "LÍNEA 1 (BAJA)"
    elif valor_pot <= UMBRAL_MEDIO:
        led_medio.value = True
        linea_produccion = "LÍNEA 2 (MEDIA)"
    else: 
        led_alto.value = True
        linea_produccion = "LÍNEA 3 (ALTA)"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # 3. LÓGICA DE CONTEO (SOLO SI LA LÍNEA ESTÁ LIBRE)
    if not deteccion_ir: 
        if valor_pot <= UMBRAL_BAJO:
            item_count_line1 += 1
        elif valor_pot <= UMBRAL_MEDIO:
            item_count_line2 += 1
        else:
            item_count_line3 += 1
    
    
    # 4. SALIDA A CONSOLA (Fondo Negro Uniforme y Alto Contraste)
    
    # a. Definir el texto del estado (IR)
    if deteccion_ir:
        texto_estado = f"{COLOR_ROJO_BRILLANTE}🛑 OBJETO DETECTADO en {linea_produccion}"
    else:
        texto_estado = f"{COLOR_VERDE_BRILLANTE}✅ CONTEO ACTIVO en {linea_produccion}"
    
    # b. Definir el texto de los contadores (Amarillo)
    texto_contadores = (
        f"{COLOR_AMARILLO_BRILLANTE}"
        f"C1:{item_count_line1:<3} C2:{item_count_line2:<3} C3:{item_count_line3:<3}"
    )
    
    # c. Definir el texto del Potenciómetro (Azul Claro)
    texto_pot = f"{COLOR_AZUL_CLARO_BRILLANTE}V:{valor_pot:<5}"
    
    # d. IMPRESIÓN FINAL
    mensaje_compuesto = (
        f"{texto_estado:<40} | " 
        f"{texto_contadores} | "
        f"{texto_pot}"
    )
    
    print(f"{COLOR_FONDO_NEGRO}{mensaje_compuesto}{COLOR_FIN}")
        
    time.sleep(0.5)