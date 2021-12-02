import datetime

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from IMS_app.models import FeedBackStudent, Subjects, Students, Courses, CustomUser, Attendance, AttendanceReport, StudentResult

def student_home(request):
    student_obj = Students.objects.get(admin = request.user.id)
    attendance_total = AttendanceReport.objects.filter(student_id = student_obj).count()
    attendance_present= AttendanceReport.objects.filter(student_id = student_obj,status =True).count()
    attendance_absent= AttendanceReport.objects.filter(student_id = student_obj,status =False).count()

    course = Courses.objects.get(id=student_obj.course_id.id)
    subjects= Subjects.objects.filter(course_id=course).count()

    subject_name=[]
    data_present=[]
    data_absent=[]
    subject_data=Subjects.objects.filter(course_id=student_obj.course_id)
    for subject in subject_data:
        attendance=Attendance.objects.filter(subject_id=subject.id)
        attendance_present_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=True,student_id=student_obj.id).count()
        attendance_absent_count=AttendanceReport.objects.filter(attendance_id__in=attendance,status=False,student_id=student_obj.id).count()
        subject_name.append(subject.subject_name)
        data_present.append(attendance_present_count)
        data_absent.append(attendance_absent_count)
    return render(request,"student_templates/student_home_template.html",{'attendance_total':attendance_total,'attendance_present':attendance_present,'attendance_absent':attendance_absent,'subjects':subjects,"data_name":subject_name,"data1":data_present,"data2":data_absent})

def student_view_attendance(request):
    student = Students.objects.get(admin=request.user.id)
    courses = student.course_id
    subjects = Subjects.objects.filter(course_id=courses)
    return render(request,"student_templates/student_view_attendance_template.html",{'subjects': subjects})

def student_view_attendance_post(request):
    subject_id=request.POST.get("subject")
    start_date=request.POST.get("start_date")
    end_date=request.POST.get("end_date")

    start_data_parse = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
    end_data_parse = datetime.datetime.strptime(end_date, "%Y-%m-%d").date()

    subject_obj=Subjects.objects.get(id=subject_id)
    user_object=CustomUser.objects.get(id=request.user.id)
    stud_obj=Students.objects.get(admin=user_object)

    attendance=Attendance.objects.filter(attendance_date__range=(start_data_parse,end_data_parse),subject_id=subject_obj)
    attendance_reports=AttendanceReport.objects.filter(attendance_id__in=attendance,student_id=stud_obj)

    return render(request,"student_templates/student_attendance_data.html",{"attendance_reports":attendance_reports})


def student_feedback(request):
    student_id=Students.objects.get(admin=request.user.id)
    feedback_data=FeedBackStudent.objects.filter(student_id=student_id)
    return render(request,"student_templates/student_feedback_template.html",{"feedback_data":feedback_data})

def student_feedback_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("student_feedback"))
    else:
        feedback_msg=request.POST.get("feedback_msg")

        student_obj=Students.objects.get(admin=request.user.id)
        try:
            feedback=FeedBackStudent(student_id=student_obj,feedback=feedback_msg,feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("student_feedback"))


def student_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    student = Students.objects.get(admin=user)
    return render(request,'student_templates/student_profile.html',{"user":user,"student":student})

def student_profile_save(request):
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    address = request.POST.get('address')
    password = request.POST.get('password')
    try:
        customuser = CustomUser.objects.get(id=request.user.id)
        customuser.first_name = first_name
        customuser.last_name = last_name

        if password!=None and password!="":
            customuser.set_password(password)
        customuser.save()

        student = Students.objects.get(admin = customuser.id)
        student.address = address
        student.save()

        messages.success(request, "Successfully Updated Profile")
        return HttpResponseRedirect(reverse("student_profile"))
    except:
        messages.error(request, "Failed to Update Profile")
        return HttpResponseRedirect(reverse("student_profile"))


def student_view_result(request):
    student=Students.objects.get(admin=request.user.id)
    studentresult=StudentResult.objects.filter(student_id=student.id)
    return render(request, "student_templates/student_view_result.html",{"studentresult":studentresult})