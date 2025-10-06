import board, pwmio, time

servo_pwm = pwmio.PWMOut(board.GP13, frequency=50)  # cambiá GP15 por el pin que uses

while True:
    servo_pwm.duty_cycle = 1638   # 0 grados
    time.sleep(1)
    servo_pwm.duty_cycle = 4915   # 90 grados
    time.sleep(1)
    servo_pwm.duty_cycle = 8192   # 180 grados
    time.sleep(1)
