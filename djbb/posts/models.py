from django.db import models
from django.urls import reverse

from djbb.core.conf import settings

MARKUP_CHOICES = [('bbcode', 'bbcode')]
try:
    import markdown

    MARKUP_CHOICES.append(("markdown", "markdown"))
except ImportError:
    pass


class Post(models.Model):
    topic = models.ForeignKey("topics.Topic", related_name='posts', verbose_name='Topic', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', verbose_name='User',
                             on_delete=models.CASCADE)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', blank=True, null=True)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Updated by', blank=True, null=True,
                                   on_delete=models.CASCADE)
    markup = models.CharField('Markup', max_length=15, default=settings.DEFAULT_MARKUP, choices=MARKUP_CHOICES)
    body = models.TextField('Message')
    body_html = models.TextField('HTML version')
    user_ip = models.GenericIPAddressField('User IP', blank=True, null=True)

    class Meta:
        ordering = ['created']
        get_latest_by = 'created'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'

    def save(self, *args, **kwargs):
        self.body_html = convert_text_to_html(self.body, self.markup)
        if forum_settings.SMILES_SUPPORT and self.user.forum_profile.show_smilies:
            self.body_html = smiles(self.body_html)
        super(Post, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self_id = self.id
        head_post_id = self.topic.posts.order_by('created')[0].id
        forum = self.topic.forum
        topic = self.topic
        profile = self.user.forum_profile
        self.last_topic_post.clear()
        self.last_forum_post.clear()
        super(Post, self).delete(*args, **kwargs)
        # if post was last in topic - remove topic
        if self_id == head_post_id:
            topic.delete()
        else:
            try:
                topic.last_post = Post.objects.filter(topic__id=topic.id).latest()
            except Post.DoesNotExist:
                topic.last_post = None
            topic.post_count = Post.objects.filter(topic__id=topic.id).count()
            topic.save()
        try:
            forum.last_post = Post.objects.filter(topic__forum__id=forum.id).latest()
        except Post.DoesNotExist:
            forum.last_post = None
        # TODO: for speedup - save/update only changed fields
        forum.post_count = Post.objects.filter(topic__forum__id=forum.id).count()
        forum.topic_count = Topic.objects.filter(forum__id=forum.id).count()
        forum.save()
        profile.post_count = Post.objects.filter(user__id=self.user_id).count()
        profile.save()

    def get_absolute_url(self):
        return reverse('djangobb:post', args=[self.id])

    def summary(self):
        LIMIT = 50
        tail = len(self.body) > LIMIT and '...' or ''
        return self.body[:LIMIT] + tail

    __str__ = summary
