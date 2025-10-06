import board
import digitalio
import analogio
import time

import json

import wifi
import socketpool
import adafruit_minimqtt.adafruit_minimqtt as MQTT

#SERVO
import pwmio
from adafruit_motor import servo
SERVO_PIN = board.GP13  # o el pin que uses para el cable naranja
pwm_servo = pwmio.PWMOut(SERVO_PIN, duty_cycle=2 ** 15, frequency=50)
mi_servo = servo.Servo(pwm_servo)

# Configuración de RED
#SSID = "wfrre-Docentes"
#PASSWORD = "20$tscFrre.24"
#BROKER = "10.13.100.154"  
#NOMBRE_EQUIPO = "masones"
#DESCOVERY_TOPIC = "descubrir"
#TOPIC = f"sensores/{NOMBRE_EQUIPO}"

#print(f"Intentando conectar a {SSID}...")
#try:
#    wifi.radio.connect(SSID, PASSWORD)
#    print(f"Conectado a {SSID}")
#    print(f"Dirección IP: {wifi.radio.ipv4_address}")
#except Exception as e:
#    print(f"Error al conectar a WiFi: {e}")
#    while True:
#       pass 

# Configuración MQTT 
#pool = socketpool.SocketPool(wifi.radio)

#def connect(client, userdata, flags, rc):
#    print("Conectado al broker MQTT")
#    client.publish(DESCOVERY_TOPIC, json.dumps({"equipo":NOMBRE_EQUIPO,"magnitudes": ["deteccion_objeto", "voltaje"]}))

#mqtt_client = MQTT.MQTT(
#    broker=BROKER,
#    port=1883,
#    socket_pool=pool
#)

#mqtt_client.on_connect = connect
#mqtt_client.connect()

# Variables dglobales para cerrar y abrir compuertas
ANG_L1 = 10     # línea 1 (bajo)
ANG_L2 = 90     # línea 2 (medio)
ANG_L3 = 170    # línea 3 (alto)
ultimo_angulo_servo = None

# Usamos estas varaibles globales para controlar cada cuanto publicamos
last_pub = 0
PUB_INTERVAL = 5  
def publish():
    global last_pub
    now = time.monotonic()
   
    if now - last_pub >= PUB_INTERVAL:
        try:
            topic = f"{TOPIC}/voltaje" 
            mqtt_client.publish(topic, str(potenciometro.value))
            
            hum_topic = f"{TOPIC}/deteccion_objeto" 
            mqtt_client.publish(hum_topic, str(sensor_ir.value))
            
            last_pub = now
          
        except Exception as e:
            print(f"Error publicando MQTT: {e}")


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
    
    # Lógica de Potencia y Asignación de Línea (Solo enciende el LED y define la línea)
    if valor_pot <= UMBRAL_BAJO:
        led_bajo.value = True
        linea_produccion = "LÍNEA 1 (CHI)"
    elif valor_pot <= UMBRAL_MEDIO:
        led_medio.value = True
        linea_produccion = "LÍNEA 2 (MED)"
    else: 
        led_alto.value = True
        linea_produccion = "LÍNEA 3 (GRA)"


    # 2. LECTURA Y CONTROL DEL SENSOR IR
    deteccion_ir = not sensor_ir.value 
    led_ir.value = deteccion_ir
    
    
    # --- CAMBIO CLAVE: LÓGICA DE CONTEO (SOLO SI NO HAY OBSTÁCULO) ---
    if not deteccion_ir: # Si NO hay obstáculo (deteccion_ir es False)
        # Solo se permite contar si la línea está libre
        if valor_pot <= UMBRAL_BAJO:
            item_count_line1 += 1
            target = ANG_L1

        elif valor_pot <= UMBRAL_MEDIO:
            item_count_line2 += 1
            target = ANG_L2

        else:
            item_count_line3 += 1
            target = ANG_L3
    
    # solo mover si cambió de verdad
    if target != ultimo_angulo_servo:
        mi_servo.angle = target
        ultimo_angulo_servo = target
    # -------------------------------------------------------------------
    
    
    # 3. SALIDA A CONSOLA (Fondo Negro Uniforme)
    
    # 3a. Construcción del mensaje de Obstáculos
    if deteccion_ir:
        # Texto en ROJO si hay obstáculo
        texto_estado = f"{COLOR_ROJO_BRILLANTE}🛑 OBJETO DETECTADO en {linea_produccion}"
    else:
        # Texto en VERDE si NO hay obstáculo
        texto_estado = f"{COLOR_VERDE_BRILLANTE}✅ CONTEO ACTIVO en {linea_produccion}" # Mensaje actualizado
    
    # 3b. Mensaje de CONTADORES (Amarillo)
    texto_contadores = f"{COLOR_AMARILLO_BRILLANTE}Conteo L1:{item_count_line1:<4} Conteo L2:{item_count_line2:<4} Conteo L3:{item_count_line3:<4}"
    
    # 3c. Mensaje del valor del Potenciómetro (Azul Claro)
    texto_pot = f"{COLOR_AZUL_CLARO_BRILLANTE}V:{valor_pot:<5}"
    
    # 3d. IMPRESIÓN FINAL: Aplica el fondo negro a toda la línea
    mensaje_final = f"{COLOR_FONDO_NEGRO}{texto_estado:<55} | {texto_contadores} | {texto_pot} {COLOR_FIN}"
    
    print(mensaje_final)
    publish()
    time.sleep(0.5)
    
    