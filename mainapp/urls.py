from django.conf.urls import url
from .views import signupView,loginView,success

app_name = 'mainapp'

urlpatterns = [
    url(r'^signup/',signupView.as_view(),name='signup'),
    url(r'^login/',loginView.as_view(),name='login'),
    url(r'^success/',success,name='success')
]