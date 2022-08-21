from django.conf import settings
from django.db import models
from django.urls import reverse


class Topic(models.Model):
    forum = models.ForeignKey("forum.Forum", related_name='topics', verbose_name='Forum', on_delete=models.CASCADE)
    name = models.CharField('Subject', max_length=255)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='User', on_delete=models.CASCADE)
    views = models.IntegerField('Views count', blank=True, default=0)
    sticky = models.BooleanField('Sticky', blank=True, default=False)
    closed = models.BooleanField('Closed', blank=True, default=False)
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscriptions',
                                         verbose_name='Subscribers', blank=True)
    post_count = models.IntegerField('Post count', blank=True, default=0)
    last_post = models.ForeignKey('posts.Post', related_name='last_topic_post', blank=True, null=True,
                                  on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-updated']
        get_latest_by = 'updated'
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        db_table = 'topics'

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        try:
            last_post = self.posts.latest()
            last_post.last_forum_post.clear()
        except Post.DoesNotExist:
            pass
        else:
            last_post.last_forum_post.clear()
        forum = self.forum
        super(Topic, self).delete(*args, **kwargs)
        try:
            forum.last_post = Topic.objects.filter(forum__id=forum.id).latest().last_post
        except Topic.DoesNotExist:
            forum.last_post = None
        forum.topic_count = Topic.objects.filter(forum__id=forum.id).count()
        forum.post_count = Post.objects.filter(topic__forum__id=forum.id).count()
        forum.save()

    @property
    def head(self):
        try:
            return self.posts.select_related().order_by('created')[0]
        except IndexError:
            return None

    @property
    def reply_count(self):
        return self.post_count - 1

    def get_absolute_url(self):
        return reverse('djangobb:topic', args=[self.id])

    def update_read(self, user):
        tracking = user.posttracking
        # if last_read > last_read - don't check topics
        if tracking.last_read and (tracking.last_read > self.last_post.created):
            return
        if isinstance(tracking.topics, dict):
            # clear topics if len > 5Kb and set last_read to current time
            if len(tracking.topics) > 5120:
                tracking.topics = None
                tracking.last_read = timezone.now()
                tracking.save()
            # update topics if exist new post or doesn't exist in dict
            if self.last_post_id > tracking.topics.get(str(self.id), 0):
                tracking.topics[str(self.id)] = self.last_post_id
                tracking.save()
        else:
            # initialize topic tracking dict
            tracking.topics = {self.id: self.last_post_id}
            tracking.save()
