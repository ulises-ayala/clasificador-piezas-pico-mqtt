import board
import pulseio
import servo
import time

# --- CONFIGURACIÓN DEL SERVO ---
# Conecta el cable de señal (Naranja/Amarillo) del servo al Pin GP17
SERVO_PIN = board.GP17

# Configura la salida PWM (Modulación por Ancho de Pulso)
# ¡IMPORTANTE!: Usamos pulseio.PWMOut para acceder a la función!
pwm = pulseio.PWMOut(SERVO_PIN, duty_cycle=2**15, frequency=50)

# Crea el objeto Servo
servo_motor = servo.Servo(pwm)

# --- MOVIMIENTO PRINCIPAL ---
print("Servo MG90S iniciado. Moviendo...")

# 1. Movimiento a 0 grados (Posición inicial)
print("Moviendo a 0 grados.")
servo_motor.angle = 0
time.sleep(1) 

# 2. Movimiento a 90 grados
print("Moviendo a 90 grados.")
servo_motor.angle = 90
time.sleep(2) 

# 3. Regreso a 0 grados
print("Regresando a 0 grados.")
servo_motor.angle = 0
time.sleep(1)

print("Ciclo de prueba terminado.")