from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from myapp.forms import SignUpForm
from django.contrib import messages
from django.db.models import Q
from myapp.forms import BloodRequestForm

from myapp.models import BloodGroup, BloodRequestSession,BloodRequestStatus 



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


def search(request):
    """
    GET / search/blood-donner
        * Input 
            - []blood_group (minimum 1 is required)(select)
            - address
            - date
        * Return
            - [
                user {
                    - name
                    - blood_group
                    - last_donated_date
                }
            ].order_by('last_donated_date')

        * Template 
            -Tabale
                -data [Click] -> Invite
                - multi select | send Invite [users] -> invitation
    """
    pass


def search(request):
    data = BloodRequestSession.objects.all() 
    blood_groups = BloodGroup.objects.all()
    if 'q' in request.GET:
        q = request.GET('q')
        multiple_q = Q(Q(blood_groups__icontains=q)|Q(pincode__icontains=q)|Q(req_date__icontains=q))
        data = BloodRequestSession.filter(multiple_q)
    else:
        BloodRequestSession.objects.all()
    context = {
        'data':data,
        'blood_groups':blood_groups
    }    
    return render(request,'search.html',context)
