#!/bin/bash

# Script pour lancer les tests du module médical
# Usage: ./run_tests.sh [test_class]

# Configuration
MODULE_NAME="medical_consultation"
ODOO_PATH="/mnt/extra-addons"
DB_NAME="test_medical_db"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 Lancement des tests du module médical${NC}"
echo -e "${YELLOW}Module: $MODULE_NAME${NC}"
echo -e "${YELLOW}Base de données: $DB_NAME${NC}"
echo ""

# Fonction pour afficher le statut
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Créer la base de données de test si elle n'existe pas
echo -e "${BLUE}📦 Création de la base de données de test...${NC}"
createdb -h localhost -U odoo $DB_NAME 2>/dev/null
if [ $? -eq 0 ]; then
    print_status 0 "Base de données créée"
else
    print_status 1 "La base de données existe déjà ou erreur de création"
fi

# Installer le module
echo -e "${BLUE}📥 Installation du module $MODULE_NAME...${NC}"
odoo -d $DB_NAME -i $MODULE_NAME --stop-after-init --log-level=test
print_status $? "Installation du module"

# Lancer tous les tests si aucune classe spécifiée
if [ -z "$1" ]; then
    echo -e "${BLUE}🧪 Lancement de tous les tests...${NC}"
    odoo -d $DB_NAME --test-enable --stop-after-init --log-level=test --test-tags=$MODULE_NAME
    print_status $? "Tests complets"
else
    echo -e "${BLUE}🧪 Lancement des tests pour: $1${NC}"
    odoo -d $DB_NAME --test-enable --stop-after-init --log-level=test --test-tags=$MODULE_NAME.$1
    print_status $? "Tests pour $1"
fi

# Tests spécifiques par modèle
echo ""
echo -e "${BLUE}📋 Tests disponibles:${NC}"
echo -e "${YELLOW}1. TestMedicalPatient${NC} - Tests du modèle Patient"
echo -e "${YELLOW}2. TestMedicalMedecin${NC} - Tests du modèle Médecin"
echo -e "${YELLOW}3. TestMedicalRendezvous${NC} - Tests du modèle Rendez-vous"
echo -e "${YELLOW}4. TestMedicalConsultation${NC} - Tests du modèle Consultation"
echo -e "${YELLOW}5. TestMedicalPrescription${NC} - Tests du modèle Prescription"
echo -e "${YELLOW}6. TestMedicalWorkflow${NC} - Tests du workflow complet"
echo -e "${YELLOW}7. TestMedicalViews${NC} - Tests des vues et actions"
echo -e "${YELLOW}8. TestMedicalSecurity${NC} - Tests de sécurité"
echo -e "${YELLOW}9. TestMedicalPerformance${NC} - Tests de performance"

echo ""
echo -e "${GREEN}🎉 Tests terminés !${NC}"
echo -e "${BLUE}📊 Pour voir les résultats détaillés, consultez les logs Odoo${NC}"
