# Generated by Django 4.1 on 2022-08-20 22:00

from django.db import migrations, models
import django.db.models.deletion
import djbb.core.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('position', models.IntegerField(blank=True, default=0, verbose_name='Position')),
                ('description', models.TextField(blank=True, default='', verbose_name='Description')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('post_count', models.IntegerField(blank=True, default=0, verbose_name='Post count')),
                ('topic_count', models.IntegerField(blank=True, default=0, verbose_name='Topic count')),
                ('forum_logo', djbb.core.fields.ExtendedImageField(blank=True, default='', upload_to='djbb/forum_logo', verbose_name='Forum Logo')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forums', to='categories.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
                'ordering': ['position'],
            },
        ),
    ]
