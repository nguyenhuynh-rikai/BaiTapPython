from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse
from app.models import Clinic, Doctor, Patient, Drug, Appointment, TimeSlot, WorkSchedule
from datetime import time, date, timedelta
import uuid

User = get_user_model()

class AuthTests(APITestCase):
    def test_register_patient(self):
        url = reverse('auth-register')
        data = {
            "email": "newuser@example.com",
            "password": "Password123!",
            "password_confirm": "Password123!",
            "full_name": "New User",
            "role": "patient",
            "phone": "0123456789"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="newuser@example.com").exists())
        self.assertTrue(Patient.objects.filter(user__email="newuser@example.com").exists())

    def test_login(self):
        user = User.objects.create_user(email="test@example.com", password="Password123!", full_name="Test User")
        url = reverse('auth-login')
        data = {"email": "test@example.com", "password": "Password123!"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

class ClinicAndDoctorTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="admin@example.com", password="Password123!", full_name="Admin")
        self.clinic = Clinic.objects.create(
            name="Test Clinic", address="123 Street", phone="123", open_time=time(8, 0), close_time=time(17, 0)
        )
        self.doctor_user = User.objects.create_user(email="doc@example.com", password="pw", full_name="Doc", role="doctor")
        self.doctor = Doctor.objects.create(user=self.doctor_user, clinic=self.clinic, specialty="general", license_number="12345")

    def test_list_clinics(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('clinic-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_clinic_admin(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('clinic-list')
        data = {
            "name": "New Clinic",
            "address": "456 Ave",
            "phone": "987654",
            "open_time": "07:00",
            "close_time": "18:00"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_doctors(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('doctor-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

class DrugTests(APITestCase):
    def setUp(self):
        self.drug = Drug.objects.create(name="Paracetamol", unit="viên")
    
    def test_list_drugs(self):
        self.admin = User.objects.create_superuser(email="admin@example.com", password="Password123!", full_name="Admin")
        self.client.force_authenticate(user=self.admin)
        url = reverse('drug-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AppointmentTests(APITestCase):
    def setUp(self):
        self.patient_user = User.objects.create_user(email="pat@ex.com", password="pw", full_name="Pat", role="patient")
        self.patient = Patient.objects.create(user=self.patient_user)
        
        self.doctor_user = User.objects.create_user(email="doc2@ex.com", password="pw", full_name="Doc", role="doctor")
        self.clinic = Clinic.objects.create(name="C", address="A", phone="1", open_time=time(8,0), close_time=time(17,0))
        self.doctor = Doctor.objects.create(user=self.doctor_user, clinic=self.clinic, license_number="L1")
        
        self.schedule = WorkSchedule.objects.create(
            doctor=self.doctor, weekday=date.today().weekday(), start_time=time(8,0), end_time=time(12,0)
        )
        self.slot = TimeSlot.objects.create(
            schedule=self.schedule, slot_date=date.today(), start_time=time(8,0), end_time=time(8,30)
        )

    def test_create_appointment(self):
        self.client.force_authenticate(user=self.patient_user)
        url = reverse('appointment-list')
        data = {
            "doctor_id": str(self.doctor.id),
            "slot_id": str(self.slot.id),
            "symptoms": "Headache"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Appointment.objects.filter(patient=self.patient).exists())

    def test_get_available_slots(self):
        self.client.force_authenticate(user=self.patient_user)
        url = reverse('slots-available')
        response = self.client.get(url, {"doctor_id": str(self.doctor.id), "date": str(date.today())})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class AdditionalTests(APITestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(email="adm2@ex.com", password="pw", full_name="Ad")
        self.pat_user = User.objects.create_user(email="p2@ex.com", password="pw", role="patient", full_name="Pat")
        self.pat = Patient.objects.create(user=self.pat_user)
        self.doc_user = User.objects.create_user(email="d2@ex.com", password="pw", role="doctor", full_name="Doc")
        self.clinic = Clinic.objects.create(name="C2", address="A2", phone="2", open_time=time(8,0), close_time=time(17,0))
        self.doc = Doctor.objects.create(user=self.doc_user, clinic=self.clinic, license_number="L2")
        self.schedule = WorkSchedule.objects.create(
            doctor=self.doc, weekday=date.today().weekday(), start_time=time(8,0), end_time=time(12,0)
        )
        self.slot = TimeSlot.objects.create(
            schedule=self.schedule, slot_date=date.today(), start_time=time(8,0), end_time=time(8,30)
        )
        self.apt = Appointment.objects.create(patient=self.pat, doctor=self.doc, slot=self.slot)

    def test_patient_me(self):
        self.client.force_authenticate(user=self.pat_user)
        response = self.client.get(reverse("patient-me"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_change_password(self):
        self.client.force_authenticate(user=self.pat_user)
        response = self.client.post(reverse("auth-change-password"), {
            "old_password": "pw", "new_password": "NewPassword1!", "password_confirm": "NewPassword1!"
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_workload(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('doctor-workload', kwargs={'pk': self.doc.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_doctor_schedule(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('doctor-schedule', kwargs={'pk': self.doc.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_appointment_confirm(self):
        self.client.force_authenticate(user=self.admin)
        url = reverse('appointment-confirm', kwargs={'pk': self.apt.id})
        response = self.client.patch(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_appointment_medical_record(self):
        self.client.force_authenticate(user=self.doc_user)
        url = reverse('appointment-medical-record', kwargs={'pk': self.apt.id})
        data = {
            "diagnosis": "Sick",
            "treatment_plan": "Rest",
            "notes": "None"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
