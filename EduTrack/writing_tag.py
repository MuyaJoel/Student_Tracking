import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
    student_id = input("Enter student ID to write to RFID tag: ")
    print("Place your RFID tag near the reader...")

    reader.write(student_id)
    print(f"Successfully written: {student_id}")

finally:
    GPIO.cleanup()
    print("cleanup done")
