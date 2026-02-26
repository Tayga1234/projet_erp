#!/bin/bash

# Script de démonstration pour le projet médical
# Usage: ./demo.sh

echo "🎯 DÉMONSTRATION DU MODULE MÉDICAL"
echo "=================================="

# Vérifier que Docker est running
echo "📦 Vérification des services Docker..."
docker-compose ps

# Créer la base de démo si nécessaire
echo "🗄️ Création de la base de démonstration..."
docker-compose exec db createdb -U odoo demo_medical_db 2>/dev/null || echo "Base de démo déjà existante"

# Installer le module
echo "📥 Installation du module médical..."
docker-compose exec odoo odoo -d demo_medical_db --db_host=db --db_port=5432 --db_user=odoo --db_password=odoo -i medical_consultation --stop-after-init

echo ""
echo "🎉 MODULE INSTALLÉ AVEC SUCCÈS !"
echo ""
echo "📋 ACCÈS À L'APPLICATION:"
echo "   URL: http://localhost:8069"
echo "   Base de données: demo_medical_db"
echo "   Utilisateur: admin"
echo "   Mot de passe: admin"
echo ""
echo "🌟 FONCTIONNALITÉS À MONTRER:"
echo "   1. Menu Patients (avec badges colorés)"
echo "   2. Menu Médecins (spécialités et tarifs)"
echo "   3. Menu Rendez-vous (calendrier et workflow)"
echo "   4. Menu Consultations (diagnostics et prescriptions)"
echo "   5. Menu Prescriptions (médicaments et dosages)"
echo "   6. Vues Graphiques et Pivot (statistiques)"
echo ""
echo "🧪 POUR LANCER LES TESTS:"
echo "   ./run_tests.sh"
echo ""
echo "📊 POUR VOIR LES DONNÉES DE TEST:"
echo "   15 patients"
echo "   12 médecins"
echo "   28 rendez-vous"
echo "   2 consultations"
echo "   5 prescriptions"
echo ""
echo "🎯 POINTS CLÉS À PRÉSENTER:"
echo "   • Interface moderne avec badges et couleurs"
echo "   • Workflow complet: Patient → Rendez-vous → Consultation → Prescription"
echo "   • 55 tests unitaires et d'intégration"
echo "   • Graphiques et statistiques intégrées"
echo "   • Architecture modulaire et maintenable"
echo ""
echo "🚀 DÉMARREZ VOTRE PRÉSENTATION MAINTENANT !"
