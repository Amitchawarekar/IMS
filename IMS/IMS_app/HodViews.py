from django.http.response import HttpResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from IMS_app.models import CustomUser,Staffs,Courses,Subjects,Students

def admin_home(request):
    return render(request,'hod_templates/home_content.html')

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
            return HttpResponseRedirect("/add_staff")
        except:
            messages.error(request,"Failed to Add Staff")
            return HttpResponseRedirect("/add_staff")

def add_course(request):
    return render(request, 'hod_templates/add_course_template.html')

def add_course_save(request):
    if request.method != "POST":
        return HttpResponseRedirect("Method Not Allowed")
    else:
        course=request.POST.get('course')
        try:
            course_model = Courses(course_name=course)
            course_model.save()
            messages.success(request,"Successfully Added Course")
            return HttpResponseRedirect("/add_course")

        except:
            messages.error(request,"Failed To Add Course")
            return HttpResponseRedirect("/add_course")

def add_student(request):
    courses = Courses.objects.all()
    return render(request, 'hod_templates/add_student_template.html',{"courses": courses})

def add_student_save(request):
    if request.method != 'POST':
        return HttpResponse("Method not allowed")
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address = request.POST.get('address')
        date = request.POST.get('date')
        batch = request.POST.get('batch')
        contact = request.POST.get('contact')
        dob = request.POST.get('dob')

        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        course_id = request.POST.get('course')
        sex = request.POST.get('sex')

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
            user.students.session_start_year=session_start
            user.students.session_end_year=session_end
            user.students.profile_pic=profile_pic_url
            user.students.gender=sex
            user.students.batch=batch
            user.students.date=date
            user.students.contact=contact
            user.students.dob=dob
            user.save()
            messages.success(request,"Successfully Added Student")
            return HttpResponseRedirect("/add_student")
        except Exception as e:

            print(e)
            raise e
            messages.error(request,"Failed to Add Student")
            return HttpResponseRedirect("/add_student")

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
            return HttpResponseRedirect("/add_subject")
        except:
            messages.error(request,"Failed to Add Subject")
            return HttpResponseRedirect("/add_subject")

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
    return render(request, 'hod_templates/edit_staff_template.html',{'staff':staff})

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
            return HttpResponseRedirect("/edit_staff/"+ staff_id)
        except:
            messages.error(request,"Failed to Edit Staff")
            return HttpResponseRedirect("/edit_staff/"+ staff_id)

def edit_student(request,student_id):
    courses = Courses.objects.all()
    student =Students.objects.get(admin=student_id)
    return render(request, 'hod_templates/edit_student_template.html',{'student':student, "courses" :courses})

def edit_student_save(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        student_id=request.POST.get("student_id")
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        date = request.POST.get('date')
        batch = request.POST.get('batch')
        contact = request.POST.get('contact')
        dob = request.POST.get('dob')

        session_start = request.POST.get('session_start')
        session_end = request.POST.get('session_end')
        course_id = request.POST.get('course')
        sex = request.POST.get('sex')

        if request.FILES['profile_pic']:
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

            student = Students.objects.get(id=student_id)
            student.address=address
            student.session_start_year=session_start
            student.session_end_year=session_end
            course_obj=Courses.objects.get(id=course_id)
            user.students.course_id=course_obj
            
            if profile_pic_url !=None:
                student.profile_pic= profile_pic_url
            student.gender=sex
            student.batch=batch
            student.date=date
            student.contact=contact
            student.dob=dob
            student.save()

            messages.success(request,"Successfully Edited Student")
            return HttpResponseRedirect("/edit_student/"+ student_id)
        except Exception as e:
            print(e)
            raise e
            messages.error(request,"Failed to Edit Student")
            return HttpResponseRedirect("/edit_student/"+ student_id)

def edit_subject(request ,subject_id):
    subject = Subjects.objects.get(id=subject_id)
    courses = Courses.objects.all()
    staffs = CustomUser.objects.filter(user_type=2)
    return render(request, 'hod_templates/edit_subject_template.html',{'subject':subject , 'courses':courses, 'staffs':staffs})

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
            return HttpResponseRedirect("/edit_subject/"+ subject_id)

        except Exception as e:
            print(e)
            raise e
            messages.error(request,"Failed to Edit Subject")
            return HttpResponseRedirect("/edit_subject/"+ subject_id)

def edit_course(request, course_id):
    course =Courses.objects.get(id=course_id)
    return render(request, 'hod_templates/edit_course_template.html',{'course':course})

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
            return HttpResponseRedirect("/edit_course/"+ course_id)

        except Exception as e:
            print(e)
            raise e
            messages.error(request,"Failed to Edit Course")
            return HttpResponseRedirect("/edit_course/"+ course_id)
        




