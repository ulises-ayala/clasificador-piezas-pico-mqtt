import board
import digitalio
import analogio
import time

# --- CÓDIGOS DE COLOR ANSI ---
# Códigos para FONDO NEGRO y TEXTO BRILLANTE

COLOR_FONDO_NEGRO = "\033[40m" # Código para el fondo de texto negro

COLOR_ROJO_BRILLANTE = "\033[91m"     # Texto Rojo Brillante (Alerta)
COLOR_VERDE_BRILLANTE = "\033[92m"    # Texto Verde Brillante (Éxito)
COLOR_AZUL_CLARO_BRILLANTE = "\033[96m" # Texto Cian Brillante (Valores)

COLOR_FIN = "\033[0m"       # Código para RESETEAR el color y el fondo

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
    
    
    # 3. SALIDA A CONSOLA (¡Con Fondo Negro!)
    
    # 3a. Construcción del mensaje de Obstáculos
    if deteccion_ir:
        # Mensaje de Alerta (ROJO, Fondo NEGRO)
        status_mensaje = f"{COLOR_FONDO_NEGRO}{COLOR_ROJO_BRILLANTE}🛑 OBJETO DETECTADO en {linea_produccion}{COLOR_FIN}"
    else:
        # Mensaje Normal (VERDE, Fondo NEGRO)
        status_mensaje = f"{COLOR_FONDO_NEGRO}{COLOR_VERDE_BRILLANTE}✅ NO HAY OBSTÁCULOS en {linea_produccion}{COLOR_FIN}"
    
    # 3b. Mensaje del valor del Potenciómetro (AZUL, Fondo NEGRO)
    # Reaplicamos el fondo para la segunda parte de la línea
    mensaje_pot = f"{COLOR_FONDO_NEGRO}{COLOR_AZUL_CLARO_BRILLANTE}Valor Potenciómetro: {valor_pot:<5}{COLOR_FIN}"
    
    # 3c. Imprime el mensaje completo en una sola línea
    # Nota: El relleno de espacios (<70) también tendrá el fondo negro.
    print(f"{status_mensaje:<70} | {mensaje_pot}")
        
    time.sleep(0.5)