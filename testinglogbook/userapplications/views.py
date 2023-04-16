from django.shortcuts import render, get_object_or_404, redirect
from userapplications.forms import ReportForm, FlightEntryForm, MedicalForm, AccountDetailForm, CertificatesHeldForm, RatingsHeldForm
from userapplications.models import Flight, Medical, AccountDetail, CertificatesHeld, RatingsHeld
from django.contrib.auth.models import User
from django.db.models import Sum
from django.contrib import messages
from datetime import timedelta, datetime

# Create your views here.
def UserHomeView(request):
    return render(request, 'userhome.html')

def FlightEntryView(request):
    user=request.user
    flight_form = FlightEntryForm()
    pilot_in_command = AccountDetail.objects.filter(pilot = user).values('pilot_in_command')
    
    if pilot_in_command:
        pic = pilot_in_command[0]['pilot_in_command']
        
        if pic:
            pilotincommand = "pic"
        else:
            pilotincommand = "sic"
    else:
        pilotincommand = ''
    
    aircraft_type = AccountDetail.objects.filter(pilot=user).values('current_aircraft_type')
    if aircraft_type:
        aircraft = aircraft_type[0]['current_aircraft_type']
    else:
        aircraft = ''

    if request.method == "POST":
        flight_form = FlightEntryForm(request.POST)
        if flight_form.is_valid():
            print(flight_form.cleaned_data)
            obj=flight_form.save(commit=False)
            obj.pilot=request.user
            obj.save()
            messages.success(request, "Flight information saved")
            flight_form = FlightEntryForm()
        else:
            messages.warning(request, "Please make sure all fields are filled out")

    context = {
        "form": flight_form,
        "flyingtype" : aircraft,
        "pic" : pilotincommand
    }
    return render(request, 'flightentry.html', context)

def FlightDetailView(request, id=None):
    user = request.user
    flight = get_object_or_404(Flight,id=id)
    flight_update_form = FlightEntryForm(instance=flight)
    pilot_in_command = AccountDetail.objects.filter(pilot = user).values('pilot_in_command')

    if request.method == "POST":
        flight_update_form = FlightEntryForm(request.POST, instance=flight)
        if flight_update_form.is_valid():
            obj = flight_update_form.save(commit=False)
            obj.pilot = request.user
            if pilot_in_command:
                obj.pic_time = obj.total_time
            else:
                obj.sic_time = obj.total_time
            obj.save()
            

    context = {
        "flight": flight,
        "form": flight_update_form
    }

    return render(request, 'flightdetail.html', context)

def FlightDeleteView(request, id):
    flight = Flight.objects.get(id=id)

    if request.method == 'POST':
        flight.delete()
        messages.success(request, "Flight successfully deleted")
        return redirect('summary')

    context = {
        "flight" : flight
    }
    return render(request, 'flightdelete.html', context)

def SummaryView(request):
    user = request.user

    queryset = Flight.objects.filter(pilot = user).order_by('-flight_date')
    totaltime = Flight.objects.filter(pilot=user).aggregate(Sum('total_time'))['total_time__sum']
    if totaltime == None:
        totaltime = 0
    else:
        totaltime = round(totaltime, 1)
    night = Flight.objects.filter(pilot=user).aggregate(Sum('night_time'))['night_time__sum']
    if night == None:
        night = 0
    else:
        night = round(night, 1)
    vfr = Flight.objects.filter(pilot=user).aggregate(Sum('vfr_time'))['vfr_time__sum']
    if vfr == None:
        vfr = 0
    else:
        vfr = round(vfr, 1)
    ifr = Flight.objects.filter(pilot=user).aggregate(Sum('ifr_time'))['ifr_time__sum']
    if ifr == None:
        ifr = 0
    else:
        ifr = round(ifr, 1)
    multi = Flight.objects.filter(pilot=user).aggregate(Sum('multi_engine_time'))['multi_engine_time__sum']
    if multi == None:
        multi = 0
    else:
        multi = round(multi, 1)
    single = Flight.objects.filter(pilot=user).aggregate(Sum('single_engine_time'))['single_engine_time__sum']
    if single == None:
        single = 0
    else:
        single = round(single, 1)
    pic_time = Flight.objects.filter(pilot=user).aggregate(Sum('pic_time'))['pic_time__sum']
    if pic_time == None:
        pic_time = 0
    else:
        pic_time = round(pic_time, 1)
    sic_time = Flight.objects.filter(pilot=user).aggregate(Sum('sic_time'))['sic_time__sum']
    if sic_time == None:
        sic_time = 0
    else:
        sic_time = round(sic_time, 1)

    context={
        "data" : queryset,
        "total_time" : totaltime,
        "night_time" : night,
        "vfr_time" : vfr,
        "ifr_time" : ifr,
        "multi_time" : multi,
        "single_time" : single,
        "pic_time": pic_time,
        "sic_time": sic_time
    }
    
    return render(request, 'summary.html', context)

def AccountDetailView(request):
    user = request.user
    
    queryset = AccountDetail.objects.filter(pilot = user).first()
    
    try:
        certificates = CertificatesHeld.objects.filter(pilot = user).first()
    except CertificatesHeld.DoesNotExist:
        certificates = None
    try:
        ratings = RatingsHeld.objects.filter(pilot = user).first()
    except RatingsHeld.DoesNotExist:
        ratings = None

    if ratings == None:
        ratings_held_form = RatingsHeldForm()
    else:
        ratings_data = RatingsHeld.objects.get(pilot=user)
        ratings_held_form = RatingsHeldForm(instance=ratings_data)

    if certificates == None:
        certificates_held_form = CertificatesHeldForm()
    else:
        certificates_data = CertificatesHeld.objects.get(pilot = user)
        certificates_held_form = CertificatesHeldForm(instance=certificates_data)

    if queryset == None:
        account_detail_form = AccountDetailForm()

    else:
        account_detail = AccountDetail.objects.get(pilot = user)
        account_detail_form = AccountDetailForm(instance=account_detail)


    if request.method == "POST":
        account_detail_form = AccountDetailForm(request.POST)
        if account_detail_form.is_valid():
            obj = account_detail_form.save(commit=False)
            obj.pilot = user
            obj.save()

    context = {
        "form": account_detail_form,
        "account_detail_data" : queryset,
        "certificates_form" : certificates_held_form,
        "ratings_form" : ratings_held_form
    }        
    return render(request, 'accountdetail.html', context)

def CertificatesHeldView(request):
    user = request.user
    if request.method == "POST":
        certificates_form = CertificatesHeldForm(request.POST)
        if certificates_form.is_valid():
            obj = certificates_form.save(commit=False)
            obj.pilot = user
            obj.save()
            return redirect('accountdetail')
        
def RatingsHeldView(request):
    user = request.user
    if request.method == "POST":
        ratings_form = RatingsHeldForm(request.POST)
        if ratings_form.is_valid():
            obj = ratings_form.save(commit=False)
            obj.pilot = user
            obj.save()
            return redirect('accountdetail')

def MedicalView(request):
    user = request.user
    medical_form = MedicalForm()
    if request.method == "POST":
        medical_form = MedicalForm(request.POST)
        if medical_form.is_valid():
            print(medical_form.cleaned_data)
            obj=medical_form.save(commit=False)
            obj.pilot=request.user
            obj.save()
            medical_form = MedicalForm()
    try:
        queryset = Medical.objects.filter(pilot = user).latest()
    except Medical.DoesNotExist:
        queryset = None

    history = Medical.objects.filter(pilot = user)
    pilot_age = AccountDetail.objects.filter(pilot = user).values('age')
    flying_type = AccountDetail.objects.filter(pilot = user).values('faa_part_type')


    if queryset and pilot_age:
        next_medical_due = CalculateMedicalDue(queryset, pilot_age, flying_type)
    else:
        next_medical_due = None



    context = {
        "form": medical_form,
        "data": queryset,
        "history": history,
        "medical_due" : next_medical_due
    }

    return render(request, 'medical.html', context)

def ReportsView(request):
    form = ReportForm
    context={
        'form' : form
    }
    return render(request, 'reports.html', context)

def CalculateMedicalDue(queryset, pilot_age, flying_type):
    medical_class = queryset.medical_class
    medical_date = queryset.medical_date
    age = pilot_age[0]['age']
    type = flying_type[0]['faa_part_type']

    if medical_class == 1:
        if age < 40:
            if type == 121:
                months = 12
            else:
                months = 60
        else:
            if type == 121:
                months = 6
            else: months = 24
    else:
        if age < 40:
            months = 60
        else:
            months = 24
    month_lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30 ,31]
    new_date = medical_date + timedelta(days = months*30.5)
    exp_month = new_date.month
    if exp_month == medical_date.month:
        exp_month += 1
    exp_year = new_date.year
    exp_day = month_lengths[exp_month - 1]
    print(exp_month, exp_day)

    return datetime(exp_year, exp_month, exp_day)
    


