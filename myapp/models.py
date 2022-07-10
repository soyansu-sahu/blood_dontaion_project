from datetime import datetime
from enum import Enum
from http.client import ACCEPTED
from django.utils.timezone import now
from statistics import mode
from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class BloodGroup(models.Model):
    """
    BloodGroup
    
    """

    name = models.CharField(primary_key=True,max_length=4)
    # req_sessions = models.ManyToManyField('BloodRequestSession', through='BloodGroupSessionMapper')
    # users

    def __str__(self):
        return self.name

class UserDetail(models.Model):
    """
    UserDetails is a extended model of User model
    It keeps the user's blood_group, contact_no, address
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    blood_group = models.ForeignKey(BloodGroup, on_delete=models.DO_NOTHING)
    contact_no = models.CharField(max_length=10, unique=True)
    pincode = models.IntegerField()
    image = models.ImageField(upload_to='static/images', blank=True)
    is_donor = models.BooleanField(default=True)
    last_donated_date = models.DateTimeField(default=now)

    def __str__(self):
        return str(self.user)


class BloodRequestSession(models.Model):
    """
    Blood Request session will contain the details about 
    the user who requested 
    the blood group
    the time limit
    at which address

    [] Request Detais
    """
    # id = models.IntegerField(primary_key=True)
    req_user = models.ForeignKey(User, on_delete=models.CASCADE)
    pincode = models.IntegerField()
    total_unit = models.PositiveIntegerField(default=1)  # 1unit = 500ml blood
    req_date = models.DateTimeField(max_length=100, default=now)
    till_date = models.DateTimeField(default=now)

    blood_groups = models.ManyToManyField(BloodGroup, through='BloodGroupSessionMapper',
        related_name='requests',
       
     )
    # blood_groups = models.ForeignKey(BloodGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.req_user}_{self.blood_groups}_{self.pincode}"
        #  return f"->{self.blood_groups}-[{self.unit}]-{self.start_date}"






"""
class StatusTypes(Enum):
    PENDING, ACCEPTED, REJECTED = 'pending', 'accepted', 'rejected'
"""


class BloodGroupSessionMapper(models.Model):
   
    blood_group = models.ForeignKey( BloodGroup, on_delete=models.CASCADE, related_name='bloodgroups')
    request_session = models.ForeignKey( BloodRequestSession, on_delete=models.CASCADE, related_name='sessions')



    def __str__(self):
        #  ["A+, O+"]
        return f'{self.blood_group.__str__}_{self.request_session.__str__}'


class BloodRequestStatus(models.Model):
    donner = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    session = models.ForeignKey(BloodRequestSession, on_delete=models.CASCADE)
    invitation_status = models.CharField(max_length=10, default='pending')
    donation_status = models.CharField(max_length=10, default='False')
    donation_date = models.DateTimeField(default=now)

    # inv_response = models.CharField(max_length=100,default=StatusTypes.PENDING)

    def __str__(self):
        return f"{self.invitation_status}_{self.donation_status}"
