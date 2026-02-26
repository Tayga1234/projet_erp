{
    'name': 'Gestion de Consultation Médicale',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Module pour la gestion des consultations médicales',
    'description': '''
        Module de gestion de consultation médicale pour les cabinets médicaux.
        Fonctionnalités :
        - Gestion des patients
        - Gestion des médecins
        - Prise de rendez-vous
        - Consultations médicales
        - Prescriptions médicales
    ''',
    'author': 'korogo ange',
    'website': 'https://projet-erp.com',
    'license': 'LGPL-3',
    'depends': ['base', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/patient_views.xml',
        'views/medecin_views.xml',
        'views/consultation_views.xml',
        'views/prescription_views.xml',
        'views/rendezvous_views.xml',
        'views/medical_menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}