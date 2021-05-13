"""CySm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name = "index"),
    path('school', views.school_reg, name = "school-reg"),
    path('teacher', views.teacher_reg, name = "teacher-reg"),
    path('enquiry', views.enquiry_form, name = "enquiry"),
    path('school-profile-status', views.school_profile_status, name = "school-profile-status"),
    path('thankyou/', views.thankyou_enquiry, name = "thankyou_enquiry"),
    path('register-user/', views.register, name="register-user"),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
]
