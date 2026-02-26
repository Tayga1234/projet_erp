from odoo import models, fields, api

class MedicalPrescription(models.Model):
    _name = 'medical.prescription'
    _description = 'Prescription Médicale'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    consultation_id = fields.Many2one(
        'medical.consultation',
        string='Consultation',
        required=True,
        ondelete='cascade'
    )
    
    patient_id = fields.Many2one(
        related='consultation_id.patient_id',
        string='Patient',
        store=True,
        readonly=True
    )
    
    medecin_id = fields.Many2one(
        related='consultation_id.medecin_id',
        string='Médecin',
        store=True,
        readonly=True
    )
    
    date_prescription = fields.Datetime(
        string='Date de prescription',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    
    medicament = fields.Char(
        string='Médicament',
        required=True,
        tracking=True,
        help='Nom du médicament'
    )
    
    dosage = fields.Char(
        string='Dosage',
        required=True,
        help='Ex: 500mg, 1g, etc.'
    )
    
    posologie = fields.Text(
        string='Posologie',
        required=True,
        help='Comment prendre le médicament (ex: 1 comprimé matin et soir pendant 7 jours)'
    )
    
    duree = fields.Integer(
        string='Durée (jours)',
        help='Durée du traitement en jours'
    )
    
    quantite = fields.Integer(
        string='Quantité',
        help='Quantité prescrite (nombre de boîtes, flacons, etc.)'
    )
    
    instructions = fields.Text(
        string='Instructions supplémentaires',
        help='Instructions particulières pour le patient'
    )
    
    type_medicament = fields.Selection([
        ('comprime', 'Comprimé'),
        ('gelule', 'Gélule'),
        ('sirop', 'Sirop'),
        ('pommade', 'Pommade'),
        ('gouttes', 'Gouttes'),
        ('injection', 'Injection'),
        ('autre', 'Autre'),
    ], string='Type de médicament')
    
    voie_administration = fields.Selection([
        ('orale', 'Voie orale'),
        ('intraveineuse', 'Voie intraveineuse'),
        ('intramusculaire', 'Voie intramusculaire'),
        ('cutanee', 'Voie cutanée'),
        ('nasale', 'Voie nasale'),
        ('autre', 'Autre'),
    ], string='Voie d\'administration', default='orale')
    
    active = fields.Boolean(
        string='Active',
        default=True
    )
    
    @api.model
    def create(self, vals):
        return super(MedicalPrescription, self).create(vals)
    
    def name_get(self):
        result = []
        for prescription in self:
            name = f"{prescription.medicament} - {prescription.patient_id.name}"
            result.append((prescription.id, name))
        return result