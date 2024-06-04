import serial
import time
from enum import Enum
from utils import check_internet_connection

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1.0)
time.sleep(3)
ser.reset_input_buffer()

print("Serial OK")

arduinoReady = False

class Condition(Enum):
    OK = 3,
    NO_INTERNET = 2,
    BAD = 1


while not arduinoReady:
    if ser.in_waiting > 0:
        line=ser.readline().decode('utf-8').rstrip()
        print(line)
        if line == 'ready':
            arduinoReady = True

try: 
    while True:
            condition = Condition.OK
            print("Send current condition to Arduino")
            if check_internet_connection():
                condition = Condition.NO_INTERNET
                print("no internet")
            else:
                print("ok")
            ser.write(condition.value)
            time.sleep(5)

except KeyboardInterrupt:
    print("Close serial communication")
    ser.write(-1) # bye to arduino
    ser.close()
