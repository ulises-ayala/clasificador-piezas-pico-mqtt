# --- BUCLE PRINCIPAL (MODIFICADO) ---
while True:
    # Intenta invertir la lógica (comprueba si es True, que significa OBSTÁCULO)
    # Algunas versiones de este sensor envían ALTO (True) al detectar.
    if sensor_ir.value: # CAMBIO: Eliminamos el 'not'
        # 1. OBSTÁCULO DETECTADO (Si el sensor envía True)
        print("¡OBSTÁCULO DETECTADO! 🛑")
        led.value = True       # Enciende el LED
        
    else:
        # 2. CAMINO LIBRE (Si el sensor envía False)
        print("Camino libre. ✅")
        led.value = False      # Apaga el LED
        
    time.sleep(0.1)