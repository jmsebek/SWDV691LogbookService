from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Flight(models.Model):
    pilot = models.ForeignKey(User, on_delete=models.CASCADE)
    flight_date = models.DateField()
    origin = models.CharField(max_length=3)
    destination = models.CharField(max_length=3)
    tail_number = models.IntegerField()
    total_time = models.FloatField()
    landings = models.IntegerField()
    multi_engine_time = models.FloatField()
    single_engine_time = models.FloatField()
    vfr_time = models.FloatField()
    ifr_time = models.FloatField()
    night_time = models.FloatField()
    pic_time = models.FloatField(default = 0)
    sic_time = models.FloatField(default = 0)
    notes = models.TextField()

class Medical(models.Model):
    pilot = models.ForeignKey(User, on_delete=models.CASCADE)
    medical_class = models.IntegerField()
    medical_date = models.DateField()
    examiner_name = models.CharField(max_length=50)
    examiner_phone = models.CharField(max_length=20)
    notes = models.TextField()
    class Meta:
        get_latest_by = "medical_date"

class AccountDetail(models.Model):
    pilot = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    pilot_in_command = models.BooleanField()
    current_aircraft_type = models.CharField(max_length=20)
    faa_part_type = models.IntegerField()

class CertificatesHeld(models.Model):
    pilot = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    student = models.BooleanField()
    sport = models.BooleanField()
    recreational = models.BooleanField()
    private_pilot = models.BooleanField()
    csel = models.BooleanField()
    cmel = models.BooleanField()
    atp = models.BooleanField()
    cfi = models.BooleanField()

class RatingsHeld(models.Model):
    pilot = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    instrument = models.BooleanField()
    multi_engine = models.BooleanField()
