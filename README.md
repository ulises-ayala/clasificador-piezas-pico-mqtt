# TDA – TP Microcontrolador (Laboratorio 1)
 
Sistema de clasificación y conteo de piezas por líneas de producción, programado en **CircuitPython** sobre una **Raspberry Pi Pico 2 W**. Un potenciómetro simula el tamaño de la pieza, un sensor infrarrojo detecta obstáculos, un servo actúa como compuerta y los datos se publican por **MQTT**.
 
> Primer laboratorio de la materia (Técnicas de Automatización). El [Laboratorio 2](https://github.com/ulises-ayala/Laboratorio-2---TPA) resuelve una lógica equivalente con un PLC (OpenPLC, Ladder).
 
## Qué hace
 
1. Lee el potenciómetro (ADC, GP26) y asigna la pieza a una de tres líneas:
   | Rango de lectura (0–65535) | Línea | LED |
   |---|---|---|
   | ≤ 21845 | Línea 1 (chica) | GP17 |
   | ≤ 43690 | Línea 2 (mediana) | GP18 |
   | > 43690 | Línea 3 (grande) | GP19 |
2. Lee el sensor IR (GP16, entrada con pull-up; nivel bajo = objeto detectado):
   - **Objeto detectado**: enciende el LED indicador (GP15) y el servo (GP13) pasa a 160° (compuerta cerrada).
   - **Camino libre**: el servo vuelve a 20° (abierta).
3. **Cuenta** piezas por línea solo cuando no hay obstáculo (bloqueo de conteo).
4. Muestra el estado en consola con colores ANSI (línea activa, contadores, valor del potenciómetro).
5. Cada 5 s publica por MQTT el valor del potenciómetro y el estado del sensor IR.
## Comunicación MQTT
 
- Librería: `adafruit_minimqtt`, conexión WiFi con `wifi` / `socketpool`.
- Al conectar publica en el topic `descubrir` un JSON con el nombre del equipo y las magnitudes disponibles (`deteccion_objeto`, `voltaje`).
- Telemetría en `sensores/<equipo>/voltaje` y `sensores/<equipo>/deteccion_objeto`.
## Estructura del repositorio
 
| Archivo / carpeta | Descripción |
|---|---|
| `pruebaservosensor.py` | Programa completo: potenciómetro + IR + servo + LEDs + conteo + MQTT |
| `code.py` | Prueba mínima del servo (barrido 0° / 90° / 180° por PWM a 50 Hz) |
| `IR001` | Prueba aislada del sensor IR con LED externo |
| `VersionesAnteriores/` | Iteraciones previas (potenciómetro, sensor IR, servo) |
| `lib/` | Librerías de Adafruit (minimqtt, motor, connection manager, etc.) |
| `boot_out.txt` | Info de la placa: CircuitPython 9.2.8, Raspberry Pi Pico 2 W (RP2350) |
 
## Cómo probarlo
 
1. Instalar CircuitPython 9.x para Raspberry Pi Pico 2 W y copiar el contenido del repositorio al volumen `CIRCUITPY`.
2. Para usar el programa completo, copiar el contenido de `pruebaservosensor.py` como `code.py`.
3. Configurar la red y el broker (ver nota de seguridad abajo).
4. Conectar: potenciómetro a GP26, sensor IR a GP16, LEDs a GP15/17/18/19 y servo a GP13.
5. Abrir la consola serie para ver contadores y estados.
## Nota sobre credenciales
 
No guardes la contraseña de WiFi en el código. En CircuitPython podés usar el archivo `settings.toml` (`CIRCUITPY_WIFI_SSID`, `CIRCUITPY_WIFI_PASSWORD`) y leerlo con `os.getenv()`.
 
## Autor
 
**Ulises Ayala** – Estudiante de Ingeniería en Sistemas de Información, UTN FRRe (Resistencia, Chaco).
 
