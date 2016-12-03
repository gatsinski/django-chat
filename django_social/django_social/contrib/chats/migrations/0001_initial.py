# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(max_length=1, choices=[('s', 'system'), ('a', 'action'), ('m', 'message'), ('f', 'file'), ('j', 'join'), ('l', 'leave'), ('n', 'notification')])),
                ('message', models.CharField(max_length=255, blank=True)),
                ('file', models.FileField(blank=True, upload_to='uploads/')),
                ('date', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(related_name='author', null=True, to=settings.AUTH_USER_MODEL, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='message',
            name='room',
            field=models.ForeignKey(to='chats.Room'),
        ),
    ]
