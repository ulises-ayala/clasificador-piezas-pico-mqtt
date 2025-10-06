import board, pwmio, time
pwm = pwmio.PWMOut(board.GP15, frequency=50)

while True:
    pwm.duty_cycle = 4915  # pulso medio (~1.5 ms) → debería ir al centro
    time.sleep(2)
