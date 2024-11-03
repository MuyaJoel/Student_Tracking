
from django.contrib import admin
from django.urls import path, include
import stu_details.urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(stu_details.urls)),
]
