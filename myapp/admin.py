from django.contrib import admin
from myapp.models import BloodRequestStatus,BloodRequestSession,UserDetail,BloodGroup, BloodGroupSessionMapper

#Register your models here.

admin.site.register(BloodGroup)
admin.site.register(BloodGroupSessionMapper)


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'pincode', 'last_donated_date')


@admin.register(BloodRequestSession)
class BloodRequestSessionAdmin(admin.ModelAdmin):
    list_display = ['req_user', 'pincode', 'total_unit', 'req_date', 'till_date']


@admin.register(BloodRequestStatus)
class BloodRequestStatusAdmin(admin.ModelAdmin):
    list_display = ['donner', 'session', 'invitation_status', 'donation_status', 'donation_date']




# class BloodRequestadmin(admin.ModelAdmin):
#     pass

# @admin.register(RequestBlood)
# class RequestBloodadmin(admin.ModelAdmin):
#     pass

# @admin.register(BloodNeedSatisfaction)
# class BloodNeedSatisfactionadmin(admin.ModelAdmin):
#     pass

# @admin.register(Invitation)
# class Invitationadmin(admin.ModelAdmin):
#     pass

# @admin.register(BloodDonationHistory)
# class BloodDonationHistoryadmin(admin.ModelAdmin):
    # pass
