"""bigRiver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from . import view
from django.conf import settings
from django.conf.urls.static import static
import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bigRiver.settings")
django.setup()

urlpatterns = [
    #path('hello/', view.hello),
    path('',view.login),
    path('aboutBOT/',view.about_us),
    path('user/',view.user),
    path('userinfo/',view.user_info),
    path('useredit/',view.user_edit),
    path('usercompany/',view.user_company),
    path('usercompany/search/',view.search_company),
    path('usercompany/confirm/',view.confirm_join),
    path('createcompany/',view.create_company),
    path('login/', view.login),
    path('calendar/',view.calendar),
    path('register/',view.regist),
    path('login/regist/', view.regist),
    path('face/', view.face),
    path('face/uploadimage/',view.upload_image),
    path('face/face_enter/',view.face_enter),
    path('face/camera/',view.face_camera),
    path('admin/', view.admin_employees),
    path('admin/employees/', view.admin_employees),
    path('admin/requests/', view.admin_requests),
    path('boss/', view.boss_admins),
    path('boss/employees/', view.boss_admins),
    path('boss/requests/', view.boss_requests),
    # path('send_requests/',view.send_requests),
    path('handle_requests/', view.handle_requests)
] + static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
