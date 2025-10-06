import time
import board
import pwmio

# Configurar PWM en GP14 (cambia el pin si lo conectaste a otro)
servo_pwm = pwmio.PWMOut(board.GP14, frequency=50)

print("Prueba cruda de PWM en servo MG90S")

while True:
    # Pulso corto (~0.5 ms) → debería ir a 0 grados
    servo_pwm.duty_cycle = 1638   # equivale aprox. a 0°
    print("0 grados")
    time.sleep(1)

    # Pulso medio (~1.5 ms) → debería ir al centro (90 grados)
    servo_pwm.duty_cycle = 4915   # aprox. 90°
    print("90 grados")
    time.sleep(1)

    # Pulso largo (~2.5 ms) → debería ir a 180 grados
    servo_pwm.duty_cycle = 8192   # aprox. 180°
    print("180 grados")
    time.sleep(1)
