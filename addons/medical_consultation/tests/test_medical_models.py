from odoo.tests.common import TransactionCase
from datetime import datetime, timedelta

class TestMedicalPatient(TransactionCase):
    """Test suite for the Medical Patient model"""
    
    def setUp(self):
        super().setUp()
        # Create a partner for testing
        self.partner = self.env['res.partner'].create({
            'name': 'Test Patient Partner',
            'email': 'test@example.com',
            'phone': '1234567890',
        })
        
        # Create a doctor for testing
        self.doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test Doctor',
            'prenoms': 'John',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
    
    def test_patient_creation(self):
        """Test creating a new patient"""
        patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
            'prenoms': 'John',
            'date_naissance': '1990-01-01',
            'groupe_sanguin': 'A+',
            'partner_id': self.partner.id,
            'medecin_traitant': self.doctor.id,
        })
        
        self.assertEqual(patient.name, 'Test Patient')
        self.assertEqual(patient.prenoms, 'John')
        self.assertEqual(patient.groupe_sanguin, 'A+')
        self.assertEqual(patient.age, 34)  # Assuming current year is 2024
        self.assertEqual(patient.partner_id, self.partner)
        self.assertEqual(patient.medecin_traitant, self.doctor)
    
    def test_patient_age_calculation(self):
        """Test age calculation from birth date"""
        # Test with different birth dates
        birth_dates = [
            ('2000-01-01', 24),
            ('1995-06-15', 29),
            ('1980-12-31', 44),
        ]
        
        for birth_date, expected_age in birth_dates:
            patient = self.env['medical.patient'].create({
                'name': f'Patient {birth_date}',
                'date_naissance': birth_date,
            })
            self.assertEqual(patient.age, expected_age)
    
    def test_patient_name_get(self):
        """Test the name_get method for patients"""
        patient = self.env['medical.patient'].create({
            'name': 'Test',
            'prenoms': 'John',
            'date_naissance': '1990-01-01',
        })
        
        name_display = patient.name_get()[0][1]
        self.assertIn('Test', name_display)
        self.assertIn('John', name_display)
    
    def test_patient_constraints(self):
        """Test patient model constraints"""
        # Test required fields
        with self.assertRaises(Exception):
            self.env['medical.patient'].create({
                'name': '',  # Empty name should fail
                'date_naissance': '1990-01-01',
            })
        
        with self.assertRaises(Exception):
            self.env['medical.patient'].create({
                'name': 'Test Patient',
                'date_naissance': '',  # Empty birth date should fail
            })
    
    def test_patient_group_sanguin_selection(self):
        """Test blood group selection values"""
        valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        
        for group in valid_groups:
            patient = self.env['medical.patient'].create({
                'name': f'Patient {group}',
                'date_naissance': '1990-01-01',
                'groupe_sanguin': group,
            })
            self.assertEqual(patient.groupe_sanguin, group)
    
    def test_patient_medical_history(self):
        """Test medical history fields"""
        patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
            'date_naissance': '1990-01-01',
            'antecedents': 'Diabetes, Hypertension',
            'allergies': 'Penicillin, Peanuts',
            'numero_secu': '123456789012345',
        })
        
        self.assertEqual(patient.antecedents, 'Diabetes, Hypertension')
        self.assertEqual(patient.allergies, 'Penicillin, Peanuts')
        self.assertEqual(patient.numero_secu, '123456789012345')


class TestMedicalMedecin(TransactionCase):
    """Test suite for the Medical Doctor model"""
    
    def test_doctor_creation(self):
        """Test creating a new doctor"""
        doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test',
            'prenoms': 'Smith',
            'specialite': 'cardiologue',
            'tarif_consultation': 10000,
        })
        
        self.assertEqual(doctor.name, 'Dr. Test')
        self.assertEqual(doctor.prenoms, 'Smith')
        self.assertEqual(doctor.specialite, 'cardiologue')
        self.assertEqual(doctor.tarif_consultation, 10000)
    
    def test_doctor_specialite_selection(self):
        """Test doctor specialty selection"""
        specialties = ['generaliste', 'cardiologue', 'pediatre', 'gynecologue', 'dermatologue']
        
        for specialite in specialties:
            doctor = self.env['medical.medecin'].create({
                'name': f'Dr. {specialite}',
                'specialite': specialite,
                'tarif_consultation': 5000,
            })
            self.assertEqual(doctor.specialite, specialite)
    
    def test_doctor_tarif_positive(self):
        """Test that consultation fee is positive"""
        doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test',
            'tarif_consultation': 7500,
        })
        
        self.assertGreater(doctor.tarif_consultation, 0)


class TestMedicalRendezvous(TransactionCase):
    """Test suite for the Medical Appointment model"""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
            'date_naissance': '1990-01-01',
        })
        
        self.doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
    
    def test_appointment_creation(self):
        """Test creating a new appointment"""
        appointment = self.env['medical.rendezvous'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_heure': '2024-12-15 14:00:00',
            'duree': 30,
            'motif': 'Consultation générale',
        })
        
        self.assertEqual(appointment.patient_id, self.patient)
        self.assertEqual(appointment.medecin_id, self.doctor)
        self.assertEqual(appointment.motif, 'Consultation générale')
        self.assertEqual(appointment.duree, 30)
        self.assertEqual(appointment.state, 'brouillon')
    
    def test_appointment_date_fin_calculation(self):
        """Test end date calculation"""
        appointment = self.env['medical.rendezvous'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_heure': '2024-12-15 14:00:00',
            'duree': 30,
            'motif': 'Test',
        })
        
        # End time should be start time + duration
        expected_end = appointment.date_heure + timedelta(minutes=30)
        self.assertEqual(appointment.date_fin, expected_end)
    
    def test_appointment_state_transitions(self):
        """Test appointment state transitions"""
        appointment = self.env['medical.rendezvous'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_heure': '2024-12-15 14:00:00',
            'motif': 'Test',
        })
        
        # Test state transitions
        appointment.action_confirm()
        self.assertEqual(appointment.state, 'confirme')
        
        appointment.action_start()
        self.assertEqual(appointment.state, 'en_cours')
        
        appointment.action_finish()
        self.assertEqual(appointment.state, 'termine')
        
        appointment.action_cancel()
        self.assertEqual(appointment.state, 'annule')
    
    def test_appointment_name_get(self):
        """Test appointment name_get method"""
        appointment = self.env['medical.rendezvous'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_heure': '2024-12-15 14:00:00',
            'motif': 'Test',
        })
        
        name_display = appointment.name_get()[0][1]
        self.assertIn('RDV', name_display)
        self.assertIn('Test Patient', name_display)
        self.assertIn('Dr. Test', name_display)


class TestMedicalConsultation(TransactionCase):
    """Test suite for the Medical Consultation model"""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
            'date_naissance': '1990-01-01',
        })
        
        self.doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
    
    def test_consultation_creation(self):
        """Test creating a new consultation"""
        consultation = self.env['medical.consultation'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_consultation': '2024-12-15 14:00:00',
            'motif': 'Consultation générale',
            'diagnostic': 'Patient en bonne santé',
            'traitement': 'Repos et hydratation',
        })
        
        self.assertEqual(consultation.patient_id, self.patient)
        self.assertEqual(consultation.medecin_id, self.doctor)
        self.assertEqual(consultation.motif, 'Consultation générale')
        self.assertEqual(consultation.diagnostic, 'Patient en bonne santé')
        self.assertEqual(consultation.state, 'brouillon')
    
    def test_consultation_state_transitions(self):
        """Test consultation state transitions"""
        consultation = self.env['medical.consultation'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_consultation': '2024-12-15 14:00:00',
            'motif': 'Test',
        })
        
        # Test state transitions
        consultation.action_start()
        self.assertEqual(consultation.state, 'en_cours')
        
        consultation.action_finish()
        self.assertEqual(consultation.state, 'termine')
        
        consultation.action_cancel()
        self.assertEqual(consultation.state, 'annule')


class TestMedicalPrescription(TransactionCase):
    """Test suite for the Medical Prescription model"""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
            'date_naissance': '1990-01-01',
        })
        
        self.doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
        
        self.consultation = self.env['medical.consultation'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_consultation': '2024-12-15 14:00:00',
        })
    
    def test_prescription_creation(self):
        """Test creating a new prescription"""
        prescription = self.env['medical.prescription'].create({
            'consultation_id': self.consultation.id,
            'medicament': 'Paracetamol',
            'dosage': '500mg',
            'frequence': '3 fois par jour',
            'duree_traitement': '5 jours',
            'instructions': 'Prendre après les repas',
        })
        
        self.assertEqual(prescription.consultation_id, self.consultation)
        self.assertEqual(prescription.medicament, 'Paracetamol')
        self.assertEqual(prescription.dosage, '500mg')
        self.assertEqual(prescription.frequence, '3 fois par jour')
        self.assertEqual(prescription.duree_traitement, '5 jours')
        self.assertEqual(prescription.instructions, 'Prendre après les repas')
    
    def test_prescription_required_fields(self):
        """Test required fields for prescription"""
        # Test that consultation_id is required
        with self.assertRaises(Exception):
            self.env['medical.prescription'].create({
                'medicament': 'Test',
            })
        
        # Test that medicament is required
        with self.assertRaises(Exception):
            self.env['medical.prescription'].create({
                'consultation_id': self.consultation.id,
            })


class TestMedicalWorkflow(TransactionCase):
    """Test suite for complete medical workflow"""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
            'date_naissance': '1990-01-01',
        })
        
        self.doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
    
    def test_complete_workflow(self):
        """Test complete patient workflow: appointment -> consultation -> prescription"""
        # Step 1: Create appointment
        appointment = self.env['medical.rendezvous'].create({
            'patient_id': self.patient.id,
            'medecin_id': self.doctor.id,
            'date_heure': '2024-12-15 14:00:00',
            'motif': 'Consultation générale',
        })
        
        # Step 2: Confirm appointment
        appointment.action_confirm()
        self.assertEqual(appointment.state, 'confirme')
        
        # Step 3: Start appointment (creates consultation)
        appointment.action_start()
        self.assertEqual(appointment.state, 'en_cours')
        self.assertTrue(appointment.consultation_id)
        
        # Step 4: Add prescription to consultation
        consultation = appointment.consultation_id
        prescription = self.env['medical.prescription'].create({
            'consultation_id': consultation.id,
            'medicament': 'Ibuprofen',
            'dosage': '400mg',
            'frequence': '2 fois par jour',
            'duree_traitement': '3 jours',
        })
        
        # Step 5: Finish consultation
        consultation.action_finish()
        self.assertEqual(consultation.state, 'termine')
        
        # Step 6: Finish appointment
        appointment.action_finish()
        self.assertEqual(appointment.state, 'termine')
        
        # Verify all records are linked correctly
        self.assertEqual(prescription.consultation_id, consultation)
        self.assertEqual(consultation.patient_id, self.patient)
        self.assertEqual(appointment.patient_id, self.patient)
        self.assertEqual(appointment.consultation_id, consultation)
