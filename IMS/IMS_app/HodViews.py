from django.shortcuts import render

def admin_home(request):
    return render(request,'hod_templates/home_content.html')