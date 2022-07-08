from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib import messages
from django.db.models import Q
from .forms import BloodRequestForm

from myapp.models import BloodGroup,UserDetail,BloodRequestSession,BloodRequestStatus, BloodGroupSessionMapper,User



# Create your views here.
def home(request):
    return render(request,'home.html')

    


# def request_blood(request):
#     if request.method == "POST":
#         form =BloodRequestForm(request.POST)

#         if form.is_valid():
#             req_name = form.cleaned_data["name"]
#             pincode = form.cleaned_data["pincode"]
#             blood_group = form.cleaned_data["blood_group"]
#             total_unit = form.cleaned_data["total_unit"]
#             req_date = form.cleaned_data["req_date"]
#             reg = BloodRequestSession(req_name=req_name,pincode=pincode,blood_group=blood_group,total_unit=total_unit,req_date=req_date)

#             reg.save()
#     else:
#         form = BloodRequestForm()

#     return render(request, "request_blood.html", {"form":form} )         
def request_blood(request):
    if request.method == "POST":
        req_user = request.POST['req_user']
        pincode = request.POST['pincode']
        total_unit = request.POST['total_unit']
        req_date = request.POST['req_date']
        till_date = request.POST['till_date']
        blood_groups = request.POST['blood_groups']
        blood_requests = BloodRequestSession.objects.create(name=req_user, pincode=pincode, total_unit=total_unit, req_date=req_date,till_date=till_date, blood_groups = blood_groups)
        print(blood_requests)
        blood_requests.save()
        return render(request, "home.html")
    return render(request, "request_blood.html")




def see_all_request(request):
    """
    This method shows a single user blood request sessions
        - Request Sessions []


    """
    blod_req_sessions = BloodRequestSession.objects.all()
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

    # print(main_data)

    return render(request,"see_all_request.html",{"request_sessions":main_data})        


    
    # return render(request, "see_all_request.html", {'requests':requests})










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





# def search(request):
#     data = BloodRequest.objects.all()
#     return render(request,'search.html')    






# def search(request):
#     """
#     GET / search/blood-donner
#         * Input 
#             - []blood_group (minimum 1 is required)(select)
#             - address
#             - date
#         * Return
#             - [
#                 user {
#                     - name
#                     - blood_group
#                     - last_donated_date
#                 }
#             ].order_by('last_donated_date')

#         * Template 
#             -Tabale
#                 -data [Click] -> Invite
#                 - multi select | send Invite [users] -> invitation
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



# # def search(request):
# #     if request.method == "GET":
# #         blood_group = request.GET.get("blood_group")
# #         pincode = request.GET.get("pincode")
# #         req_date = request.GET.get("req_date")
# #         if blood_group:
# #             results = BloodRequestSession.filter(BloodRequestSession.blood_group== blood_group)
# #         if pincode:
# #             results = BloodRequestSession.filter(BloodRequestSession.pincode == pincode)
# #         if req_date:
# #             results = BloodRequestSession.filter(BloodRequestSession.req_date == req_date) 

# #         data = BloodRequestSession.objects.all()               
# #     return render(request,'search.html')