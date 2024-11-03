from django.shortcuts import render
from .models import Student, Movement

# Create your views here.
def students_dashboard(request):
    students=Student.objects.all()

    return render(request, 'stu_details/index.html', {'students':students})