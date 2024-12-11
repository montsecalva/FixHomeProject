import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('repair_type', models.CharField(choices=[('plumbing', 'Plumbing'), ('electricity', 'Electricity'), ('carpentry', 'Carpentry'), ('other', 'Other')], max_length=20)),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rescheduled', 'Rescheduled')], default='pending', max_length=15)),
                ('assigned_professional', models.CharField(blank=True, max_length=50, null=True)),
                ('tenant', models.ForeignKey(limit_choices_to={'role': 'tenant'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
