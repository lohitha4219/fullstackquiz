from django.shortcuts import render, redirect
from django.core.mail import send_mail
import random

# ✅ ONLY 2 ADMINS
ALLOWED_ADMINS = [
    {"email": "admin1@gmail.com", "password": "1234"},
    {"email": "admin2@gmail.com", "password": "5678"},
]

# 🔐 LOGIN
from django.contrib import messages

def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        # 🔐 Check Admin First
        for admin in ALLOWED_ADMINS:
            if admin['email'] == email and admin['password'] == password:
                request.session['admin'] = email
                return redirect('admin_dashboard')

        # 👤 Check User
        from accounts.models import Student  # your model
        try:
            user = Student.objects.get(email=email, password=password)
            request.session['user'] = user.email
            return redirect('user_dashboard')
        except:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')

# 📊 DASHBOARD

def admin_dashboard(request):
    if 'admin' not in request.session:
        return redirect('login')
    

def user_dashboard(request):
    if 'user' not in request.session:
        return redirect('login')

# 🚪 LOGOUT
def admin_logout(request):
    request.session.flush()
    return redirect('admin_login')


# 📧 SEND OTP
def send_otp(request):
    if request.method == "POST":
        email = request.POST['email']

        allowed_emails = [admin['email'] for admin in ALLOWED_ADMINS]

        if email not in allowed_emails:
            return render(request, 'send_otp.html', {'error': 'Not authorized'})

        otp = random.randint(1000, 9999)

        request.session['otp'] = otp
        request.session['email'] = email

        send_mail(
            'Admin OTP',
            f'Your OTP is {otp}',
            'yourgmail@gmail.com',
            [email],
            fail_silently=False,
        )

        return redirect('verify_otp')

    return render(request, 'send_otp.html')


# 🔢 VERIFY OTP
def verify_otp(request):
    if request.method == "POST":
        user_otp = request.POST['otp']

        if int(user_otp) == request.session.get('otp'):
            request.session['admin'] = request.session.get('email')
            return redirect('admin_dashboard')
        else:
            return render(request, 'verify_otp.html', {'error': 'Invalid OTP'})

    return render(request, 'verify_otp.html')