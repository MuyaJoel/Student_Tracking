import os
import django
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from datetime import datetime

# Set up Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "EduTrack.settings")
django.setup()

# Import Django models and email modules
from stu_details.models import Student, Movement
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.timezone import now


def send_notification_email(student, action):
    subject = f"Student {student.Name} has {action}"
    
    message = render_to_string('stu_details/email_template.html', {
        'student': student,
        'action': action,
        'now': now(),
    })

    # Assumes Student model has a parent_email field
    recipient = student.parent_Email
    if recipient:
        email = EmailMessage(subject, message, to=[recipient])
        email.content_subtype = "html"
        email.send()
        print(f"📧 Email sent to {recipient}")
    else:
        print("No parent email found for this student.")


def update_database(rfid_tag):
    """Save RFID data using Django ORM"""
    try:
        print("Checking if the RFID tag is assigned to a student...")
        student = Student.objects.filter(rfid_Tag=rfid_tag).first()

        if student:
            print(f"Found student: {student.Name} (ID: {student.student_Id})")

            movement = Movement.objects.filter(student=student, check_out_time__isnull=True).first()

            if movement:
                movement.check_out_time = datetime.now()
                movement.save()
                print(f"🔄 Student {student.Name} checked out at {movement.check_out_time}.")
                send_notification_email(student, "checked out")
            else:
                Movement.objects.create(student=student, location="School Gate", check_in_time=datetime.now())
                print(f"🟢 Student {student.Name} checked in at {datetime.now()}.")
                send_notification_email(student, "checked in")

        else:
            print("RFID tag not assigned to any student. Please register it.")

    except Exception as e:
        print("Database Error:", e)


def read_rfid():
    """Read RFID tag and update Django database"""
    reader = SimpleMFRC522()
    try:
        print("Waiting for RFID scan...")
        rfid_id, text = reader.read()
        print(f"RFID Tag Read: {rfid_id}")
        update_database(str(rfid_id))

    except KeyboardInterrupt:
        print("RFID reading stopped.")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    read_rfid()
