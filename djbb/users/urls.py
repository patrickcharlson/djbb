from django.urls import re_path

from djbb.users import views

app_name = 'users'
urlpatterns = [
    re_path('^user/(?P<username>.*)/$', views.get_user, name='forum_profile'),

]
