from django.urls import re_path

from djbb.forum import views

app_name = "forums"
urlpatterns = [
    re_path('^$', views.index, name='index'),

]
