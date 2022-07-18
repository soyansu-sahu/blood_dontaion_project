import json
from ast import Not
from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from myapp.forms import SignUpForm
from django.contrib import messages
from django.db.models import Q
from myapp.forms import BloodRequestForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.forms.models import model_to_dict

from myapp.models import BloodGroup, BloodRequestSession,BloodRequestStatus,UserDetail



# Create your views here.
def home(request):
    return render(request,'home.html')


def request_blood(request):
    
    if request.method == "POST":
        form = BloodRequestForm(request.POST)

        if form.is_valid():
            req_user = form.cleaned_data.get("req_user")
            pincode = form.cleaned_data.get("pincode")
            total_unit = form.cleaned_data.get("total_unit")
            req_date = form.cleaned_data.get("req_date")
            blood_groups = form.cleaned_data.get("blood_groups")
            bloodgroups = BloodGroup.objects.filter(name__in=blood_groups)
            blood_requests = BloodRequestSession.objects.create(req_user=req_user,pincode=pincode,total_unit=total_unit,req_date=req_date)     

            print(pincode,req_user)                   
            
            for bloodgroup in bloodgroups:
               blood_requests.blood_groups.add(bloodgroup)
            blood_requests.save()
            return redirect("all_request")
        else:
            print("hi from else")
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
            "id": session_req.id,
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

    return render(request,"see_all_request.html",{"request_sessions": main_data})        


def view_session_detail(request, id):
    session_data = BloodRequestSession.objects.get(id=id)#.order_by('-req_date')
    user_invitation_data = BloodRequestStatus.objects.filter(session=session_data.id).all()
    blood_groups = []
    for blood_group in session_data.blood_groups.all():
        blood_groups.append(blood_group.name)

    return render(request,'user_invitation_status.html',{
        'user_invitation_data':user_invitation_data,
        'session_data': session_data,
        'blood_groups': blood_groups
        })





def search_blood_doner(request):
    
    users=[]
    if request.method == "POST":
        form = BloodRequestForm(request.POST)
        


        if form.is_valid():
            pincode = form.cleaned_data.get("pincode")
            blood_groups = form.cleaned_data.get("blood_groups")
            users = UserDetail.objects.filter(Q(blood_group__in = blood_groups)).filter(Q(pincode = pincode)).all()
            print(users)
    else:
        form = BloodRequestForm()
        
    


        
    return render(request,'search.html',{"form":form, 'users':users})


def send_donation_invitation(request):
    print(request.POST)
    if request.method == 'POST':
        form_data = json.loads(request.POST.get("formData"))
        req_user = request.user
        pincode = form_data['pincode']    
        total_unit = form_data['total_unit']
        till_date = form_data['till_date']
        blood_groups = form_data['blood_groups'] # ['A +', 'O +']
        matched_bloodgroups = BloodGroup.objects.filter(name__in=blood_groups)
        # print(pincode ,total_unit, till_date, blood_groups, matched_bloodgroups)
        request_session = BloodRequestSession.objects.create(req_user=req_user,pincode=pincode,total_unit=total_unit,till_date=till_date)
        
        for _bloodgroup in matched_bloodgroups:
            request_session.blood_groups.add(_bloodgroup)
        request_session.save(),
        print(request_session.__dict__)

        selected_users = json.loads(request.POST.get("selected_users"))
        print("selected_users > ", type(selected_users), selected_users)

        for user_id in selected_users:
            _user = User.objects.get(id=int(user_id))
            _user_deatils = UserDetail.objects.get(user=_user)
            obj = BloodRequestStatus.objects.create(
                donner=_user, 
                blood_group=_user_deatils.blood_group,
                session=request_session,
                )
            obj.save()

    return JsonResponse(data={
        "message":"Invitation Sent Successfully",
        "url": f"/invitation_status_detail/{request_session.id}"
    })  



    





def send_mail_user(request):
    send_mail(
        'testing email',
        'This is used for testing purpose',
        'soyansuwork@gmail.com',
        ['ssoyansu@gmail.com'],
        fail_silently=False,



    )
    return render(request,'send_mail.html')

    
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