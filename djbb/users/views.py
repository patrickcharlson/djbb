from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import render, get_object_or_404

from djbb.users.forms import EssentialsProfileForm

User = get_user_model()


@transaction.atomic
def get_user(request, username, section='essentials', action=None,
             template='djbb/users/profile_essentials.html', form_class=EssentialsProfileForm):
    user = get_object_or_404(User, username=username)
    if request.user.is_authenticated() and user == request.user or request.user.is_superuser:
        form = build_form(form_class, request, instance=user.forum_profile, extra_args={'request': request})
        if request.method == 'POST' and form.is_valid():
            form.save()
            profile_url = reverse('djangobb:forum_profile_%s' % section, args=[user.username])
            messages.success(request, _("User profile saved."))
            return HttpResponseRedirect(profile_url)
        return render(request, template, {'active_menu': section,
                                          'profile': user,
                                          'form': form,
                                          })
    else:
        template = 'djangobb_forum/user.html'
        topic_count = Topic.objects.filter(user__id=user.id).count()
        if user.forum_profile.post_count < forum_settings.POST_USER_SEARCH and not request.user.is_authenticated():
            messages.error(request, _("Please sign in."))
            return HttpResponseRedirect(settings.LOGIN_URL + '?next=%s' % request.path)
        return render(request, template, {'profile': user,
                                          'topic_count': topic_count,
                                          })
