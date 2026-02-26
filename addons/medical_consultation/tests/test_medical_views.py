from odoo.tests.common import TransactionCase, tagged
from odoo.tests import Form


@tagged('-at_install', 'post_install')
class TestMedicalViews(TransactionCase):
    """Test suite for medical module views and actions"""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.patient = self.env['medical.patient'].create({
            'name': 'Test Patient',
            'prenoms': 'John',
            'date_naissance': '1990-01-01',
            'groupe_sanguin': 'A+',
        })
        
        self.doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Test',
            'prenoms': 'Smith',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
    
    def test_patient_tree_view(self):
        """Test patient tree view"""
        # Test the tree view loads correctly
        tree_view = self.env.ref('medical_consultation.view_medical_patient_tree')
        self.assertEqual(tree_view.model, 'medical.patient')
        self.assertEqual(tree_view.type, 'tree')
    
    def test_patient_form_view(self):
        """Test patient form view"""
        # Test the form view loads correctly
        form_view = self.env.ref('medical_consultation.view_medical_patient_form')
        self.assertEqual(form_view.model, 'medical.patient')
        self.assertEqual(form_view.type, 'form')
    
    def test_patient_kanban_view(self):
        """Test patient kanban view"""
        # Test the kanban view loads correctly
        kanban_view = self.env.ref('medical_consultation.view_medical_patient_kanban')
        self.assertEqual(kanban_view.model, 'medical.patient')
        self.assertEqual(kanban_view.type, 'kanban')
    
    def test_patient_action(self):
        """Test patient action window"""
        # Test the patient action
        action = self.env.ref('medical_consultation.action_medical_patient')
        self.assertEqual(action.res_model, 'medical.patient')
        self.assertIn('tree', action.view_mode)
        self.assertIn('form', action.view_mode)
        self.assertIn('kanban', action.view_mode)
        self.assertIn('graph', action.view_mode)
        self.assertIn('pivot', action.view_mode)
    
    def test_doctor_views(self):
        """Test doctor views"""
        # Test doctor tree view
        tree_view = self.env.ref('medical_consultation.view_medical_medecin_tree')
        self.assertEqual(tree_view.model, 'medical.medecin')
        
        # Test doctor form view
        form_view = self.env.ref('medical_consultation.view_medical_medecin_form')
        self.assertEqual(form_view.model, 'medical.medecin')
        
        # Test doctor action
        action = self.env.ref('medical_consultation.action_medical_medecin')
        self.assertEqual(action.res_model, 'medical.medecin')
    
    def test_appointment_views(self):
        """Test appointment views"""
        # Test appointment tree view
        tree_view = self.env.ref('medical_consultation.view_medical_rendezvous_tree')
        self.assertEqual(tree_view.model, 'medical.rendezvous')
        
        # Test appointment form view
        form_view = self.env.ref('medical_consultation.view_medical_rendezvous_form')
        self.assertEqual(form_view.model, 'medical.rendezvous')
        
        # Test appointment action
        action = self.env.ref('medical_consultation.action_medical_rendezvous')
        self.assertEqual(action.res_model, 'medical.rendezvous')
    
    def test_consultation_views(self):
        """Test consultation views"""
        # Test consultation tree view
        tree_view = self.env.ref('medical_consultation.view_medical_consultation_tree')
        self.assertEqual(tree_view.model, 'medical.consultation')
        
        # Test consultation form view
        form_view = self.env.ref('medical_consultation.view_medical_consultation_form')
        self.assertEqual(form_view.model, 'medical.consultation')
        
        # Test consultation action
        action = self.env.ref('medical_consultation.action_medical_consultation')
        self.assertEqual(action.res_model, 'medical.consultation')
    
    def test_prescription_views(self):
        """Test prescription views"""
        # Test prescription tree view
        tree_view = self.env.ref('medical_consultation.view_medical_prescription_tree')
        self.assertEqual(tree_view.model, 'medical.prescription')
        
        # Test prescription form view
        form_view = self.env.ref('medical_consultation.view_medical_prescription_form')
        self.assertEqual(form_view.model, 'medical.prescription')
        
        # Test prescription action
        action = self.env.ref('medical_consultation.action_medical_prescription')
        self.assertEqual(action.res_model, 'medical.prescription')
    
    def test_patient_form_creation(self):
        """Test creating patient through form view"""
        # Create patient using Form API
        patient_form = Form(self.env['medical.patient'])
        patient_form.name = 'Form Test Patient'
        patient_form.prenoms = 'Jane'
        patient_form.date_naissance = '1995-05-15'
        patient_form.groupe_sanguin = 'B+'
        
        patient = patient_form.save()
        
        self.assertEqual(patient.name, 'Form Test Patient')
        self.assertEqual(patient.prenoms, 'Jane')
        self.assertEqual(patient.groupe_sanguin, 'B+')
    
    def test_appointment_form_creation(self):
        """Test creating appointment through form view"""
        # Create appointment using Form API
        appointment_form = Form(self.env['medical.rendezvous'])
        appointment_form.patient_id = self.patient
        appointment_form.medecin_id = self.doctor
        appointment_form.date_heure = '2026-12-20 10:00:00'
        appointment_form.duree = 45
        appointment_form.motif = 'Form Test Appointment'
        
        appointment = appointment_form.save()
        
        self.assertEqual(appointment.patient_id, self.patient)
        self.assertEqual(appointment.medecin_id, self.doctor)
        self.assertEqual(appointment.motif, 'Form Test Appointment')
        self.assertEqual(appointment.duree, 45)
    
    def test_menu_structure(self):
        """Test menu structure"""
        # Test main menu
        main_menu = self.env.ref('medical_consultation.medical_root')
        self.assertEqual(main_menu.name, 'Médical')
        
        # Test patient menu
        patient_menu = self.env.ref('medical_consultation.medical_patient_menu')
        self.assertEqual(patient_menu.name, 'Patients')
        self.assertEqual(patient_menu.parent_id, main_menu)
        
        # Test doctor menu
        doctor_menu = self.env.ref('medical_consultation.medical_medecin_menu')
        self.assertEqual(doctor_menu.name, 'Médecins')
        self.assertEqual(doctor_menu.parent_id, main_menu)
        
        # Test appointment menu
        appointment_menu = self.env.ref('medical_consultation.medical_rendezvous_menu')
        self.assertEqual(appointment_menu.name, 'Rendez-vous')
        self.assertEqual(appointment_menu.parent_id, main_menu)


@tagged('-at_install', 'post_install')
class TestMedicalSecurity(TransactionCase):
    """Test suite for medical module security and access rights"""
    
    def setUp(self):
        super().setUp()
        # Create test users
        self.user_medical = self.env['res.users'].create({
            'name': 'Medical User',
            'login': 'medical_user',
            'password': 'medical_password',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        
        self.user_admin = self.env['res.users'].create({
            'name': 'Admin User',
            'login': 'admin_user',
            'password': 'admin_password',
            'groups_id': [(6, 0, [self.env.ref('base.group_user').id])]
        })
        
        # Create test data as admin
        self.patient = self.env['medical.patient'].sudo().create({
            'name': 'Test Patient',
            'date_naissance': '1990-01-01',
        })
    
    def test_patient_access_rights(self):
        """Test patient model access rights"""
        # Test that regular users can read patients
        patients = self.env['medical.patient'].sudo(self.user_medical).search([])
        self.assertTrue(len(patients) > 0)
        
        # Test that regular users can create patients
        patient = self.env['medical.patient'].sudo(self.user_medical).create({
            'name': 'Security Test Patient',
            'date_naissance': '1995-01-01',
        })
        self.assertTrue(patient.exists())
        
        # Test that regular users can write to patients
        patient.sudo(self.user_medical).write({'prenoms': 'Security'})
        self.assertEqual(patient.prenoms, 'Security')
    
    def test_doctor_access_rights(self):
        """Test doctor model access rights"""
        # Test that regular users can read doctors
        doctors = self.env['medical.medecin'].sudo(self.user_medical).search([])
        self.assertTrue(len(doctors) >= 0)
        
        # Test that regular users can create doctors
        doctor = self.env['medical.medecin'].sudo(self.user_medical).create({
            'name': 'Dr. Security Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
        self.assertTrue(doctor.exists())
    
    def test_appointment_access_rights(self):
        """Test appointment model access rights"""
        # Create a doctor for testing
        doctor = self.env['medical.medecin'].sudo().create({
            'name': 'Dr. Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
        
        # Test that regular users can create appointments
        appointment = self.env['medical.rendezvous'].sudo(self.user_medical).create({
            'patient_id': self.patient.id,
            'medecin_id': doctor.id,
            'date_heure': '2024-12-20 10:00:00',
            'motif': 'Security Test',
        })
        self.assertTrue(appointment.exists())
    
    def test_consultation_access_rights(self):
        """Test consultation model access rights"""
        # Create doctor and appointment for testing
        doctor = self.env['medical.medecin'].sudo().create({
            'name': 'Dr. Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
        
        appointment = self.env['medical.rendezvous'].sudo().create({
            'patient_id': self.patient.id,
            'medecin_id': doctor.id,
            'date_heure': '2024-12-20 10:00:00',
            'motif': 'Test',
        })
        
        # Test that regular users can create consultations
        consultation = self.env['medical.consultation'].sudo(self.user_medical).create({
            'patient_id': self.patient.id,
            'medecin_id': doctor.id,
            'date_consultation': '2024-12-20 10:00:00',
            'motif': 'Security Test',
        })
        self.assertTrue(consultation.exists())
    
    def test_prescription_access_rights(self):
        """Test prescription model access rights"""
        # Create consultation for testing
        doctor = self.env['medical.medecin'].sudo().create({
            'name': 'Dr. Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
        
        consultation = self.env['medical.consultation'].sudo().create({
            'patient_id': self.patient.id,
            'medecin_id': doctor.id,
            'date_consultation': '2024-12-20 10:00:00',
        })
        
        # Test that regular users can create prescriptions
        prescription = self.env['medical.prescription'].sudo(self.user_medical).create({
            'consultation_id': consultation.id,
            'medicament': 'Security Test Medicament',
            'dosage': '500mg',
            'frequence': '1 fois par jour',
            'duree_traitement': '3 jours',
        })
        self.assertTrue(prescription.exists())


@tagged('-at_install', 'post_install')
class TestMedicalPerformance(TransactionCase):
    """Test suite for medical module performance"""
    
    def setUp(self):
        super().setUp()
        # Create test data
        self.doctor = self.env['medical.medecin'].create({
            'name': 'Dr. Performance Test',
            'specialite': 'generaliste',
            'tarif_consultation': 5000,
        })
    
    def test_patient_creation_performance(self):
        """Test performance of patient creation"""
        import time
        
        # Create multiple patients and measure time
        start_time = time.time()
        
        for i in range(10):
            self.env['medical.patient'].create({
                'name': f'Performance Test Patient {i}',
                'date_naissance': '1990-01-01',
                'groupe_sanguin': 'A+',
            })
        
        end_time = time.time()
        creation_time = end_time - start_time
        
        # Should complete within reasonable time (5 seconds for 10 records)
        self.assertLess(creation_time, 5.0)
    
    def test_patient_search_performance(self):
        """Test performance of patient search"""
        # Create test data
        for i in range(20):
            self.env['medical.patient'].create({
                'name': f'Search Test Patient {i}',
                'date_naissance': '1990-01-01',
                'groupe_sanguin': 'A+',
            })
        
        import time
        start_time = time.time()
        
        # Search patients
        patients = self.env['medical.patient'].search([('groupe_sanguin', '=', 'A+')])
        
        end_time = time.time()
        search_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(search_time, 1.0)
        self.assertGreaterEqual(len(patients), 20)
    
    def test_appointment_workflow_performance(self):
        """Test performance of appointment workflow"""
        # Create test patient
        patient = self.env['medical.patient'].create({
            'name': 'Workflow Test Patient',
            'date_naissance': '1990-01-01',
        })
        
        import time
        start_time = time.time()
        
        # Create and process multiple appointments
        for i in range(5):
            appointment = self.env['medical.rendezvous'].create({
                'patient_id': patient.id,
                'medecin_id': self.doctor.id,
                'date_heure': '2024-12-20 10:00:00',
                'motif': f'Performance Test {i}',
            })
            
            # Process workflow
            appointment.action_confirm()
            appointment.action_start()
            if appointment.consultation_id:
                appointment.consultation_id.action_finish()
            appointment.action_finish()
        
        end_time = time.time()
        workflow_time = end_time - start_time
        
        # Should complete within reasonable time
        self.assertLess(workflow_time, 3.0)
