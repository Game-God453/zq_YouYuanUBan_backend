# Generated by Django 5.1.6 on 2025-02-24 17:08

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatConnection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_message_user1', models.BigIntegerField(default=0)),
                ('last_message_user2', models.BigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections_user1', to=settings.AUTH_USER_MODEL)),
                ('user2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='connections_user2', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user1', 'user2')},
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat_longpolling.chatconnection')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_messages', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_messages', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
