from django import forms
from .models import Flight, Medical, AccountDetail, CertificatesHeld, RatingsHeld

class ReportForm(forms.Form):
    report_choice = forms.ChoiceField(choices=(("totalTime", "Total Time"),("progress", "Progress")),widget=forms.RadioSelect(), required=True)
    #report_choice.widget.attrs.update({'class':'form-check-input'})

class DateInput(forms.DateInput):
    input_type = 'date'

class FlightEntryForm(forms.ModelForm):
    flight_date = forms.DateField(widget=DateInput)
    origin = forms.CharField(max_length=3, help_text="Enter Origin Airport ID")
    destination = forms.CharField(max_length=3, help_text="Enter Destination Airport ID")
    tail_number = forms.IntegerField(label="Tail Number: N", min_value=0, max_value=999)
    total_time = forms.FloatField(help_text="Enter total flight time.", min_value=0)
    landings = forms.IntegerField(min_value=0, max_value=1, initial=0)
    multi_engine_time = forms.FloatField(min_value=0)
    single_engine_time = forms.FloatField(min_value=0)
    vfr_time = forms.FloatField(min_value=0, help_text="Enter total VFR time", initial=0)
    ifr_time = forms.FloatField(min_value=0, help_text="Enter total IFR time", initial=0)
    night_time = forms.FloatField(min_value=0, help_text="Enter total night time", initial=0)
    pic_time = forms.FloatField(label="PIC time", min_value= 0, initial=0)
    sic_time = forms.FloatField(label="SIC time", min_value= 0, initial=0)
    notes = forms.CharField(max_length=250, initial="None")

    class Meta:
        model = Flight
        fields = [
            "flight_date",
            "origin",
            "destination",
            "tail_number",
            "total_time",
            "landings",
            "multi_engine_time",
            "single_engine_time",
            "vfr_time",
            "ifr_time",
            "night_time",
            "pic_time",
            "sic_time",
            "notes" ]
        
class MedicalForm(forms.ModelForm):
    medical_class = forms.ChoiceField(choices=(("1", "First Class"),("2", "Second Class"), ("3", "Third Class")),widget=forms.RadioSelect(), required=True)
    medical_date = forms.DateField(widget=DateInput)
    examiner_name = forms.CharField(max_length=50)
    examiner_phone = forms.CharField(max_length=20)
    notes = forms.CharField()
    class Meta:
        model = Medical
        
        fields = [
            "medical_class",
            "medical_date",
            "examiner_name",
            "examiner_phone",
            "notes"
        ]

class AccountDetailForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    age = forms.IntegerField(min_value=0)
    pilot_in_command = forms.ChoiceField(choices=(("True", "PIC"),("False", "SIC")),widget=forms.RadioSelect(), required=True)
    current_aircraft_type = forms.ChoiceField(choices=(("multi", "Multi-Engine"),("single", "Single-Engine")),widget=forms.RadioSelect(), required=True)
    faa_part_type = forms.ChoiceField(label="FAA Part Type", choices=(("135", "Part 135"),("121", "Part 121")),widget=forms.RadioSelect(), required=True)

    class Meta:
        model = AccountDetail

        fields = [
            "first_name",
            "last_name",
            "age",
            "pilot_in_command",
            "current_aircraft_type",
            "faa_part_type"
        ]

class CertificatesHeldForm(forms.ModelForm):
    student = forms.BooleanField(required=False)
    sport = forms.BooleanField(required=False)
    recreational = forms.BooleanField(required=False)
    private_pilot = forms.BooleanField(required=False)
    csel = forms.BooleanField(label="CSEL", required=False)
    cmel = forms.BooleanField(label="CMEL", required=False)
    atp = forms.BooleanField(label="ATP", required=False)
    cfi = forms.BooleanField(label="CFI", required=False)

    class Meta:
        model = CertificatesHeld

        fields = [
            "student",
            "sport",
            "recreational",
            "private_pilot",
            "csel",
            "cmel",
            "atp",
            "cfi"
        ]

class RatingsHeldForm(forms.ModelForm):
    instrument = forms.BooleanField(required=False)
    multi_engine = forms.BooleanField(required=False)

    class Meta:
        model = RatingsHeld

        fields = [
            "instrument",
            "multi_engine"
        ]