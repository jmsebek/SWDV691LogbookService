# Generated by Django 4.1.7 on 2023-04-12 00:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_date', models.DateField()),
                ('origin', models.CharField(max_length=3)),
                ('destination', models.CharField(max_length=3)),
                ('tail_number', models.IntegerField()),
                ('total_time', models.FloatField()),
                ('landings', models.IntegerField()),
                ('multi_engine_time', models.FloatField()),
                ('single_engine_time', models.FloatField()),
                ('vfr_time', models.FloatField()),
                ('ifr_time', models.FloatField()),
                ('night_time', models.FloatField()),
                ('notes', models.TextField()),
                ('pilot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
