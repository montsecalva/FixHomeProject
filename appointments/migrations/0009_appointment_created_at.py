import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0008_appointment_admin_alter_appointment_status_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
