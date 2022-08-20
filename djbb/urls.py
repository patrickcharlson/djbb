from django.urls import path, include

app_name = 'djforum'
urlpatterns = [
    path('', include('djbb.categories.urls', namespace='categories')),
    path('', include('djbb.forum.urls', namespace='forums')),
    path('', include('djbb.topics.urls', namespace='topics')),
    path('', include('djbb.posts.urls', namespace='posts')),
    path('', include('djbb.users.urls', namespace='users'))
]
