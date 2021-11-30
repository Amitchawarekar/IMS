from django import forms
from django.forms.widgets import NumberInput
from IMS_app.models import Courses, SessionYearModel

class DateInput(forms.DateInput):
    input_type = "date"


class AddStudentForm(forms.Form):

    course_list=[]
    courses=Courses.objects.all()
    
    for course in courses:
        small_course=(course.id,course.course_name)
        course_list.append(small_course)


    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    batch_choice=(
        ("January","January"),
        ("February","February"),
        ("March","March"),
        ("April","April"),
        ("May","May"),
        ("June","June"),
        ("July","July"),
        ("August","August"),
        ("September","September"),
        ("October","October"),
        ("November","November"),
        ("December","December"),
    )

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year)+"   TO  "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list=[]

    date=forms.DateField(label="Date",widget=DateInput(attrs={"class":"form-control"}))
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control","autocomplete":"off"}))
    password=forms.CharField(label="Password",max_length=50,widget=forms.PasswordInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    batch=forms.ChoiceField(label="Batch",choices=batch_choice,widget=forms.Select(attrs={"class":"form-control"}))
    contact=forms.CharField(label="Contact Number",max_length=50,widget=NumberInput(attrs={"class":"form-control"}))
    dob=forms.DateField(label="Date of Birth",widget=DateInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control","autocomplete":"off"}))
    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Duration",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",widget=forms.FileInput(attrs={"class":"form-control"}))
    coursefees=forms.CharField(label="Course Fees",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control", "onkeyup":"balance(value1)"}))
    amountpaid=forms.CharField(label="Amount Paid",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control","onkeyup":"balance(value2)"}))
    date_ap=forms.DateField(label="Date of Amount Paid",widget=DateInput(attrs={"class":"form-control"}))
    balance=forms.CharField(label="Balance Amount",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))
    cerificate_issue=forms.CharField(label="Certificate Issued",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    cerificate_issue_date=forms.DateField(label="Date of Certificate Issue",widget=DateInput(attrs={"class":"form-control"}),required=False)

class EditStudentForm(forms.Form):

    course_list=[]
    try:
        courses=Courses.objects.all()
        for course in courses:
            small_course=(course.id,course.course_name)
            course_list.append(small_course)
    except:
        course_list=[]


    gender_choice=(
        ("Male","Male"),
        ("Female","Female")
    )

    batch_choice=(
        ("January","January"),
        ("February","February"),
        ("March","March"),  
        ("April","April"),
        ("May","May"),
        ("June","June"),
        ("July","July"),
        ("August","August"),
        ("September","September"),
        ("October","October"),
        ("November","November"),
        ("December","December"),
    )

    session_list = []
    try:
        sessions = SessionYearModel.object.all()

        for ses in sessions:
            small_ses = (ses.id, str(ses.session_start_year)+"   TO  "+str(ses.session_end_year))
            session_list.append(small_ses)
    except:
        session_list=[]

    date=forms.DateField(label="Date",widget=DateInput(attrs={"class":"form-control"}))
    email=forms.EmailField(label="Email",max_length=50,widget=forms.EmailInput(attrs={"class":"form-control"}))
    first_name=forms.CharField(label="First Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    last_name=forms.CharField(label="Last Name",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    batch=forms.ChoiceField(label="Batch",choices=batch_choice,widget=forms.Select(attrs={"class":"form-control"}))
    contact=forms.CharField(label="Contact Number",max_length=50,widget=NumberInput(attrs={"class":"form-control"}))
    dob=forms.DateField(label="Date of Birth",widget=DateInput(attrs={"class":"form-control"}))
    username=forms.CharField(label="Username",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    course=forms.ChoiceField(label="Course",choices=course_list,widget=forms.Select(attrs={"class":"form-control"}))
    address=forms.CharField(label="Address",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    sex=forms.ChoiceField(label="Gender",choices=gender_choice,widget=forms.Select(attrs={"class":"form-control"}))
    session_year_id=forms.ChoiceField(label="Session Duration",choices=session_list,widget=forms.Select(attrs={"class":"form-control"}))
    profile_pic=forms.FileField(label="Profile Pic",widget=forms.FileInput(attrs={"class":"form-control"}),required=False)
    coursefees=forms.CharField(label="Course Fees",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))
    amountpaid=forms.CharField(label="Amount Paid",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))
    date_ap=forms.DateField(label="Date of Amount Paid",widget=DateInput(attrs={"class":"form-control"}))
    balance=forms.CharField(label="Balance Amount",max_length=50,widget=forms.NumberInput(attrs={"class":"form-control"}))
    cerificate_issue=forms.CharField(label="Certificate Issued",max_length=50,widget=forms.TextInput(attrs={"class":"form-control"}))
    cerificate_issue_date=forms.DateField(label="Date of Certificate Issue",widget=DateInput(attrs={"class":"form-control"}),required=False)