import board
import pulseio
import time
# --- IMPORTACIÓN CORREGIDA ---
# Importamos la CLASE 'Servo' desde el módulo 'adafruit_motor.servo'
from adafruit_motor.servo import Servo

# --- CONFIGURACIÓN DEL SERVO ---
# Conecta el cable de señal (Naranja/Amarillo) del servo al Pin GP17
SERVO_PIN = board.GP17

# Configura la salida PWM
pwm = pulseio.PWMOut(SERVO_PIN, duty_cycle=2**15, frequency=50)

# Crea el objeto Servo, usando la CLASE Servo importada
# Le pasamos el objeto PWM y los pulsos mínimos/máximos para el MG90S
servo_motor = Servo(pwm, min_pulse=500, max_pulse=2500) 

# --- MOVIMIENTO PRINCIPAL ---
print("Servo MG90S iniciado. Moviendo...")

# 1. Movimiento a 0 grados (Posición inicial)
print("Moviendo a 0 grados.")
servo_motor.angle = 0
time.sleep(1) # Espera 1 segundo

# 2. Movimiento a 90 grados
print("Moviendo a 90 grados.")
servo_motor.angle = 90
time.sleep(2) # Espera 2 segundos

# 3. Regreso a 0 grados
print("Regresando a 0 grados.")
servo_motor.angle = 0
time.sleep(1)

print("Ciclo de prueba terminado.")