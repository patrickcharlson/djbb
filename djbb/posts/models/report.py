from django.conf import settings
from django.db import models


class Report(models.Model):
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reported_by', verbose_name='Reported by',
                                    on_delete=models.CASCADE)
    post = models.ForeignKey("posts.Post", verbose_name='Post', on_delete=models.CASCADE)
    zapped = models.BooleanField('Zapped', blank=True, default=False)
    zapped_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='zapped_by', blank=True, null=True,
                                  verbose_name='Zapped by', on_delete=models.CASCADE)
    created = models.DateTimeField('Created', blank=True)
    reason = models.TextField('Reason', blank=True, default='', max_length='1000')

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

    def __str__(self):
        return '%s %s' % (self.reported_by, self.zapped)
