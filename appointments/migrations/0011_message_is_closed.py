# Generated by Django 5.1.3 on 2024-12-22 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0010_message_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="is_closed",
            field=models.BooleanField(default=False),
        ),
    ]