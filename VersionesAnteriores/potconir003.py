import board
import digitalio
import analogio
import time

# --- CONFIGURACIÓN DE PINES ---
POT_PIN = board.GP26
potenciometro = analogio.AnalogIn(POT_PIN)

SENSOR_IR_PIN = board.GP16
sensor_ir = digitalio.DigitalInOut(SENSOR_IR_PIN)
sensor_ir.direction = digitalio.Direction.INPUT
sensor_ir.pull = digitalio.Pull.UP 

LED_IR_PIN = board.GP15
led_ir = digitalio.DigitalInOut(LED_IR_PIN)
led_ir.direction = digitalio.Direction.OUTPUT

LED_POT_PIN = board.GP17
led_pot = digitalio.DigitalInOut(LED_POT_PIN)
led_pot.direction = digitalio.Direction.OUTPUT

# Umbral de activación (Mitad del giro)
UMBRAL_ACTIVACION = 32768 
# Variable para evitar que la consola se inunde
estado_anterior_ir = False 

print("Sistema IR y Potenciómetro Activo. V = Valor del Potenciómetro (0-65535)")
print("----------------------------------------------------------------------")

# --- BUCLE PRINCIPAL ---
while True:
    # 1. LECTURA Y CONTROL DEL POTENCIÓMETRO
    valor_pot = potenciometro.value
    pot_alto = valor_pot > UMBRAL_ACTIVACION
    
    led_pot.value = pot_alto
    
    # 2. LECTURA Y CONTROL DEL SENSOR IR
    # NOTA: Usamos la lógica que te funcionó (si tu sensor envía False al detectar, usa 'if not sensor_ir.value:')
    # Asumiendo que has ajustado el potenciómetro y ahora detecta correctamente:
    deteccion_ir = not sensor_ir.value # Usamos la lógica de BAJO=Obstáculo (la más común)
    
    led_ir.value = deteccion_ir
    
    # 3. SALIDA A CONSOLA (Informando ambos sensores)
    
    # Reportamos el estado del Potenciómetro siempre
    mensaje_pot = f"V={valor_pot:<5}" 

    # Solo mostramos el mensaje de detección del IR cuando el estado CAMBIA
    if deteccion_ir != estado_anterior_ir:
        if deteccion_ir:
            print(f"IR: OBSTÁCULO DETECTADO 🛑 | {mensaje_pot} | POT: ALTO" if pot_alto else f"IR: OBSTÁCULO DETECTADO 🛑 | {mensaje_pot} | POT: BAJO")
        else:
            print(f"IR: Camino libre. ✅        | {mensaje_pot} | POT: ALTO" if pot_alto else f"IR: Camino libre. ✅        | {mensaje_pot} | POT: BAJO")
        
        # Actualizamos el estado para la siguiente iteración
        estado_anterior_ir = deteccion_ir
    else:
        # Si el estado del IR no cambió, solo mostramos una línea simple del potenciómetro
        # Esta línea evita que la consola se quede estática, mostrando solo el valor del potenciómetro.
        print(f"IR: Estado estable.          | {mensaje_pot} | POT: ALTO" if pot_alto else f"IR: Estado estable.          | {mensaje_pot} | POT: BAJO")
        
    time.sleep(0.5) # Aumentamos el tiempo para que la consola sea legible