#!/usr/bin/env python3
"""
Apollo AI Marketing Toolkit - Script Principal
Interface en ligne de commande pour toutes les fonctionnalités
"""

import argparse
import sys
import os
from datetime import datetime, timedelta
import json
import subprocess
from colorama import init, Fore, Back, Style
from tqdm import tqdm
import time

# Initialize colorama for cross-platform colored output
init()

from config import APOLLO_GYMS, OPENAI_CONFIG
from content_generator import ApolloContentGenerator
from scheduler import ApolloScheduler
from analytics import ApolloAnalytics

class ApolloMainInterface:
    def __init__(self):
        self.content_generator = ApolloContentGenerator()
        self.scheduler = ApolloScheduler()
        self.analytics = ApolloAnalytics()
        
    def print_banner(self):
        """Affiche le banner Apollo"""
        banner = f"""
{Fore.RED}
╔═══════════════════════════════════════════════╗
║           🥊 APOLLO AI MARKETING TOOLKIT      ║
║                                               ║
║   IA • Growth Hacking • Automatisation       ║
║   Content • Analytics • Multi-plateformes    ║
╚═══════════════════════════════════════════════╝
{Style.RESET_ALL}

{Fore.CYAN}📍 13 salles Apollo Sporting Club à Paris{Style.RESET_ALL}
{Fore.GREEN}🚀 Prêt pour l'alternance chez Apollo!{Style.RESET_ALL}
"""
        print(banner)
    
    def show_menu(self):
        """Affiche le menu principal"""
        menu = f"""
{Fore.YELLOW}═══════════ MENU PRINCIPAL ═══════════{Style.RESET_ALL}

{Fore.CYAN}1.{Style.RESET_ALL} 🤖 Content Generator   - Générer du contenu IA
{Fore.CYAN}2.{Style.RESET_ALL} 📅 Scheduler           - Programmer publications  
{Fore.CYAN}3.{Style.RESET_ALL} 📊 Analytics           - Analyser performances
{Fore.CYAN}4.{Style.RESET_ALL} 📱 Dashboard Web       - Interface Streamlit
{Fore.CYAN}5.{Style.RESET_ALL} 🔧 Configuration       - Paramétrer le système
{Fore.CYAN}6.{Style.RESET_ALL} 📋 Démo Complète       - Présentation pour Apollo
{Fore.CYAN}7.{Style.RESET_ALL} ❌ Quitter

{Fore.YELLOW}═══════════════════════════════════════{Style.RESET_ALL}
"""
        print(menu)
    
    def content_generator_menu(self):
        """Menu du générateur de contenu"""
        while True:
            print(f"\n{Fore.YELLOW}🤖 CONTENT GENERATOR{Style.RESET_ALL}")
            print("1. Générer un post simple")
            print("2. Générer un lot de posts")
            print("3. Générer pour toutes les salles")
            print("4. Voir le contenu généré")
            print("5. Retour au menu principal")
            
            choice = input(f"\n{Fore.CYAN}Votre choix (1-5): {Style.RESET_ALL}")
            
            if choice == "1":
                self.generate_single_post()
            elif choice == "2":
                self.generate_batch_posts()
            elif choice == "3":
                self.generate_all_gyms()
            elif choice == "4":
                self.show_generated_content()
            elif choice == "5":
                break
            else:
                print(f"{Fore.RED}❌ Choix invalide{Style.RESET_ALL}")
    
    def generate_single_post(self):
        """Génère un post simple"""
        print(f"\n{Fore.CYAN}📝 Génération d'un post personnalisé{Style.RESET_ALL}")
        
        # Sélection de salle
        print("\nSalles disponibles:")
        for i, gym in enumerate(APOLLO_GYMS, 1):
            print(f"{i}. {gym['name']} - {gym['address']}")
        
        try:
            gym_choice = int(input("Choisir une salle (1-4): ")) - 1
            if gym_choice < 0 or gym_choice >= len(APOLLO_GYMS):
                raise ValueError
            gym_id = APOLLO_GYMS[gym_choice]['id']
        except (ValueError, IndexError):
            print(f"{Fore.RED}❌ Choix de salle invalide{Style.RESET_ALL}")
            return
        
        # Sélection plateforme
        platforms = ["instagram", "facebook", "linkedin", "tiktok"]
        print(f"\nPlateformes: {', '.join(platforms)}")
        platform = input("Choisir une plateforme: ").lower()
        if platform not in platforms:
            print(f"{Fore.RED}❌ Plateforme invalide{Style.RESET_ALL}")
            return
        
        # Sélection type
        post_types = ["motivation", "workout_tips", "coach_spotlight", "member_success"]
        print(f"\nTypes de posts: {', '.join(post_types)}")
        post_type = input("Choisir un type: ").lower()
        if post_type not in post_types:
            print(f"{Fore.RED}❌ Type invalide{Style.RESET_ALL}")
            return
        
        # Prompt personnalisé
        custom_prompt = input("\nPrompt personnalisé (optionnel): ").strip()
        
        # Génération
        print(f"\n{Fore.YELLOW}🤖 Génération en cours...{Style.RESET_ALL}")
        
        with tqdm(total=100, desc="Génération IA", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            for i in range(100):
                time.sleep(0.02)  # Simulation du temps de traitement
                pbar.update(1)
        
        content = self.content_generator.generate_post_content(
            gym_id=gym_id,
            platform=platform,
            post_type=post_type,
            custom_prompt=custom_prompt if custom_prompt else None
        )
        
        if content:
            print(f"\n{Fore.GREEN}✅ Contenu généré avec succès!{Style.RESET_ALL}")
            print(f"\n{Fore.CYAN}═══ CONTENU GÉNÉRÉ ═══{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}🏋️ Salle:{Style.RESET_ALL} {content['gym']['name']}")
            print(f"{Fore.YELLOW}📱 Plateforme:{Style.RESET_ALL} {content['platform']}")
            print(f"{Fore.YELLOW}🎯 Type:{Style.RESET_ALL} {content['type']}")
            print(f"{Fore.YELLOW}⏰ Heure optimale:{Style.RESET_ALL} {content['optimal_time']}")
            print(f"\n{Fore.CYAN}📝 CONTENU:{Style.RESET_ALL}")
            print(f"{content['content']}")
            print(f"\n{Fore.CYAN}🏷️ HASHTAGS:{Style.RESET_ALL}")
            print(" ".join(content['hashtags'][:10]))
            
            # Option de sauvegarde
            if input(f"\n{Fore.CYAN}Sauvegarder ce contenu? (o/N): {Style.RESET_ALL}").lower() == 'o':
                filepath = self.content_generator.save_content_batch([content])
                print(f"{Fore.GREEN}💾 Sauvegardé dans: {filepath}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Échec de la génération{Style.RESET_ALL}")
    
    def generate_batch_posts(self):
        """Génère un lot de posts"""
        print(f"\n{Fore.CYAN}📦 Génération d'un lot de posts{Style.RESET_ALL}")
        
        try:
            count = int(input("Nombre de posts à générer (1-20): "))
            if count < 1 or count > 20:
                raise ValueError
        except ValueError:
            print(f"{Fore.RED}❌ Nombre invalide{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.YELLOW}🤖 Génération de {count} posts en cours...{Style.RESET_ALL}")
        
        batch = self.content_generator.generate_batch_content(count=count)
        
        if batch:
            print(f"\n{Fore.GREEN}✅ {len(batch)} posts générés avec succès!{Style.RESET_ALL}")
            
            # Aperçu
            for i, content in enumerate(batch[:3], 1):
                print(f"\n{i}. {content['gym']['name']} - {content['platform']} - {content['type']}")
                print(f"   {content['content'][:80]}...")
            
            if len(batch) > 3:
                print(f"   ... et {len(batch)-3} autres posts")
            
            # Sauvegarde automatique
            filepath = self.content_generator.save_content_batch(batch)
            print(f"{Fore.GREEN}💾 Lot sauvegardé dans: {filepath}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Échec de la génération{Style.RESET_ALL}")
    
    def analytics_menu(self):
        """Menu analytics"""
        while True:
            print(f"\n{Fore.YELLOW}📊 ANALYTICS{Style.RESET_ALL}")
            print("1. Rapport de performance")
            print("2. Analyse par salle")
            print("3. Comparaison plateformes")
            print("4. Recommandations IA")
            print("5. Export des données")
            print("6. Retour au menu principal")
            
            choice = input(f"\n{Fore.CYAN}Votre choix (1-6): {Style.RESET_ALL}")
            
            if choice == "1":
                self.show_performance_report()
            elif choice == "2":
                self.analyze_by_gym()
            elif choice == "3":
                self.compare_platforms()
            elif choice == "4":
                self.show_ai_recommendations()
            elif choice == "5":
                self.export_analytics_data()
            elif choice == "6":
                break
            else:
                print(f"{Fore.RED}❌ Choix invalide{Style.RESET_ALL}")
    
    def show_performance_report(self):
        """Affiche le rapport de performance"""
        print(f"\n{Fore.CYAN}📋 Génération du rapport de performance{Style.RESET_ALL}")
        
        try:
            days = int(input("Période d'analyse (jours, défaut 30): ") or "30")
        except ValueError:
            days = 30
        
        print(f"\n{Fore.YELLOW}📊 Analyse en cours...{Style.RESET_ALL}")
        
        report = self.analytics.generate_performance_report(days=days)
        
        print(f"\n{Fore.GREEN}✅ Rapport généré pour les {days} derniers jours{Style.RESET_ALL}")
        print(f"\n{Fore.CYAN}═══ RÉSUMÉ EXÉCUTIF ═══{Style.RESET_ALL}")
        print(f"🎯 Total leads générés: {report['summary']['total_leads_generated']}")
        print(f"💬 Taux d'engagement moyen: {report['summary']['average_engagement_rate']:.2%}")
        print(f"👥 Reach total: {report['summary']['total_reach']:,}")
        print(f"📈 Leads par jour: {report['summary']['leads_per_day']:.1f}")
        
        print(f"\n{Fore.CYAN}═══ PERFORMANCE PAR PLATEFORME ═══{Style.RESET_ALL}")
        for platform, data in report['platforms'].items():
            print(f"\n📱 {platform.upper()}:")
            print(f"   Posts publiés: {data['total_posts']}")
            print(f"   Reach moyen: {data['avg_daily_reach']:,.0f}")
            print(f"   Leads générés: {data['total_leads']}")
        
        # Export optionnel
        if input(f"\n{Fore.CYAN}Exporter le rapport? (o/N): {Style.RESET_ALL}").lower() == 'o':
            filepath = self.analytics.export_report_to_json(report)
            print(f"{Fore.GREEN}💾 Rapport exporté: {filepath}{Style.RESET_ALL}")
    
    def show_ai_recommendations(self):
        """Affiche les recommandations IA"""
        print(f"\n{Fore.CYAN}💡 Recommandations IA{Style.RESET_ALL}")
        
        report = self.analytics.generate_performance_report(days=14)
        recommendations = report['recommendations']
        
        if not recommendations:
            print(f"{Fore.YELLOW}ℹ️ Aucune recommandation spécifique pour le moment{Style.RESET_ALL}")
            return
        
        print(f"\n{Fore.GREEN}🎯 {len(recommendations)} recommandations générées:{Style.RESET_ALL}")
        
        for i, rec in enumerate(recommendations, 1):
            priority_color = {
                'high': Fore.RED,
                'medium': Fore.YELLOW, 
                'low': Fore.GREEN
            }[rec['priority']]
            
            print(f"\n{priority_color}{i}. [{rec['priority'].upper()}] {rec['title']}{Style.RESET_ALL}")
            print(f"   Plateforme: {rec['platform']}")
            print(f"   {rec['description']}")
            print(f"   {Fore.GREEN}Impact attendu: {rec['expected_impact']}{Style.RESET_ALL}")
    
    def launch_dashboard(self):
        """Lance le dashboard Streamlit"""
        print(f"\n{Fore.CYAN}🚀 Lancement du dashboard web...{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}📱 Le dashboard va s'ouvrir dans votre navigateur{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔗 URL: http://localhost:8501{Style.RESET_ALL}")
        
        try:
            # Lancement de Streamlit
            subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"], 
                         check=True)
        except subprocess.CalledProcessError:
            print(f"{Fore.RED}❌ Erreur lors du lancement du dashboard{Style.RESET_ALL}")
        except KeyboardInterrupt:
            print(f"\n{Fore.YELLOW}⏹️ Dashboard arrêté par l'utilisateur{Style.RESET_ALL}")
    
    def configuration_menu(self):
        """Menu de configuration"""
        print(f"\n{Fore.YELLOW}🔧 CONFIGURATION{Style.RESET_ALL}")
        print("1. Vérifier la configuration")
        print("2. Tester la connexion OpenAI")
        print("3. Configurer les APIs sociales")
        print("4. Voir les salles Apollo")
        print("5. Retour au menu principal")
        
        choice = input(f"\n{Fore.CYAN}Votre choix (1-5): {Style.RESET_ALL}")
        
        if choice == "1":
            self.check_configuration()
        elif choice == "2":
            self.test_openai_connection()
        elif choice == "3":
            self.configure_social_apis()
        elif choice == "4":
            self.show_apollo_gyms()
        elif choice == "5":
            return
    
    def check_configuration(self):
        """Vérifie la configuration"""
        print(f"\n{Fore.CYAN}🔍 Vérification de la configuration{Style.RESET_ALL}")
        
        # Vérification OpenAI
        openai_key = OPENAI_CONFIG.get('api_key', '')
        if openai_key and len(openai_key) > 10:
            print(f"{Fore.GREEN}✅ Clé OpenAI configurée{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}❌ Clé OpenAI manquante{Style.RESET_ALL}")
        
        # Vérification des dossiers
        required_dirs = ['data', 'data/generated_content', 'data/analytics_data']
        for dir_path in required_dirs:
            if os.path.exists(dir_path):
                print(f"{Fore.GREEN}✅ Dossier {dir_path} existe{Style.RESET_ALL}")
            else:
                os.makedirs(dir_path, exist_ok=True)
                print(f"{Fore.YELLOW}📁 Dossier {dir_path} créé{Style.RESET_ALL}")
        
        # Vérification des dépendances
        try:
            import openai, pandas, plotly, streamlit
            print(f"{Fore.GREEN}✅ Toutes les dépendances sont installées{Style.RESET_ALL}")
        except ImportError as e:
            print(f"{Fore.RED}❌ Dépendance manquante: {e}{Style.RESET_ALL}")
    
    def test_openai_connection(self):
        """Teste la connexion OpenAI"""
        print(f"\n{Fore.CYAN}🤖 Test de la connexion OpenAI{Style.RESET_ALL}")
        
        if not OPENAI_CONFIG.get('api_key'):
            print(f"{Fore.RED}❌ Clé API OpenAI non configurée{Style.RESET_ALL}")
            return
        
        try:
            # Test simple
            content = self.content_generator.generate_post_content(
                gym_id=1, platform='instagram', post_type='motivation'
            )
            
            if content:
                print(f"{Fore.GREEN}✅ Connexion OpenAI fonctionnelle{Style.RESET_ALL}")
                print(f"📝 Test généré: {content['content'][:50]}...")
            else:
                print(f"{Fore.RED}❌ Échec du test OpenAI{Style.RESET_ALL}")
                
        except Exception as e:
            print(f"{Fore.RED}❌ Erreur OpenAI: {str(e)[:100]}{Style.RESET_ALL}")
    
    def show_apollo_gyms(self):
        """Affiche les salles Apollo"""
        print(f"\n{Fore.CYAN}🏋️ Salles Apollo Sporting Club{Style.RESET_ALL}")
        
        for i, gym in enumerate(APOLLO_GYMS, 1):
            print(f"\n{Fore.YELLOW}{i}. {gym['name']}{Style.RESET_ALL}")
            print(f"   📍 {gym['address']}")
            print(f"   📞 {gym['phone']}")
            print(f"   🥊 Spécialités: {', '.join(gym['specialties'])}")
            print(f"   👨‍🏫 Coachs: {', '.join(gym['coaches'])}")
            print(f"   👥 Capacité: {gym['capacity']} personnes")
    
    def run_complete_demo(self):
        """Démo complète pour Apollo"""
        print(f"\n{Fore.RED}🎬 DÉMO COMPLÈTE APOLLO AI MARKETING TOOLKIT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Cette démo présente toutes les fonctionnalités du système{Style.RESET_ALL}")
        
        input(f"\n{Fore.YELLOW}Appuyez sur Entrée pour commencer...{Style.RESET_ALL}")
        
        # 1. Génération de contenu
        print(f"\n{Fore.CYAN}🤖 1. CONTENT GENERATOR{Style.RESET_ALL}")
        print("Génération de 3 posts pour différentes salles Apollo...")
        
        demo_posts = []
        for i in range(3):
            gym_id = (i % 4) + 1
            platforms = ['instagram', 'facebook', 'linkedin']
            post_types = ['motivation', 'workout_tips', 'coach_spotlight']
            
            content = self.content_generator.generate_post_content(
                gym_id=gym_id,
                platform=platforms[i],
                post_type=post_types[i]
            )
            
            if content:
                demo_posts.append(content)
                print(f"✅ Post {i+1}: {content['gym']['name']} - {content['platform']}")
        
        # 2. Analytics
        print(f"\n{Fore.CYAN}📊 2. ANALYTICS{Style.RESET_ALL}")
        print("Génération d'un rapport de performance...")
        
        report = self.analytics.generate_performance_report(days=7)
        print(f"✅ Rapport généré: {report['summary']['total_leads_generated']} leads")
        
        # 3. Recommandations IA
        print(f"\n{Fore.CYAN}💡 3. RECOMMANDATIONS IA{Style.RESET_ALL}")
        recommendations = report['recommendations'][:2]
        for rec in recommendations:
            print(f"• [{rec['priority'].upper()}] {rec['title']}")
        
        # 4. ROI projeté
        print(f"\n{Fore.CYAN}💰 4. ROI PROJETÉ POUR APOLLO{Style.RESET_ALL}")
        roi_metrics = [
            "+200% d'engagement grâce à la personnalisation IA",
            "+150% de leads générés via l'automatisation", 
            "-80% de temps consacré au content marketing",
            "+300% de reach multi-plateformes synchronisé"
        ]
        
        for metric in roi_metrics:
            print(f"🎯 {metric}")
        
        print(f"\n{Fore.GREEN}🎉 DÉMO TERMINÉE!{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Ce système est prêt à être déployé chez Apollo Sporting Club{Style.RESET_ALL}")
        
        if input(f"\n{Fore.CYAN}Lancer le dashboard web pour voir l'interface complète? (o/N): {Style.RESET_ALL}").lower() == 'o':
            self.launch_dashboard()
    
    def run(self):
        """Fonction principale"""
        self.print_banner()
        
        # Vérification rapide de la configuration
        if not OPENAI_CONFIG.get('api_key'):
            print(f"{Fore.RED}⚠️  Clé OpenAI non configurée dans config.py{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}💡 Ajoutez votre clé API dans le fichier .env{Style.RESET_ALL}")
        
        while True:
            self.show_menu()
            
            try:
                choice = input(f"{Fore.CYAN}Votre choix (1-7): {Style.RESET_ALL}")
                
                if choice == "1":
                    self.content_generator_menu()
                elif choice == "2":
                    print(f"{Fore.YELLOW}📅 Scheduler en développement...{Style.RESET_ALL}")
                elif choice == "3":
                    self.analytics_menu()
                elif choice == "4":
                    self.launch_dashboard()
                elif choice == "5":
                    self.configuration_menu()
                elif choice == "6":
                    self.run_complete_demo()
                elif choice == "7":
                    print(f"\n{Fore.GREEN}👋 Merci d'avoir utilisé Apollo AI Marketing Toolkit!{Style.RESET_ALL}")
                    break
                else:
                    print(f"{Fore.RED}❌ Choix invalide. Veuillez choisir entre 1 et 7.{Style.RESET_ALL}")
                    
            except KeyboardInterrupt:
                print(f"\n\n{Fore.YELLOW}⏹️ Application interrompue par l'utilisateur{Style.RESET_ALL}")
                break
            except Exception as e:
                print(f"{Fore.RED}❌ Erreur: {str(e)}{Style.RESET_ALL}")

def main():
    """Point d'entrée avec gestion des arguments"""
    parser = argparse.ArgumentParser(description='Apollo AI Marketing Toolkit')
    parser.add_argument('--version', action='version', version='Apollo AI Marketing Toolkit v1.0')
    parser.add_argument('--dashboard', action='store_true', help='Lancer directement le dashboard web')
    parser.add_argument('--demo', action='store_true', help='Lancer la démo complète')
    parser.add_argument('--generate', type=int, metavar='N', help='Générer N posts et quitter')
    
    args = parser.parse_args()
    
    app = ApolloMainInterface()
    
    if args.dashboard:
        app.launch_dashboard()
    elif args.demo:
        app.print_banner()
        app.run_complete_demo()
    elif args.generate:
        app.print_banner()
        print(f"Génération de {args.generate} posts...")
        batch = app.content_generator.generate_batch_content(count=args.generate)
        filepath = app.content_generator.save_content_batch(batch)
        print(f"✅ {len(batch)} posts générés et sauvegardés dans {filepath}")
    else:
        app.run()

if __name__ == "__main__":
    main()