from django.contrib import admin

from .models import User, Doctor, Clinic, Patient, WorkSchedule, TimeSlot, Appointment, MedicalRecord, Drug, \
    Prescription, PrescriptionItem, Payment

admin.site.register(User)
admin.site.register(Doctor)
admin.site.register(Clinic)
admin.site.register(Patient)
admin.site.register(WorkSchedule)
admin.site.register(TimeSlot)
admin.site.register(Appointment)
admin.site.register(MedicalRecord)
admin.site.register(Drug)
admin.site.register(Prescription)
admin.site.register(PrescriptionItem)
admin.site.register(Payment)