from odoo import models, fields, api

class MedicalPatient(models.Model):
    _name = 'medical.patient'
    _description = 'Patient Medical Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    name = fields.Char(
        string='Nom',
        required=True,
        tracking=True
    )
    prenoms = fields.Char(
        string='Prénoms',
        tracking=True
    )
    partner_id = fields.Many2one(
        'res.partner', 
        string='Contact associé', 
        required=False,
        ondelete='cascade',
        help='Contact associé au patient (optionnel)'
    )
    date_naissance = fields.Date(
        string='Date de naissance',
        required=True,
        tracking=True
    )
    lieu_naissance = fields.Char(
        string='Lieu de naissance'
    )
    numero_secu = fields.Char(
        string='Numéro de sécurité sociale',
        size=15
    )
    groupe_sanguin = fields.Selection([
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], string='Groupe sanguin')
    
    antecedents = fields.Text(
        string='Antécédents médicaux',
        help='Antécédents médicaux du patient'
    )
    allergies = fields.Text(
        string='Allergies',
        help='Allergies connues du patient'
    )
    medecin_traitant = fields.Many2one(
        'medical.medecin',
        string='Médecin traitant'
    )
    
    consultation_ids = fields.One2many(
        'medical.consultation',
        'patient_id',
        string='Consultations'
    )
    rendezvous_ids = fields.One2many(
        'medical.rendezvous',
        'patient_id',
        string='Rendez-vous'
    )
    
    age = fields.Integer(
        string='Âge',
        compute='_compute_age',
        store=True
    )
    
    @api.depends('date_naissance')
    def _compute_age(self):
        for record in self:
            if record.date_naissance:
                today = fields.Date.today()
                record.age = today.year - record.date_naissance.year - (
                    (today.month, today.day) < (record.date_naissance.month, record.date_naissance.day)
                )
            else:
                record.age = 0
    
    @api.model
    def create(self, vals):
        return super(MedicalPatient, self).create(vals)
    
    def name_get(self):
        result = []
        for patient in self:
            name = f"{patient.name} ({patient.age} ans)" if patient.age else patient.name
            result.append((patient.id, name))
        return result