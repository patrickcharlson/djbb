from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db.models import Q
from django.shortcuts import render

from djbb.forum.models import Forum
from djbb.posts.models import Post
from djbb.topics.models import Topic

User = get_user_model()


def index(request):
    users_cached = cache.get('djbb_users_online', {})
    users_online = users_cached and User.objects.filter(id__in=users_cached.keys()) or []
    guests_cached = cache.get('djbb_guests_online', {})
    guest_count = len(guests_cached)
    users_count = len(users_online)

    _forums = Forum.objects.all()
    user = request.user
    if not user.is_superuser:
        user_groups = user.groups.all() or []  # need 'or []' for anonymous user otherwise: 'EmptyManager' object is not iterable
        _forums = _forums.filter(Q(category__groups__in=user_groups) | Q(category__groups__isnull=True))

    _forums = _forums.select_related('last_post__topic', 'last_post__user', 'category')

    cats = {}
    forums = {}
    for forum in _forums:
        cat = cats.setdefault(forum.category.id,
                              {'id': forum.category.id, 'cat': forum.category, 'forums': []})
        cat['forums'].append(forum)
        forums[forum.id] = forum

    cmpkey = lambda x: x['cat'].position
    cats = sorted(cats.values(), key=cmpkey)

    context = {
        'cats': cats,
        'posts': Post.objects.count(),
        'topics': Topic.objects.count(),
        'users': User.objects.count(),
        'users_online': users_online,
        'online_count': users_count,
        'guest_count': guest_count,
        # 'last_user': User.objects.latest('date_joined'),
    }

    return render(request, 'djbb/index.html', context)
