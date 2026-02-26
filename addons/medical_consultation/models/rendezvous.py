from odoo import models, fields, api
from datetime import datetime, timedelta

class MedicalRendezvous(models.Model):
    _name = 'medical.rendezvous'
    _description = 'Rendez-vous Médical'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_heure'
    
    patient_id = fields.Many2one(
        'medical.patient',
        string='Patient',
        required=True,
        tracking=True
    )
    
    medecin_id = fields.Many2one(
        'medical.medecin',
        string='Médecin',
        required=True,
        tracking=True
    )
    
    date_heure = fields.Datetime(
        string='Date et heure',
        required=True,
        tracking=True
    )
    
    duree = fields.Integer(
        string='Durée (minutes)',
        default=30,
        required=True,
        help='Durée estimée du rendez-vous en minutes'
    )
    
    date_fin = fields.Datetime(
        string='Heure de fin',
        compute='_compute_date_fin',
        store=True
    )
    
    motif = fields.Text(
        string='Motif du rendez-vous',
        required=True,
        tracking=True
    )
    
    notes = fields.Text(
        string='Notes',
        help='Notes supplémentaires'
    )
    
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('confirme', 'Confirmé'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
        ('absent', 'Patient absent'),
    ], string='État', default='brouillon', tracking=True)
    
    consultation_id = fields.Many2one(
        'medical.consultation',
        string='Consultation associée',
        readonly=True
    )
    
    couleur = fields.Char(
        string='Couleur',
        default='#1f77b4',
        help='Couleur pour l\'affichage dans le calendrier'
    )
    
    @api.depends('date_heure', 'duree')
    def _compute_date_fin(self):
        for rdv in self:
            if rdv.date_heure and rdv.duree:
                rdv.date_fin = rdv.date_heure + timedelta(minutes=rdv.duree)
            else:
                rdv.date_fin = False

    @api.model
    def create(self, vals):
        return super(MedicalRendezvous, self).create(vals)
        
    def action_confirm(self):
        self.write({'state': 'confirme'})
        
    def action_start(self):
        self.write({'state': 'en_cours'})
        # Créer automatiquement la consultation
        consultation_vals = {
            'patient_id': self.patient_id.id,
            'medecin_id': self.medecin_id.id,
            'date_consultation': fields.Datetime.now(),
            'motif': self.motif,
            'state': 'en_cours',
        }
        consultation = self.env['medical.consultation'].create(consultation_vals)
        self.write({'consultation_id': consultation.id})
    
    def action_finish(self):
        self.write({'state': 'termine'})
    
    def action_cancel(self):
        self.write({'state': 'annule'})
    
    def action_absent(self):
        self.write({'state': 'absent'})
    
    def action_reset_draft(self):
        self.write({'state': 'brouillon'})
    
    def name_get(self):
        result = []
        for rdv in self:
            name = f"RDV {rdv.date_heure.strftime('%d/%m/%Y %H:%M')} - {rdv.patient_id.name} avec Dr {rdv.medecin_id.name}"
            result.append((rdv.id, name))
        return result
    
    @api.constrains('date_heure')
    def _check_date_heure(self):
        for rdv in self:
            if rdv.date_heure and rdv.date_heure < fields.Datetime.now():
                raise models.ValidationError('La date du rendez-vous ne peut pas être dans le passé.')