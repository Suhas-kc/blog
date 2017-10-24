from django.conf.urls import url
from .views import signupView,loginView,success,homeView,logoutView,submitBlogView,blogView

app_name = 'mainapp'

urlpatterns = [
    url(r'^$',homeView.as_view(),name='home'),
    url(r'^signup/',signupView.as_view(),name='signup'),
    url(r'^login/',loginView.as_view(),name='login'),
    url(r'^logout/',logoutView,name='logout'),
    url(r'^submit/',submitBlogView.as_view(),name='submit'),
    url(r'^blog/(?P<num>[0-9]+)/',blogView.as_view(),name='blog'),
    url(r'^success/',success,name='success')
]