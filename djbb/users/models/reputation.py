from django.conf import settings
from django.db import models
from django.utils import timezone

SIGN_CHOICES = (
    (1, 'PLUS'),
    (-1, 'MINUS'),
)


class Reputation(models.Model):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reputations_from', verbose_name='From',
                                  on_delete=models.CASCADE)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reputations_to', verbose_name='To',
                                on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", related_name='post', verbose_name='Post', on_delete=models.CASCADE)
    time = models.DateTimeField('Time', auto_now_add=True)
    sign = models.IntegerField('Sign', choices=SIGN_CHOICES, default=0)
    reason = models.TextField('Reason', max_length=1000)

    class Meta:
        verbose_name = 'Reputation'
        verbose_name_plural = 'Reputations'
        db_table = 'reputations'
        unique_together = (('from_user', 'post'),)

    def __str__(self):
        time = timezone.localtime(self.time)
        return 'T[%d], FU[%d], TU[%d]: %s' % (self.post.id, self.from_user.id, self.to_user.id, str(time))
