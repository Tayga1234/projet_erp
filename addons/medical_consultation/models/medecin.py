from odoo import models, fields, api

class MedicalMedecin(models.Model):
    _name = 'medical.medecin'
    _description = 'Médecin Medical Record'
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
        help='Contact associé au médecin (optionnel)'
    )
    
    specialite = fields.Selection([
        ('generaliste', 'Médecin généraliste'),
        ('cardiologue', 'Cardiologue'),
        ('dermatologue', 'Dermatologue'),
        ('pediatre', 'Pédiatre'),
        ('gynecologue', 'Gynécologue'),
        ('ophtalmologue', 'Ophtalmologue'),
        ('psychiatre', 'Psychiatre'),
        ('orthopediste', 'Orthopédiste'),
        ('dermatologue', 'Dermatologue'),
        ('neurologue', 'Neurologue'),
        ('radiologue', 'Radiologue'),
        ('anesthesiste', 'Anesthesiste'),
        ('chirurgien', 'Chirurgien'),
        ('endocrinologue', 'Endocrinologue'),
        ('gastroenterologue', 'Gastroenterologue'),
        ('hepatologue', 'Hépatologue'),
        ('hematologue', 'Hématologue'),
        ('infectologue', 'Infectologue'),
        ('autre', 'Autre'),
    ], string='Spécialité', required=True)
    
    numero_rpps = fields.Char(
        string='Numéro RPPS',
        size=11,
        help='Numéro de Répertoire Partagé des Professionnels de Santé'
    )
    
    numero_adeli = fields.Char(
        string='Numéro ADELI',
        size=9,
        help='Numéro d\'identification des professionnels de santé'
    )
    
    tarif_consultation = fields.Float(
        string='Tarif consultation (FCFA)',
        default=5000,
        help='Tarif standard d\'une consultation'
    )
    
    telephone = fields.Char(
        related='partner_id.phone',
        string='Téléphone',
        store=True
    )
    
    email = fields.Char(
        related='partner_id.email',
        string='Email',
        store=True
    )
    

    consultation_ids = fields.One2many(
        'medical.consultation',
        'medecin_id',
        string='Consultations'
    )
    
    rendezvous_ids = fields.One2many(
        'medical.rendezvous',
        'medecin_id',
        string='Rendez-vous'
    )
    
    patient_ids = fields.One2many(
        'medical.patient',
        'medecin_traitant',
        string='Patients suivis'
    )
    
    active = fields.Boolean(
        string='Actif',
        default=True
    )
    

    @api.model
    def create(self, vals):
        return super(MedicalMedecin, self).create(vals)
    
    def name_get(self):
        result = []
        for medecin in self:
            name = f"Dr {medecin.name} - {medecin.specialite}"
            result.append((medecin.id, name))
        return result
    
    @api.depends('specialite')
    def _compute_display_name(self):
        for record in self:
            record.display_name = f"Dr {record.name} - {record.specialite}"