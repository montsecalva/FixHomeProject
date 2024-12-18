from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("appointments", "0003_message"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="message_images/"),
        ),
    ]
