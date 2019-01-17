# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2019-01-15 09:54
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_auto_20190104_2140'),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionAnswer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('status', models.BooleanField(default=0)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='courses.Module')),
                ('student', models.ForeignKey(default='-1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions_asked', to='courses.Student')),
                ('teacher', models.ForeignKey(default='-1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='questions_answerd', to='courses.Teacher')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='approved',
            field=models.ForeignKey(default='-1', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='courses_approved', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='discount',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='course',
            name='updated',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2019, 1, 15, 9, 54, 56, 973493, tzinfo=utc)),
            preserve_default=False,
        ),
    ]