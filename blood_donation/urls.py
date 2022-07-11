"""blood_donation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('request_blood',views.request_blood,name='request_blood'),
    path('all_request',views.see_all_request,name='all_request'),
    path('logout/', views.logout_user, name='logout'),
    path('sign_up/', views.sign_up, name ='sign_up'),
    path('user_login/', views.user_login, name ='user_login'),
    path('search/',views.search_blood_doner,name='search'),
    path('status_detail/',views.req_status_details,name='view_detail'),
    

]
