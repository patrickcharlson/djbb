# Generated by Django 4.1 on 2022-08-21 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_reputation'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'get_latest_by': 'date_joined', 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
    ]