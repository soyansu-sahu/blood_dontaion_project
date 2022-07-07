from dataclasses import field
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# from . models import BloodRequestSession



class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}




class BloodRequestForm(forms.Form):
    name = forms.CharField(max_length=100)
    pincode = forms.IntegerField()
    blood_group = forms.CharField(max_length=10)
    total_unit = forms.IntegerField()
    req_date = forms.DateTimeField()





# class bloodRequestForm(forms.ModelForm):
#     blood_groups = forms.CharField(max_length=5,required=True)
#     class Meta:
#         model = BloodRequestSession
#         fields = ['pincode', 'total_unit', 'req_date','till_date','x']
#         labels = {'pincode':'Enter pincode','total_unit':'Enter total_unit','req_date':'Enter req_date','till_date':'Enter till_date','blood_groups':'Enter blood_group'

        # }
        # error_messages = {
        #     'req_user':{'required':"Enter name"},
        #     'pincode':{'required':"Enter pincode"},
        #     'total_unit':{'required':"Enter total_unit"},
        #     'req_date':{'required':"Enter req_date"},
        #     'till_date':{'required':"Enter till_date"},
        #     'blood_groups':{'required':"Enter blood_groups"},


            
        # }