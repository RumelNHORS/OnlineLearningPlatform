# Generated by Django 4.2.13 on 2024-07-01 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_is_student_alter_profile_is_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_student',
        ),
    ]
