from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from IMS_app.models import CustomUser,Staffs,Courses,Subjects,Students, SessionYearModel, FeedBackStudent, FeedBackStaffs, Attendance, AttendanceReport, StudentRecipt
from IMS_app.forms import AddStudentForm, EditStudentForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
# from .utils import render_to_pdf
# from django.template.loader import get_template
# import datetime
# from django.views.generic import View

def admin_home(request):
    student_count1=Students.objects.all().count()
    staff_count=Staffs.objects.all().count()
    subject_count=Subjects.objects.all().count()
    course_count=Courses.objects.all().count()

    course_all=Courses.objects.all()
    course_name_list=[]
    subject_count_list=[]
    student_count_list_in_course=[]
    for course in course_all:
        subjects=Subjects.objects.filter(course_id=course.id).count()
        students=Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all=Subjects.objects.all()
    subject_list=[]
    student_count_list_in_subject=[]
    for subject in subjects_all:
        course=Courses.objects.get(id=subject.course_id.id)
        student_count=Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)


    return render(request,'hod_templates/home_content.html',{"student_count":student_count1,"staff_count":staff_count,"subject_count":subject_count,"course_count":course_count,'course_name_list':course_name_list,'subject_count_list':subject_count_list,'student_count_list_in_course':student_count_list_in_course,'subject_list':subject_list,'student_count_list_in_subject':student_count_list_in_subject})

def add_staff(request):
    return render(request, 'hod_templates/add_staff_template.html')

def add_staff_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        try:
            #Creating customuser
            user = CustomUser.objects.create_user(username=username,password=password,email=email,last_name=last_name,first_name=first_name,user_type=2)
            user.staffs.address=address
            user.save()
            messages.success(request,"Successfully Added Staff")
            return HttpResponseRedirect(reverse("add_staff"))
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect(reverse("add_staff"))

def add_course(request):
    return render(request, 'hod_templates/add_course_template.html')

def add_course_save(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        course=request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect(reverse("add_course"))

        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect(reverse("add_course"))

def add_student(request):
    form = AddStudentForm()
    courses =Courses.objects.all()
    sessions = SessionYearModel.object.all()
    return render(request, 'hod_templates/add_student_template.html',{'form':form,'courses':courses,'sessions':sessions})

def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        form = AddStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            address = form.cleaned_data['address']
            date = form.cleaned_data['date']
            batch = form.cleaned_data['batch']
            contact = form.cleaned_data['contact']
            dob = form.cleaned_data['dob']

            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course']
            sex = form.cleaned_data['sex']
            coursefees =  request.POST.get('coursefees')
            amountpaid =  request.POST.get('amountpaid')
            date_ap =  request.POST.get('date_ap')
            balance =  request.POST.get('balance')
            cerificate_issue = form.cleaned_data['cerificate_issue']
            cerificate_issue_date = form.cleaned_data['cerificate_issue_date']


            profile_pic=request.FILES['profile_pic']
            fs = FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            
            try:
                #Creating customuser
                user = CustomUser.objects.create_user(username=username,password=password,email=email,first_name=first_name,last_name=last_name,user_type=3)
                user.students.address=address
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                session_duration = SessionYearModel.object.get(id=session_year_id)
                user.students.session_year_id=session_duration
                user.students.profile_pic=profile_pic_url
                user.students.gender=sex
                user.students.batch=batch
                user.students.date=date
                user.students.contact=contact
                user.students.dob=dob
                user.students.coursefees=coursefees
                user.students.amountpaid=amountpaid
                user.students.date_ap=date_ap
                user.students.balance=balance
                user.students.cerificate_issue=cerificate_issue
                user.students.cerificate_issue_date=cerificate_issue_date
                user.save()
                messages.success(request,"Successfully Added Student")
                return HttpResponseRedirect(reverse("add_student"))
            except Exception as e:
                messages.error(request,"Failed to Add Student")
                return HttpResponseRedirect(reverse("add_student"))
        else:
            form = AddStudentForm(request.POST)
            return render(request, 'hod_templates/add_student_template.html',{'form':form})

def add_subject(request):
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_templates/add_subject_template.html',{"staffs": staffs,"courses": courses})

def add_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_name=request.POST.get("subject_name")
        course_id=request.POST.get("course")
        course=Courses.objects.get(id=course_id)
        staff_id=request.POST.get("staff")
        staff=CustomUser.objects.get(id=staff_id)

        try:
            subject=Subjects(subject_name=subject_name,course_id=course,staff_id=staff)
            subject.save()
            messages.success(request,"Successfully Added Subject")
            return HttpResponseRedirect(reverse("add_subject"))
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect(reverse("add_subject"))

def manage_staff(request):
    staffs = Staffs.objects.all()
    return render(request, 'hod_templates/manage_staff_template.html',{'staffs':staffs})

def manage_student(request):
    students = Students.objects.all()
    return render(request, 'hod_templates/manage_student_template.html',{'students':students})

def manage_course(request):
    courses = Courses.objects.all()
    return render(request, 'hod_templates/manage_course_template.html',{'courses':courses})


def manage_subject(request):
    subjects = Subjects.objects.all()
    return render(request, 'hod_templates/manage_subject_template.html',{'subjects':subjects})

def edit_staff(request,staff_id):
    staff =Staffs.objects.get(admin=staff_id)
    return render(request, 'hod_templates/edit_staff_template.html',{'staff':staff,"id":staff_id})

def edit_staff_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        staff_id=request.POST.get("staff_id")
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        email=request.POST.get("email")
        username=request.POST.get("username")
        address=request.POST.get("address")

        try:
            user=CustomUser.objects.get(id=staff_id)
            user.first_name=first_name
            user.last_name=last_name
            user.email=email
            user.username=username
            user.save()

            staff_model=Staffs.objects.get(admin=staff_id)
            staff_model.address=address
            staff_model.save()
            messages.success(request,"Successfully Edited Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect(reverse("edit_staff",kwargs={"staff_id":staff_id}))

def edit_student(request,student_id):
    request.session['student_id'] = student_id
    student =Students.objects.get(admin=student_id)
    form = EditStudentForm()
    form.fields['date'].initial=student.date
    form.fields['first_name'].initial=student.admin.first_name
    form.fields['last_name'].initial=student.admin.last_name
    form.fields['username'].initial=student.admin.username
    form.fields['email'].initial=student.admin.email
    form.fields['address'].initial=student.address
    form.fields['batch'].initial=student.batch
    form.fields['sex'].initial=student.gender
    form.fields['contact'].initial=student.contact
    form.fields['dob'].initial=student.dob
    form.fields['session_year_id'].initial=student.session_year_id
    form.fields['course'].initial=student.course_id.id
    form.fields['coursefees'].initial=student.coursefees
    form.fields['amountpaid'].initial=student.amountpaid
    form.fields['date_ap'].initial=student.date_ap
    form.fields['balance'].initial=student.balance
    form.fields['cerificate_issue'].initial=student.cerificate_issue
    form.fields['cerificate_issue_date'].initial=student.cerificate_issue_date
    return render(request, 'hod_templates/edit_student_template.html',{"form":form,"id":student_id,"username":student.admin.username})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.session.get('student_id')
        if student_id == None:
            return HttpResponseRedirect(reverse("manage_student"))

        form = EditStudentForm(request.POST,request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            address = form.cleaned_data['address']
            date = form.cleaned_data['date']
            batch = form.cleaned_data['batch']
            contact = form.cleaned_data['contact']
            dob = form.cleaned_data['dob']

            session_year_id = form.cleaned_data['session_year_id']
            course_id = form.cleaned_data['course']
            sex = form.cleaned_data['sex']
            coursefees = form.cleaned_data['coursefees']
            amountpaid = form.cleaned_data['amountpaid']
            date_ap = form.cleaned_data['date_ap']
            balance = form.cleaned_data['balance']
            cerificate_issue = form.cleaned_data['cerificate_issue']
            cerificate_issue_date = form.cleaned_data['cerificate_issue_date']


            if request.FILES.get('profile_pic',False):
                profile_pic=request.FILES['profile_pic']
                fs = FileSystemStorage()
                filename=fs.save(profile_pic.name,profile_pic)
                profile_pic_url=fs.url(filename)
            else:
                profile_pic_url =None

            try:
                user=CustomUser.objects.get(id=student_id)
                user.first_name=first_name
                user.last_name=last_name
                user.email=email
                user.username=username
                user.save()

                student = Students.objects.get(admin=student_id)
                student.address=address
                session_duration = SessionYearModel.object.get(id=session_year_id)
                student.session_year_id=session_duration
               
                course_obj=Courses.objects.get(id=course_id)
                user.students.course_id=course_obj
                
                if profile_pic_url !=None:
                    student.profile_pic= profile_pic_url
                student.gender=sex
                student.batch=batch
                student.date=date
                student.contact=contact
                student.dob=dob
                student.coursefees=coursefees
                student.amountpaid=amountpaid
                student.date_ap=date_ap
                student.balance=balance
                student.cerificate_issue=cerificate_issue
                student.cerificate_issue_date=cerificate_issue_date
                student.save()

                del request.session['student_id']
                messages.success(request,"Successfully Edited Student")
                return HttpResponseRedirect(reverse("edit_student",kwargs={"student_id":student_id}))
            except Exception as e:
                messages.error(request,"Failed to Edit Student")
                return HttpResponseRedirect(reverse("edit_student", kwargs={"student_id":student_id}))
        else:
            form=EditStudentForm(request.POST)
            student=Students.objects.get(admin=student_id)
            return render(request,"hod_template/edit_student_template.html",{"form":form,"id":student_id,"username":student.admin.username})

def edit_subject(request ,subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_templates/edit_subject_template.html',{'subject':subject , 'courses':courses, 'staffs':staffs,"id":subject_id})

def edit_subject_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        subject_id = request.POST.get('subject_id')
        subject_name = request.POST.get('subject_name')
        staff_id = request.POST.get('staff')
        course_id = request.POST.get('course')

        try:
            subject = Subjects.objects.get(id=subject_id)
            subject.subject_name = subject_name
            staff = CustomUser.objects.get(id=staff_id)
            subject.staff_id = staff
            course =Courses.objects.get(id=course_id)
            subject.course_id = course
            subject.save()

           
            messages.success(request,"Successfully Edited Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))

        except :
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect(reverse("edit_subject",kwargs={"subject_id":subject_id}))

def edit_course(request, course_id):
    course =Courses.objects.get(id=course_id)
    return render(request, 'hod_templates/edit_course_template.html',{'course':course,"id":course_id})

def edit_course_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        course_id = request.POST.get('course_id')
        course_name = request.POST.get('course')

        try:
            course = Courses.objects.get(id=course_id)
            course.course_name = course_name
            course.save()
            messages.success(request,"Successfully Edited Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id":course_id}))

        except:
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect(reverse("edit_course", kwargs={"course_id":course_id}))
        

def manage_session(request):
    return render(request, 'hod_templates/manage_session_template.html')

def add_session_duration_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("manage_session"))
    else:
        session_start=request.POST.get("session_start")
        session_end=request.POST.get("session_end")

        try:
            sessionduration=SessionYearModel(session_start_year=session_start,session_end_year=session_end)
            sessionduration.save()
            messages.success(request, "Successfully Added Session")
            return HttpResponseRedirect(reverse("manage_session"))
        except:
            messages.error(request, "Failed to Add Session")
            return HttpResponseRedirect(reverse("manage_session"))

@csrf_exempt
def check_email_exist(request):
    email = request.POST.get("email")
    user_obj =CustomUser.objects.filter(email=email).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

@csrf_exempt
def check_username_exist(request):
    username = request.POST.get("username")
    user_obj =CustomUser.objects.filter(username=username).exists()
    if user_obj:
        return HttpResponse(True)
    else:
        return HttpResponse(False)

def staff_feedback_message(request):
    feedbacks = FeedBackStaffs.objects.all()
    return render(request, 'hod_templates/staff_feedback_template.html',{'feedbacks':feedbacks})

def student_feedback_message(request):
    feedbacks = FeedBackStudent.objects.all()
    return render(request, 'hod_templates/student_feedback_template.html',{'feedbacks':feedbacks})

@csrf_exempt
def student_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStudent.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

@csrf_exempt
def staff_feedback_message_replied(request):
    feedback_id=request.POST.get("id")
    feedback_message=request.POST.get("message")

    try:
        feedback=FeedBackStaffs.objects.get(id=feedback_id)
        feedback.feedback_reply=feedback_message
        feedback.save()
        return HttpResponse("True")
    except:
        return HttpResponse("False")

def admin_view_attendance(request):
    subjects=Subjects.objects.all()
    session_year_id=SessionYearModel.object.all()
    return render(request, 'hod_templates/admin_view_attendance_template.html',{"subjects":subjects,"session_year_id":session_year_id})

@csrf_exempt
def admin_get_attendance_dates(request):
    subject=request.POST.get("subject")
    session_year_id=request.POST.get("session_year_id")
    subject_obj=Subjects.objects.get(id=subject)
    session_year_obj=SessionYearModel.object.get(id=session_year_id)
    attendance=Attendance.objects.filter(subject_id=subject_obj,session_year_id=session_year_obj)

    attendance_obj=[]

    for attendance_single in attendance:
        data={"id":attendance_single.id,"attendance_date":str(attendance_single.attendance_date),"session_year_id":attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj),safe=False)

@csrf_exempt
def admin_get_attendance_student(request):
    attendance_date=request.POST.get("attendance_date")
    attendance=Attendance.objects.get(id=attendance_date)

    attendance_data=AttendanceReport.objects.filter(attendance_id=attendance)
    list_data=[]

    for student in attendance_data:
        data_small={"id":student.student_id.admin.id,"name":student.student_id.admin.first_name+" "+student.student_id.admin.last_name,"status":student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data),content_type="application/json",safe=False)

def admin_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request,'hod_templates/admin_profile.html',{"user":user})

def admin_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("admin_profile"))
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name

            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))

def add_student_recipt(request):
    courses =Courses.objects.all()
    return render(request, 'hod_templates/add_student_recipt_template.html',{"courses":courses})

def add_student_recipt_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        date = request.POST.get('date')
        stud_name = request.POST.get('stud_name')
        course = request.POST.get('course')
        coursefees = request.POST.get('coursefees')
        amountpaid = request.POST.get('amountpaid')
        paidby = request.POST.get('paidby')
        balance = request.POST.get('balance')
        try:
            recipt = StudentRecipt(student_name=stud_name,date=date,course=course,coursefees=coursefees,amountpaid=amountpaid,paidby=paidby,balance=balance)
            recipt.save()
            messages.success(request,"Successfully Added Recipt")
            return HttpResponseRedirect(reverse("add_student_recipt"))
        except:
            messages.error(request,"Failed to Add Recipt")
            return HttpResponseRedirect(reverse("add_student_recipt"))

def manage_student_recipt(request):
    recipts = StudentRecipt.objects.all()
   
    return render(request, 'hod_templates/manage_student_recipt_template.html',{"recipts":recipts})

# def edit_student_recipt(request, recipt_id):
#     recipt_ids = StudentRecipt.objects.get(id=recipt_id)
#     return render(request, 'hod_templates/recipt.html',{"recipt_ids":recipt_ids,"id":recipt_id})


# class GeneratePdf(View):
#     def get(self, request, *args, **kwargs):
#         recipt_id = request.POST.get('recipt_id')
#         print(recipt_id)
#         template = get_template('recipt.html')
#         context = {
#             "invoice_id": recipt_id,
#             "customer_name": "John Cooper",
#             "amount": 1399.99,
#             "today": "Today",
#         }
#         html = template.render(context)
#         pdf = render_to_pdf('recipt.html', context)
#         if pdf:
#             response = HttpResponse(pdf, content_type='application/pdf')
#             filename = "Invoice_%s.pdf" %("12341231")
#             content = "inline; filename='%s'" %(filename)
#             download = request.GET.get("download")
#             if download:
#                 content = "attachment; filename='%s'" %(filename)
#             response['Content-Disposition'] = content
#             return response
#         return HttpResponse("Not found")




