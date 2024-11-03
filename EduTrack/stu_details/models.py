from django.db import models

# Create your models here.

class Student(models.Model):
    student_Id=models.CharField(max_length=20,unique=True)
    Name=models.CharField(max_length=100)
    rfid_Tag=models.CharField(max_length=100,unique=True)
    parent_Email=models.EmailField()


class Movement(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    check_In=models.DateTimeField(auto_now_add=True)
    check_Out=models.DateTimeField(null=True,blank=True)
    location=models.CharField(max_length=255)