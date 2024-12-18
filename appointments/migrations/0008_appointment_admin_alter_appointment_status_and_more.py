import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0007_message_creator_message_recipient_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="admin",
            field=models.ForeignKey(
                limit_choices_to={"role": "admin"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="admin_appointments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="status",
            field=models.CharField(
                choices=[
                    ("pending", "Pending"),
                    ("accepted", "Accepted"),
                    ("rejected", "Rejected"),
                ],
                default="pending",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="appointment",
            name="tenant",
            field=models.ForeignKey(
                limit_choices_to={"role": "tenant"},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tenant_appointments",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="creator",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="created_messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="message",
            name="recipient",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="received_messages",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
