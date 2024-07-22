import random

def send_otp(email, otp):
    print(f"Sending OTP {otp} to email {email}")

def generate_otp():
    return ''.join(random.choices('0123456789', k=6))
