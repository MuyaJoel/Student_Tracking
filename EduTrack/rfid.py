import os
import django
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "student_tracking.settings")
django.setup()

from stu_details.models import Student, Movement  

def update_database(rfid_tag):
    """ Save RFID data using Django ORM """
    try:
        student = Student.objects.filter(rfid_tag=rfid_tag).first()

        if student:
            movement = Movement.objects.filter(student=student, check_out_time__isnull=True).first()

            if movement:
                movement.check_out_time = datetime.now()
                movement.save()
                print(f"Student {student.name} (ID: {student.id}) checked out.")
            else:
                Movement.objects.create(student=student, location="School Gate", check_in_time=datetime.now())
                print(f"Student {student.name} (ID: {student.id}) checked in.")

        else:
            print("RFID tag not assigned to any student.")

    except Exception as e:
        print("Database Error:", e)

def read_rfid():
    """ Read RFID tag and update Django database """
    reader = SimpleMFRC522()
    try:
        print("Scan your RFID tag...")
        rfid_id, text = reader.read()
        print(f"RFID Tag Read: {rfid_id}")

        update_database(str(rfid_id))

    except KeyboardInterrupt:
        print("RFID reading stopped.")

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    read_rfid()
