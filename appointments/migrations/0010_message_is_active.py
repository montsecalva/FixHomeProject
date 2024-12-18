from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0009_appointment_created_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
    ]