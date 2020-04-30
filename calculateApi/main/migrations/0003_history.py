# Generated by Django 3.0.5 on 2020-04-30 17:50

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_auto_20200430_0705'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('array', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\ \\d+)*\\Z'), code='invalid', message=None)])),
                ('calculations', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\ \\d+)*\\Z'), code='invalid', message=None)])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]