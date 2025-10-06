import time
import board
import pwmio
from adafruit_motor import servo

# Configurar el pin (cambia GP14 si usaste otro)
pwm = pwmio.PWMOut(board.GP14, duty_cycle=2 ** 15, frequency=50)
mi_servo = servo.Servo(pwm)

print("Prueba de servo iniciada...")

while True:
    for angulo in [0, 45, 90, 135, 180]:
        print(f"Moviendo a {angulo} grados")
        try:
            mi_servo.angle = angulo
        except Exception as e:
            print("Error controlando el servo:", e)
        time.sleep(1)
