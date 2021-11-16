from django.shortcuts import render

def student_home(request):
    return render(request,"student_templates/student_home_template.html")