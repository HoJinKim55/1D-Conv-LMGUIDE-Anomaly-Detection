import serial
import time

ser = serial.Serial('COM3', 921600, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    time.sleep(0.1)