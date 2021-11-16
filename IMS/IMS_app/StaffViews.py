from django.shortcuts import render

def staff_home(request):
    return render(request,"staff_templates/staff_home_template.html")