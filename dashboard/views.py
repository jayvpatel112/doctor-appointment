from django.shortcuts import render, redirect
from .models import User, Post, Draft, bookappointment
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url = 'login')
def home(request):
    # userdetail = User.objects.filter(username=request.user)
    userdetail = User.objects.get(id=request.user.id)
    doctors = User.objects.filter(user_type=2)
    # for i in doctors:
    #     print(i.first_name)
    # print(doctors[1:])
    print(request.user)
    if userdetail.user_type == 1 :
        if request.method == "POST":
            submit = request.POST.get("submit")
            doctorname = request.POST.get("doctorname")
            print(doctorname)
            if submit == "bookappointment":
                b = bookappointment(doctor_name=doctorname, required_specification="", appointment_date="2022-09-14", appointment_start_time="14:15", appointment_end_time="5:00", username=request.user)
                b.save()
                print(b.id)
                return redirect('appoinmentconfirm', id=b.id)
    else:
        if request.method == "POST":
            title = request.POST.get("title")
            image = request.FILES["image"]
            category = request.POST.get("category")
            content = request.POST.get("content")
            submit = request.POST.get("submit")
            print(submit)
            if submit == "createpost":
                post = Post(title=title, image=image, category=category, content=content, username=request.user)
                post.save()
            else:
                draft = Draft(title=title, image=image, category=category, content=content, username=request.user)
                draft.save()
            return redirect('profile')
    return render(request, 'dashboard/home.html', {"userdetail":userdetail, "doctors": doctors[:]})

def signup(request):
    if request.method == "POST":
        firstname = request.POST.get("firstname")
        lastname = request.POST.get('lastname')
        Profile_Picture = request.FILES["profile_picture"]
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        user_type = request.POST.get('user_type')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('signup')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'email already exists')
                    return redirect('signup')
                else:
                    user = User.objects.create_user(first_name=firstname, last_name=lastname, Profile_Picture=Profile_Picture, email=email, username=username, password=password, address=address, city=city, state=state,pincode=pincode, user_type=user_type)
                    user.save()
                    messages.success(request, "account created successfully")
                    return redirect('login')
        else:
            messages.error(request, 'Password do not match')
            return redirect("signup")

    return render(request, 'dashboard/signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect('home')
        else:
            messages.error(request, 'Invalid login credentials')
            return redirect('login')

    return render(request, 'dashboard/login.html')

@login_required(login_url = 'login')
def profile(request):
    # userdetail = User.objects.filter(username=request.user)
    userdetail = User.objects.get(id=request.user.id)
    print(userdetail)
    return render(request, 'dashboard/profile.html', {"userdetail":userdetail})

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are successfully logout")

    return redirect('home')

@login_required(login_url = 'login')
def allpost(request):
    userdetail = User.objects.get(id=request.user.id)
    if userdetail.user_type == 1:
        posts1 = Post.objects.filter(category=1)
        posts2 = Post.objects.filter(category=2)
        posts3 = Post.objects.filter(category=3)
        posts4 = Post.objects.filter(category=4)
        posts = Post.objects.all()
    else:
        posts = Post.objects.filter(username=request.user)
        posts1 = posts.filter(category=1)
        posts2 = posts.filter(category=2)
        posts3 = posts.filter(category=3)
        posts4 = posts.filter(category=4)
    return render(request, 'dashboard/allposts.html', {"posts1":posts1,"posts2":posts2,"posts3":posts3,"posts4":posts4, "userdetail":userdetail})

    # return redirect()
@login_required(login_url = 'login')
def draft(request):
    userdetail = User.objects.get(id=request.user.id)
    if userdetail.user_type == 2:
        drafts = Draft.objects.filter(username=request.user)
        print(drafts)
    else:
        return redirect('home')
    if request.method == "POST":
        title = request.POST.get("title")
        image = request.POST.get("image")
        category = request.POST.get("category")
        content = request.POST.get("content")
        submit = request.POST.get("submit")
        draft_id = request.POST.get("draftid")
        print(draft_id)
        # print(submit)
        # if submit == "createpost":
        post = Post(title=title, image=image, category=category, content=content, username=request.user)
        post.save()
        draft = Draft.objects.get(id=draft_id)
        draft.delete()
        # if userdetail.user_type == 2:
        #     drafts = Draft.objects.filter(username=request.user)
        #     print(drafts)
        return render(request, 'dashboard/draft.html', {"draft": drafts})
    return render(request, 'dashboard/draft.html', {"draft": drafts})

from datetime import datetime
from datetime import timedelta

@login_required(login_url = 'login')
def appoinmentconfirm(request, id):
    if request.method == "POST":
        b= bookappointment.objects.get(id=id)
        print(b)
        speciality = request.POST.get('speciality')
        date = request.POST.get('date')
        time_str = request.POST.get('time')

        b.required_specification = speciality
        b.appointment_date = date
        b.appointment_start_time = time_str

        # print(b.id, b.appointment_start_time)
        # print(date, time_str)
        date_format_str = '%H:%M'
        given_time = datetime.strptime(time_str, date_format_str)
        final_time = given_time + timedelta(minutes=45)
        print(final_time)
        final_time_str = final_time.strftime('%H:%M')
        b.appointment_end_time = final_time_str
        b.save()
        # print(type(time))
        return redirect('finalconfirm', id)
    return render(request, 'dashboard/appointment.html', {"id":id})

from .calendar_API import test_calendar

@login_required(login_url = 'login')
def finalconfirm(request, id):
    b= bookappointment.objects.get(id=id)
    if request.method == "POST":
        b= bookappointment.objects.get(id=id)
        submit = request.POST.get("submit")
        if submit == "confirm":
            results = test_calendar(b.appointment_date, b.appointment_start_time, b.appointment_end_time)
            context = {"results": results}
            return redirect('bookslotdashboard')
            # return render(request, 'demo.html', context)
        else:
            b.delete()

    return render(request, 'dashboard/finalconfirm.html', {"b": b, "id": id})

@login_required(login_url = 'login')
def bookslotdashboard(request):
    b = bookappointment.objects.filter(username=request.user)
    return render(request, 'dashboard/bookslotdashboard.html', {"slots": b})