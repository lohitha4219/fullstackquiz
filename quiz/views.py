from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Result
import random
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime
from django.conf import settings
from datetime import date
from django.template.loader import get_template
from django.template.loader import render_to_string
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.pagesizes import landscape, A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.units import inch

# DOMAIN PAGE
@login_required
def quiz_home(request):
    return render(request, "domains.html")


# LEVEL PAGE
@login_required
def choose_level(request, domain):
    return render(request, "choose_level.html", {"domain": domain})


# START QUIZ
@login_required
def start_quiz(request, domain, level):

    # 🔥 START ONLY ONCE
    if not request.session.get("quiz_started", False):

        questions = list(Question.objects.filter(domain=domain, level=level))

        if not questions:
            return render(request, "quiz_result.html", {"error": "No questions found"})

        random.shuffle(questions)

        request.session["quiz_questions"] = [q.id for q in questions[:200]]
        request.session["current_index"] = 0
        request.session["score"] = 0
        request.session["domain"] = domain
        request.session["level"] = level
        request.session["completed"] = False
        request.session["saved"] = False

        request.session["quiz_started"] = True   # 🔥 IMPORTANT

    index = request.session.get("current_index", 0)
    question_ids = request.session.get("quiz_questions", [])

    # RESULT SHOW
    show_result = request.session.pop("show_result", False)
    selected = request.session.pop("last_selected", None)
    correct = request.session.pop("last_correct", None)

    if show_result:
        request.session["current_index"] = index + 1

    index = request.session.get("current_index", 0)

    if index >= len(question_ids):
        request.session["completed"] = True
        request.session["quiz_started"] = False   # reset for next time
        return redirect("quiz_result")

    question = Question.objects.get(id=question_ids[index])

    return render(request, "quiz_play.html", {
        "question": question,
        "question_number": index + 1,
        "total_questions": len(question_ids),
        "domain": request.session.get("domain"),
        "level": request.session.get("level"),
        "show_result": show_result,
        "selected": selected,
        "correct": correct,
    })

# SUBMIT ANSWER
@login_required
def submit_answer(request):

    if request.method == "POST":

        selected = request.POST.get("option")
        question_id = int(request.POST.get("question_id"))

        question = Question.objects.get(id=question_id)
        correct = int(question.correct_answer)

        score = request.session.get("score", 0)

        if selected is not None and int(selected) == correct:
            score += 1

        request.session["score"] = score

        # ❌ REMOVE INDEX UPDATE HERE

        request.session["last_selected"] = int(selected) if selected else None
        request.session["last_correct"] = correct
        request.session["show_result"] = True

        return redirect("start_quiz",
                        domain=request.session.get("domain"),
                        level=request.session.get("level"))# QUIT QUIZ
@login_required
def quit_quiz(request):

    request.session["quiz_started"] = False   # 🔥 RESET
    request.session["completed"] = False

    return redirect("quiz_result")

# RESULT PAGE
@login_required
def quiz_result(request):

    score = request.session.get("score", 0)
    total = request.session.get("current_index", 0)
    domain = request.session.get("domain", "N/A")
    level = request.session.get("level", "N/A")
    completed = request.session.get("completed", False)

    # ✅ SAVE ONLY ONCE
    if not request.session.get("saved", False) and total > 0:

        Result.objects.create(
            user=request.user,
            domain=domain,
            level=level,
            score=score,
            total=total
        )

        request.session["saved"] = True

    return render(request, "quiz_result.html", {
        "score": score,
        "total": total,
        "domain": domain,
        "level": level,
        "completed":completed
    })


# DOWNLOAD RESULT PDF
@login_required
def download_result(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="quiz_result.pdf"'

    doc = SimpleDocTemplate(response)
    styles = getSampleStyleSheet()
    elements = []

    elements.append(Paragraph("Quiz Result", styles["Title"]))
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"User: {request.user.username}", styles["Normal"]))
    elements.append(Paragraph(f"Domain: {request.session.get('domain','N/A')}", styles["Normal"]))
    elements.append(Paragraph(f"Level: {request.session.get('level','N/A')}", styles["Normal"]))
    elements.append(Spacer(1, 10))
    elements.append(Paragraph(
        f"Score: {request.session.get('score',0)} / {request.session.get('current_index',0)}",
        styles["Normal"]
    ))

    doc.build(elements)
    return response


# DOWNLOAD CERTIFICATE

@login_required
def download_certificate(request):

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="certificate.pdf"'

    c = canvas.Canvas(response, pagesize=landscape(A4))
    width, height = landscape(A4)

    # 🔥 BACKGROUND
    c.setFillColorRGB(0.08, 0.08, 0.1)
    c.rect(0, 0, width, height, fill=1)

    # 🔥 GOLD BORDER
    c.setStrokeColor(colors.gold)
    c.setLineWidth(8)
    c.rect(20, 20, width-40, height-40)

    # INNER BORDER
    c.setLineWidth(2)
    c.rect(40, 40, width-80, height-80)

    # TITLE
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(width/2, height-120, f"{request.session.get('domain','PYTHON')} QUIZ")

    # LEVEL
    c.setFont("Helvetica", 20)
    c.drawCentredString(width/2, height-160, f"{request.session.get('level','MEDIUM')} Level")

    # TEXT
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height-220, "This certifies that")

    # NAME (GOLD)
    c.setFillColor(colors.gold)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(width/2, height-280, request.user.username)

    # BACK TO WHITE
    c.setFillColor(colors.white)
    c.setFont("Helvetica", 16)
    c.drawCentredString(width/2, height-330, "has successfully completed")

    # COURSE
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(width/2, height-370,
        f"{request.session.get('domain','Python')} Quiz Completed"
    )

    # DATE
    c.setFont("Helvetica", 14)
    c.drawCentredString(width/2, 100, f"Date: {date.today().strftime('%d-%m-%Y')}")

    c.save()
    return response    

@login_required
def view_certificate(request):
    return download_certificate(request)


from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
import random
from django.core.mail import send_mail

ALLOWED_ADMINS = [
    {"email": "ramyaramya6704s@gmail.com", "password": "Sharavana@2007"},
    {"email": "lohitha4219@gmail.com", "password": "Himanthlohitha14"},
]

def login_view(request):
    if request.method == "POST":

        action = request.POST.get("action")
        username = request.POST.get("username")   # 🔥 NEW
        email = request.POST.get("email")
        password = request.POST.get("password")

        print("ACTION:", action)

        # ================= USER LOGIN =================
        if action == "login":
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('/quiz/home/')
            else:
                messages.error(request, "Invalid User Login")

        # ================= REGISTER =================
        elif action == "register":

            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
            else:
                User.objects.create_user(
                    username=username,   # 🔥 username saved
                    email=email,
                    password=password
                )
                messages.success(request, "Registered Successfully")

        # ================= ADMIN LOGIN =================
        elif action == "admin_login":
            for admin in ALLOWED_ADMINS:
                if admin["email"] == email and admin["password"] == password:
                    request.session["admin"] = email
                    return redirect("/quiz/admin-dashboard/")

            messages.error(request, "Invalid Admin Login")

        # ================= SEND OTP =================
        elif action == "send_otp":
            allowed = [a["email"] for a in ALLOWED_ADMINS]

            if email not in allowed:
                messages.error(request, "Not allowed admin")
            else:
                otp = random.randint(1000, 9999)
                request.session["otp"] = otp
                request.session["email"] = email

                send_mail(
                    "Admin OTP",
                    f"Your OTP is {otp}",
                    "yourgmail@gmail.com",
                    [email],
                    fail_silently=False,
                )

                messages.success(request, "OTP sent")

        # ================= VERIFY OTP =================
        elif action == "admin_otp":
            user_otp = request.POST.get("otp")

            if str(request.session.get("otp")) == str(user_otp):
                request.session["admin"] = request.session.get("email")
                return redirect("/quiz/admin-dashboard/")
            else:
                messages.error(request, "Invalid OTP")

    return render(request, "login_register.html")


from django.contrib.auth.models import User
from django.contrib import messages

# 🔥 ADMIN DASHBOARD (UPGRADED)
def admin_dashboard(request):
    if 'admin' not in request.session:
        return redirect('login')

    from django.contrib.auth.models import User

    students = User.objects.all()
    questions = Question.objects.all()

    # 🔥 GROUP QUESTIONS BY DOMAIN
    domain_questions = {}
    for q in questions:
        domain_questions.setdefault(q.domain, []).append(q)

    return render(request, 'admin_dashboard.html', {
        'students': students,
        'domain_questions': domain_questions,
        'total_users': students.count(),
        'total_questions': questions.count(),
    })


# ❌ DELETE USER
def delete_user(request, id):
    if 'admin' not in request.session:
        return redirect('login')

    User.objects.filter(id=id).delete()
    return redirect('/quiz/admin-dashboard/')


# ➕ ADD QUESTION
def add_question(request):
    if 'admin' not in request.session:
        return redirect('login')

    if request.method == "POST":
        Question.objects.create(
            question=request.POST.get("question"),
            option1=request.POST.get("option1"),
            option2=request.POST.get("option2"),
            option3=request.POST.get("option3"),
            option4=request.POST.get("option4"),
            correct_answer=request.POST.get("correct"),
            domain=request.POST.get("domain"),
            level=request.POST.get("level"),
        )
        messages.success(request, "Question Added")

    return redirect('/quiz/admin-dashboard/')


# ❌ DELETE QUESTION
def delete_question(request, id):
    if 'admin' not in request.session:
        return redirect('login')

    Question.objects.filter(id=id).delete()
    return redirect('/quiz/admin-dashboard/')