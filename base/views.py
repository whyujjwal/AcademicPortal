from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404


def Home(response):
    return render(response,"base/base.html")

def Dashboard(response):
    return render(response,"base/student_dashboard.html")