from django.contrib import admin
from myapp.models import BloodRequestStatus,BloodRequestSession,UserDetail,BloodGroup, BloodGroupSessionMapper

#Register your models here.

admin.site.register(BloodGroup)
# admin.site.register(UserDetail)
admin.site.register(BloodRequestSession)
admin.site.register(BloodRequestStatus)
admin.site.register(BloodGroupSessionMapper)


@admin.register(UserDetail)
class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'blood_group', 'pincode', 'last_donated_date')



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
