# Generated by Django 5.1.6 on 2025-02-18 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_date_joined_alter_user_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_joined',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
