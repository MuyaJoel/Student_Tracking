import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader=SimpleMFRC522()

try:
    print("Scan your RFID Tag ...")
    id, text=reader.read()
    print(f"RFId Tag UID: {id}")
finally:
    GPIO.cleanup()
    print("cleanup done")