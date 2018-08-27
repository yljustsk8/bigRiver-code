#urlpatterns = [
#    path('admin/', admin.site.urls),
#]
from django.urls import path
from . import view,testdb
from django.conf.urls.static import static

urlpatterns = [
    #path('hello/', view.hello),
    path('calendar/',view.calendar),
    path('login/', view.login),
    path('index/', view.index),
    path('login/regist/', view.regist),
    path('testdb/',testdb.testdb)
]
