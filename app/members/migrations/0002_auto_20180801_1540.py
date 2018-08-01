# Generated by Django 2.0.7 on 2018-08-01 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('members', '0001_initial'),
        ('posts', '0001_initial'),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='likes_posts',
            field=models.ManyToManyField(blank=True, related_name='like_posts', related_query_name='like_posts', to='posts.Post'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
