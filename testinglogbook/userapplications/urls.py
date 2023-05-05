from django.urls import path
from .views import UserHomeView, FlightEntryView, SummaryView, AccountDetailView, ReportsView, MedicalView, FlightDetailView, FlightDeleteView, CertificatesHeldView, RatingsHeldView, MedicalDeleteView, MedicalDetailView, logbook_print_view

urlpatterns = [
    path("", UserHomeView, name="userhome"),
    path("flightentry/", FlightEntryView, name="flightentry"),
    path("flightdetail/<id>/", FlightDetailView, name="flightdetail"),
    path("flights/<id>/delete/", FlightDeleteView, name="flightdelete"),
    path("medical/<id>/delete/", MedicalDeleteView, name="medicaldelete"),
    path("medicaldetail/<id>/", MedicalDetailView, name="medicaldetail"),
    path("summary/", SummaryView, name="summary"),
    path("accountdetail/", AccountDetailView, name="accountdetail"),
    path("medical/", MedicalView, name="medical"),
    path("reports/", ReportsView, name="reports"),
    path("certificates/", CertificatesHeldView, name="certificatesheld"),
    path("ratings/", RatingsHeldView, name="ratingsheld"),
    path("logbookprint/<number>/", logbook_print_view, name="logbookprint"),
]