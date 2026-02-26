from odoo import models, fields, api
from datetime import datetime

class MedicalConsultation(models.Model):
    _name = 'medical.consultation'
    _description = 'Consultation Médicale'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date_consultation desc'
    
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
    
    date_consultation = fields.Datetime(
        string='Date de consultation',
        required=True,
        default=fields.Datetime.now,
        tracking=True
    )
    
    motif = fields.Text(
        string='Motif de consultation',
        required=True,
        tracking=True
    )
    
    symptomes = fields.Text(
        string='Symptômes',
        help='Symptômes décrits par le patient'
    )
    
    diagnostic = fields.Text(
        string='Diagnostic',
        help='Diagnostic posé par le médecin'
    )
    
    examen_clinique = fields.Text(
        string='Examen clinique',
        help='Résultats de l\'examen clinique'
    )
    
    examen_complementaire = fields.Text(
        string='Examens complémentaires',
        help='Examens prescrits (radiographie, analyse, etc.)'
    )
    
    traitement = fields.Text(
        string='Traitement',
        help='Traitement prescrit'
    )
    
    notes = fields.Text(
        string='Notes',
        help='Notes supplémentaires'
    )
    
    prescription_ids = fields.One2many(
        'medical.prescription',
        'consultation_id',
        string='Prescriptions'
    )
    
    state = fields.Selection([
        ('brouillon', 'Brouillon'),
        ('en_cours', 'En cours'),
        ('terminee', 'Terminée'),
        ('annulee', 'Annulée'),
    ], string='État', default='brouillon', tracking=True)
    
    tarif = fields.Float(
        string='Tarif (FCFA)',
        related='medecin_id.tarif_consultation',
        store=True
    )
    
    paiement_effectue = fields.Boolean(
        string='Paiement effectué',
        default=False
    )
    
    @api.model
    def create(self, vals):
        return super(MedicalConsultation, self).create(vals)
    
    def action_start_consultation(self):
        self.write({'state': 'en_cours'})
    
    def action_finish_consultation(self):
        self.write({'state': 'terminee'})
    
    def action_cancel_consultation(self):
        self.write({'state': 'annulee'})
    
    def action_reset_draft(self):
        self.write({'state': 'brouillon'})
    
    def name_get(self):
        result = []
        for consultation in self:
            name = f"Consultation du {consultation.date_consultation.strftime('%d/%m/%Y %H:%M')} - {consultation.patient_id.name}"
            result.append((consultation.id, name))
        return result

