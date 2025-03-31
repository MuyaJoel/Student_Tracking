from django.urls import path
from . import views

urlpatterns=[
    path('', views.students_dashboard, name='students_dashboard'),
    path('checkin/<int:student_id>/', views.check_in, name='check_in'),
    path('checkout/<int:student_id>/', views.check_out, name='check_out'),
]
