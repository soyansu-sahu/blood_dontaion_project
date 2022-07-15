from cmath import log
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from myapp.models import BloodRequestSession, BloodGroup



class SignUpForm(UserCreationForm):
    password2 = forms.CharField(label='Confirm Password (again)', widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        labels = {'email': 'Email'}

class BloodRequestForm(forms.ModelForm):
    """
    This is a form class for blood request session
    """
    blood_groups = forms.MultipleChoiceField(choices = [(each, str(each.name)) for each in BloodGroup.objects.all()], widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = BloodRequestSession
        fields = ['pincode', 'total_unit', 'till_date', 'blood_groups']
        # labels = {'req_user':'Enter name','pincode':'Enter pincode','total_unit':'Enter total_unit'}
        widgets = {'req_user': forms.HiddenInput()}
        error_messages = {
            'pincode':{'required':"Enter pincode"},
            'total_unit':{'required':"Enter total_unit"},
            'till_date':{'required':"Enter till_date"},
            'blood_groups':{'required':"Enter till_date"},
        }