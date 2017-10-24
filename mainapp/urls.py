from django.conf.urls import url
from .views import signupView,loginView,success,homeView,logout

app_name = 'mainapp'

urlpatterns = [
    url(r'^$',homeView.as_view(),name='home'),
    url(r'^signup/',signupView.as_view(),name='signup'),
    url(r'^login/',loginView.as_view(),name='login'),
    url(r'^logout/',logout,name='logout'),
    url(r'^success/',success,name='success')
]