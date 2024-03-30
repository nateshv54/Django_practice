# your_project/urls.py

from django.contrib import admin
from django.urls import path
from django.urls import include  # Import include

from Registration import views  # Import your views from your_app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('details/', views.details_view, name='details'),
    path('', views.login_view, name='login'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    path('resend_otp/', views.resend_otp_view, name='resend_otp'),
    path('loginS/',views.login_success,name='loginS')
]
