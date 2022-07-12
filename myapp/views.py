from ast import Not
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from myapp.forms import SignUpForm
from django.contrib import messages
from django.db.models import Q
from myapp.forms import BloodRequestForm
from django.core.mail import send_mail

from myapp.models import BloodGroup, BloodRequestSession,BloodRequestStatus,UserDetail 



# Create your views here.
def home(request):
    return render(request,'home.html')


def request_blood(request):
    
    if request.method == "POST":
        print("request.POST : ", request.POST)
        form =BloodRequestForm(request.POST)

        if form.is_valid():
            req_user = form.cleaned_data.get("req_user")
            pincode = form.cleaned_data.get("pincode")
            total_unit = form.cleaned_data.get("total_unit")
            req_date = form.cleaned_data.get("req_date")
            blood_groups = form.cleaned_data.get("blood_groups")
            bloodgroups = BloodGroup.objects.filter(name__in=blood_groups)
            blood_requests = BloodRequestSession.objects.create(req_user=req_user,pincode=pincode,total_unit=total_unit,req_date=req_date)                        
            for bloodgroup in bloodgroups:
               blood_requests.blood_groups.add(bloodgroup)
            blood_requests.save()
            return redirect("all_request")
    else:
        form = BloodRequestForm(initial={'req_user': request.user.id})

    return render(request, "request_blood.html", {"form":form} ) 


def see_all_request(request):
    """
    This method shows a single user blood request sessions
        - Request Sessions []
    """
    blod_req_sessions = BloodRequestSession.objects.all().order_by('-req_date')
    main_data = []
    for session_req in blod_req_sessions:
        _temp_req_session = {
            "req_user":session_req.req_user,
            "pincode" : session_req.pincode,
            "total_unit" : session_req.total_unit,
            "req_date" : session_req.req_date,
            "till_date" : session_req.till_date,
            "blood_groups": []
        }

        for blood_group in session_req.blood_groups.all():
            _temp_req_session["blood_groups"].append(blood_group.name)
        main_data.append(_temp_req_session)

    return render(request,"see_all_request.html",{"request_sessions":main_data})        


def req_status_details(request):
    # blod_req_sessions = BloodRequestSession.objects.get().order_by('-req_date')

    status_details = BloodRequestStatus.objects.all()
    return render(request,'details.html',{"status_details":status_details})


def sign_up(request):
    if request.method == 'POST':
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request,'Account created Sucessfully')
            fm.save()
            return redirect('user_login')
    else:
        fm = SignUpForm()        
    return render(request,'registration/signup.html',{'form':fm})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    return redirect('/')
        else:
            fm = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': fm})
    else:
        return redirect('/')
                      

def logout_user(request):
    logout(request)
    return redirect('user_login')


def search_blood_doner(request):
    form = BloodRequestForm(request.POST)
    
    if form.is_valid():
        pincode = form.cleaned_data.get("pincode")
        blood_groups = form.cleaned_data.get("blood_groups")
        users = UserDetail.objects.filter(Q(blood_group__in = blood_groups)).filter(Q(pincode = pincode))
        print(users)
    return render(request,'search.html',{"multiple_q":users})

def send_mail_user(request):
    send_mail(
        'testing email',
        'This is used for testing purpose',
        'soyansuwork@gmail.com',
        ['ssoyansu@gmail.com'],
        fail_silently=False,



    )

    
