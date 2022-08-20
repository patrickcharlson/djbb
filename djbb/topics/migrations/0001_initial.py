# Generated by Django 4.1 on 2022-08-20 22:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('forum', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Subject')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('updated', models.DateTimeField(null=True, verbose_name='Updated')),
                ('views', models.IntegerField(blank=True, default=0, verbose_name='Views count')),
                ('sticky', models.BooleanField(blank=True, default=False, verbose_name='Sticky')),
                ('closed', models.BooleanField(blank=True, default=False, verbose_name='Closed')),
                ('post_count', models.IntegerField(blank=True, default=0, verbose_name='Post count')),
                ('forum', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topics', to='forum.forum', verbose_name='Forum')),
                ('last_post', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='last_topic_post', to='posts.post')),
                ('subscribers', models.ManyToManyField(blank=True, related_name='subscriptions', to=settings.AUTH_USER_MODEL, verbose_name='Subscribers')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'ordering': ['-updated'],
                'get_latest_by': 'updated',
            },
        ),
    ]