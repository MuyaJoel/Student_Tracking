from django.shortcuts import render
from .models import Student, Movement
from datetime import datetime
from django.http import JsonResponse

# Create your views here.
def students_dashboard(request):
    students=Student.objects.all()

    for student in students:
       student.is_checked_in = Movement.objects.filter(
           student=student, check_out_time__isnull=True
       ).exists()

    return render(request, 'stu_details/index.html', {'students':students})


def check_in(request, rfid_tag):
    student = Student.objects.filter(rfid_tag=rfid_tag).first()

    if student:
        existing_movement = Movement.objects.filter(student=student, check_out_time__isnull=True).first()

        if existing_movement:
            return JsonResponse({"message": f"Student {student.name} is already checked in."}, status=400)

    
        Movement.objects.create(student=student, location="School Gate", check_in_time=datetime.now())

        return JsonResponse({"message": f"Student {student.name} checked in successfully."}, status=200)

    return JsonResponse({"error": "RFID tag not recognized."}, status=404)


def check_out(request, rfid_tag):
    student = Student.objects.filter(rfid_tag=rfid_tag).first()

    if student:
        movement = Movement.objects.filter(student=student, check_out_time__isnull=True).first()

        if movement:
            movement.check_out_time = datetime.now()
            movement.save()
            return JsonResponse({"message": f"Student {student.name} checked out successfully."}, status=200)

        return JsonResponse({"message": f"Student {student.name} was not checked in."}, status=400)

    return JsonResponse({"error": "RFID tag not recognized."}, status=404)