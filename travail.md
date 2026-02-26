# Projet ERP IBAM 2026 - Module Gestion de Consultation Médicale

## 1. Introduction
- Contexte du projet
- Objectifs pédagogiques
- Choix de l'ERP : [ODOO/NextERP/Dolibarr] - à définir

## 2. Analyse des Besoins
### 2.1. Acteurs identifiés
- Médecin
- Patient
- Secrétaire médicale
- Administrateur

### 2.2. Fonctionnalités requises
- Prise de rendez-vous
- Gestion des dossiers patients
- Consultation médicale
- Prescription médicale
- Facturation
- Rapports et statistiques

## 3. Architecture Technique
### 3.1. Choix technologiques
- **ERP sélectionné** : ODOO Community Edition v16
- **Justification** : Open source, documentation complète, communauté active
- **Langage de programmation** : Python 3.10+
- **Base de données** : PostgreSQL
- **Framework** : ODOO Framework (basé sur Python)
- **Frontend** : XML (QWeb), JavaScript, CSS Bootstrap
### 3.2. Diagramme de cas d'utilisation
[Description des interactions entre acteurs et système]

## 4. Conception Détaillée
### 4.1. Diagramme de classes
- Classe Patient
- Classe Medecin  
- Classe Consultation
- Classe Prescription
- Classe RendezVous

### 4.2. Description des classes

#### Diagramme de classes ODOO

```mermaid
classDiagram
    class res_partner {
        +name: Char
        +email: Char
        +phone: Char
        +is_patient: Boolean
        +is_medecin: Boolean
        +date_naissance: Date
        +numero_secu: Char
    }
    
    class medical_medecin {
        +partner_id: Many2one
        +specialite: Char
        +numero_rpps: Char
        +tarif_consultation: Float
    }
    
    class medical_patient {
        +partner_id: Many2one
        +groupe_sanguin: Char
        +antecedents: Text
        +allergies: Text
    }
    
    class medical_consultation {
        +patient_id: Many2one
        +medecin_id: Many2one
        +date_consultation: Datetime
        +motif: Text
        +symptomes: Text
        +diagnostic: Text
        +notes: Text
        +state: Selection
    }
    
    class medical_prescription {
        +consultation_id: Many2one
        +medicament: Char
        +posologie: Char
        +duree: Integer
        +instructions: Text
    }
    
    class medical_rendezvous {
        +patient_id: Many2one
        +medecin_id: Many2one
        +date_heure: Datetime
        +duree: Integer
        +state: Selection
        +notes: Text
    }
    
    res_partner ||--o{ medical_patient : "1..1"
    res_partner ||--o{ medical_medecin : "1..1"
    medical_patient ||--o{ medical_consultation : "1..*"
    medical_medecin ||--o{ medical_consultation : "1..*"
    medical_consultation ||--o{ medical_prescription : "1..*"
    medical_patient ||--o{ medical_rendezvous : "1..*"
    medical_medecin ||--o{ medical_rendezvous : "1..*"
```

## 5. Implémentation
### 5.1. Structure des fichiers
- Organisation du module
- Fichiers de configuration
- Modèles de données
- Contrôleurs
- Vues

### 5.2. Fonctionnalités implémentées
1. Gestion des patients
2. Prise de rendez-vous
3. Consultation médicale
4. Prescription médicale

## 6. Tests et Validation
### 6.1. Plan de tests
- Tests unitaires
- Tests d'intégration
- Tests fonctionnels

### 6.2. Résultats attendus

## 7. Déploiement
### 7.1. Prérequis
### 7.2. Procédure d'installation
### 7.3. Configuration

## 8. Conclusion
- Bilan du projet
- Perspectives d'évolution

## 9. Annexes
- Code source
- Captures d'écran
- Documentation technique