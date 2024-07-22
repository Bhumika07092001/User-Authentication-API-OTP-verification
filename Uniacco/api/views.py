from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, OTP
from .email_service import send_otp, generate_otp
import jwt



from django.shortcuts import render

def register(request):
    return render(request, 'register.html')

def request_otp(request):
    return render(request, 'request_otp.html')

def verify_otp(request):
    return render(request, 'verify_otp.html')


class RegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({"message": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({"message": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(email=email)
        return Response({"message": "Registration successful. Please verify your email."}, status=status.HTTP_201_CREATED)

class RequestOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"message": "Email not registered."}, status=status.HTTP_404_NOT_FOUND)
        otp = generate_otp()
        OTP.objects.create(user=user, code=otp)
        send_otp(email, otp)
        return Response({"message": "OTP sent to your email."}, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp_code = request.data.get('otp')
        try:
            user = User.objects.get(email=email)
            otp = OTP.objects.filter(user=user, code=otp_code, is_used=False).latest('created_at')
            if otp.is_valid():
                otp.is_used = True
                otp.save()
                token = jwt.encode({'email': user.email}, 'secret', algorithm='HS256')
                print(token)
                return Response({"message": "Login successful.", "token": token}, status=status.HTTP_200_OK)
            else:
                return Response({"message": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        except (User.DoesNotExist, OTP.DoesNotExist):
            return Response({"message": "Invalid email or OTP."}, status=status.HTTP_400_BAD_REQUEST)

