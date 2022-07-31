from django.contrib import admin
from django.urls import path
from myapp import views
from django.conf.urls.static import static
from django.conf import settings





urlpatterns = [
    path('admin/', admin.site.urls),
    path('logout/', views.logout_user, name='logout'),
    path('user_login/', views.user_login, name ='user_login'),
    path('sign_up/', views.sign_up, name ='sign_up'),
    path('', views.home, name='home'),
    path('request_blood',views.request_blood,name='request_blood'),
    path('all_request',views.see_all_request,name='all_request'),
    path('search/',views.search_blood_doner,name='search'),
    path('donate/send_invitation/',views.send_donation_invitation,name='send_invitation'),
    path('invitation_status_detail/<int:id>', views.view_session_detail, name='view_session_detail'),
    path('update_status/<int:session_id>/<int:user_id>/<str:is_accepted>',views.update_inv_status,name='update_status'),

]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
