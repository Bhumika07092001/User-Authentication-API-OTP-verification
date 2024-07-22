from django.urls import path
from .views import register, request_otp, verify_otp,RegisterView, RequestOTPView, VerifyOTPView

urlpatterns = [
    path('register/', register, name='register'),
    path('request-otp/', request_otp, name='request_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/request-otp/', RequestOTPView.as_view(), name='api_request_otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='api_verify_otp'),
]
