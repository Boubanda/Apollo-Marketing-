"""
Apollo AI Scheduler
Automatisation intelligente des publications et des workflows marketing
"""

import schedule
import time
import json
from datetime import datetime, timedelta
from threading import Thread
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from config import (
    APOLLO_GYMS, AUTOMATION_CONFIG, SOCIAL_MEDIA_CONFIG,
    CONTENT_CONFIG
)
from content_generator import ApolloContentGenerator

class ApolloScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.content_generator = ApolloContentGenerator()
        self.scheduled_posts = []
        self.auto_responses_active = True
        self.lead_workflows_active = True
        
    def start(self):
        """Démarre le scheduler"""
        self.setup_automatic_posting()
        self.setup_lead_workflows()
        self.setup_performance_monitoring()
        
        self.scheduler.start()
        print("🚀 Apollo Scheduler démarré!")
        
    def stop(self):
        """Arrête le scheduler"""
        self.scheduler.shutdown()
        print("⏹️ Apollo Scheduler arrêté!")
    
    def setup_automatic_posting(self):
        """Configure la publication automatique selon le planning"""
        posting_schedule = AUTOMATION_CONFIG['posting_schedule']
        
        for day, posts in posting_schedule.items():
            for post_config in posts:
                # Planification pour chaque salle Apollo
                for gym in APOLLO_GYMS:
                    job_id = f"{day}_{post_config['time']}_{gym['id']}_{post_config['platform']}"
                    
                    # Conversion du jour en format cron
                    day_mapping = {
                        'monday': 0, 'tuesday': 1, 'wednesday': 2,
                        'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
                    }
                    
                    hour, minute = post_config['time'].split(':')
                    
                    self.scheduler.add_job(
                        func=self.auto_post,
                        trigger=CronTrigger(
                            day_of_week=day_mapping[day],
                            hour=int(hour),
                            minute=int(minute)
                        ),
                        args=[gym['id'], post_config['platform'], post_config['type']],
                        id=job_id,
                        replace_existing=True
                    )
        
        print(f"📅 {len(self.scheduler.get_jobs())} publications automatiques programmées")
    
    def auto_post(self, gym_id, platform, post_type):
        """Génère et publie automatiquement un post"""
        print(f"🤖 Publication automatique: {platform} - {post_type} - Gym {gym_id}")
        
        # Génération du contenu
        content = self.content_generator.generate_post_content(
            gym_id=gym_id,
            platform=platform,
            post_type=post_type
        )
        
        if not content:
            print("❌ Échec génération contenu")
            return
        
        # Publication sur la plateforme
        success = self.publish_content(content)
        
        if success:
            print(f"✅ Post publié avec succès sur {platform}")
            self.log_posted_content(content)
        else:
            print(f"❌ Échec publication sur {platform}")
            # Programmer une nouvelle tentative dans 30 minutes
            retry_time = datetime.now() + timedelta(minutes=30)
            self.scheduler.add_job(
                func=self.auto_post,
                trigger='date',
                run_date=retry_time,
                args=[gym_id, platform, post_type],
                id=f"retry_{gym_id}_{platform}_{int(time.time())}"
            )
    
    def publish_content(self, content):
        """Publie le contenu sur la plateforme spécifiée"""
        platform = content['platform']
        
        try:
            if platform == 'instagram':
                return self.publish_instagram(content)
            elif platform == 'facebook':
                return self.publish_facebook(content)
            elif platform == 'linkedin':
                return self.publish_linkedin(content)
            elif platform == 'tiktok':
                return self.publish_tiktok(content)
            else:
                print(f"⚠️ Plateforme non supportée: {platform}")
                return False
                
        except Exception as e:
            print(f"❌ Erreur publication {platform}: {e}")
            return False
    
    def publish_instagram(self, content):
        """Publication sur Instagram"""
        # Simulation d'API Instagram (en production, utiliser l'API officielle)
        print(f"📸 Publication Instagram pour {content['gym']['name']}")
        print(f"   Contenu: {content['content'][:50]}...")
        
        # En production, implémenter l'API Instagram Business
        """
        from instagrapi import Client
        
        cl = Client()
        cl.login(SOCIAL_MEDIA_CONFIG['instagram']['username'], 
                SOCIAL_MEDIA_CONFIG['instagram']['password'])
        
        if content.get('image_path'):
            cl.photo_upload(content['image_path'], content['content'])
        else:
            # Post texte uniquement ou avec image générée
            pass
        """
        
        return True  # Simulation de succès
    
    def publish_facebook(self, content):
        """Publication sur Facebook"""
        print(f"👥 Publication Facebook pour {content['gym']['name']}")
        
        # Simulation d'API Facebook
        """
        import facebook
        
        graph = facebook.GraphAPI(access_token=SOCIAL_MEDIA_CONFIG['facebook']['access_token'])
        graph.put_object(parent_object='me', connection_name='feed',
                        message=content['content'])
        """
        
        return True
    
    def publish_linkedin(self, content):
        """Publication sur LinkedIn"""
        print(f"💼 Publication LinkedIn pour {content['gym']['name']}")
        return True
    
    def publish_tiktok(self, content):
        """Publication sur TikTok"""
        print(f"🎵 Publication TikTok pour {content['gym']['name']}")
        return True
    
    def schedule_custom_post(self, gym_id, platform, post_type, publish_time, custom_prompt=None):
        """Planifie un post personnalisé"""
        job_id = f"custom_{gym_id}_{platform}_{int(time.time())}"
        
        self.scheduler.add_job(
            func=self.auto_post,
            trigger='date',
            run_date=publish_time,
            args=[gym_id, platform, post_type],
            id=job_id
        )
        
        scheduled_post = {
            'id': job_id,
            'gym_id': gym_id,
            'platform': platform,
            'type': post_type,
            'scheduled_time': publish_time.isoformat(),
            'custom_prompt': custom_prompt,
            'status': 'scheduled'
        }
        
        self.scheduled_posts.append(scheduled_post)
        print(f"📅 Post programmé: {publish_time} - {platform} - Gym {gym_id}")
        
        return job_id
    
    def setup_lead_workflows(self):
        """Configure les workflows automatiques pour les leads"""
        # Workflow de nurturing automatique
        self.scheduler.add_job(
            func=self.process_new_leads,
            trigger='interval',
            minutes=15,
            id='lead_processing'
        )
        
        # Suivi des prospects inactifs
        self.scheduler.add_job(
            func=self.follow_up_inactive_leads,
            trigger='interval',
            hours=24,
            id='inactive_leads_followup'
        )
        
        # Analyse des commentaires pour leads potentiels
        self.scheduler.add_job(
            func=self.analyze_social_comments,
            trigger='interval',
            hours=2,
            id='comment_analysis'
        )
    
    def process_new_leads(self):
        """Traite les nouveaux leads automatiquement"""
        print("🎯 Traitement automatique des nouveaux leads...")
        
        # Récupération des nouveaux leads (simulation)
        new_leads = self.get_new_leads()
        
        for lead in new_leads:
            # Scoring automatique
            score = self.calculate_lead_score(lead)
            
            # Assignation automatique selon le score
            if score >= 80:
                self.assign_to_sales_team(lead, priority='high')
                self.send_immediate_followup(lead)
            elif score >= 60:
                self.assign_to_sales_team(lead, priority='medium')
                self.schedule_followup(lead, hours=4)
            else:
                self.add_to_nurturing_sequence(lead)
    
    def calculate_lead_score(self, lead):
        """Calcule le score d'un lead basé sur différents critères"""
        score = 0
        
        # Critères de scoring
        if lead.get('budget') == 'premium':
            score += 30
        elif lead.get('budget') == 'standard':
            score += 20
        
        if lead.get('urgency') == 'immediate':
            score += 25
        elif lead.get('urgency') == 'this_month':
            score += 15
        
        if lead.get('experience') == 'beginner':
            score += 20  # Plus facile à convertir
        
        if lead.get('frequency') == '4+ times/week':
            score += 25
        
        # Score basé sur l'engagement social
        if lead.get('social_engagement') == 'high':
            score += 15
        
        return min(score, 100)  # Max 100
    
    def setup_performance_monitoring(self):
        """Configure le monitoring des performances"""
        # Analyse quotidienne des performances
        self.scheduler.add_job(
            func=self.analyze_daily_performance,
            trigger=CronTrigger(hour=8, minute=0),
            id='daily_performance'
        )
        
        # Rapport hebdomadaire
        self.scheduler.add_job(
            func=self.generate_weekly_report,
            trigger=CronTrigger(day_of_week=0, hour=9, minute=0),
            id='weekly_report'
        )
    
    def analyze_daily_performance(self):
        """Analyse les performances quotidiennes"""
        print("📊 Analyse des performances quotidiennes...")
        
        # Collecte des métriques
        metrics = self.collect_daily_metrics()
        
        # Détection d'anomalies
        anomalies = self.detect_performance_anomalies(metrics)
        
        if anomalies:
            self.alert_performance_issues(anomalies)
        
        # Optimisations automatiques
        self.apply_automatic_optimizations(metrics)
    
    def setup_auto_responses(self):
        """Configure les réponses automatiques aux commentaires/messages"""
        auto_responses = AUTOMATION_CONFIG['auto_responses']
        
        # Monitoring des mentions et commentaires
        self.scheduler.add_job(
            func=self.monitor_social_mentions,
            trigger='interval',
            minutes=30,
            id='social_monitoring'
        )
    
    def monitor_social_mentions(self):
        """Surveille les mentions et commentaires sur les réseaux sociaux"""
        if not self.auto_responses_active:
            return
        
        print("👂 Monitoring des mentions sociales...")
        
        # Simulation de monitoring
        mentions = self.get_recent_mentions()
        
        for mention in mentions:
            if self.should_auto_respond(mention):
                response = self.generate_auto_response(mention)
                self.send_auto_response(mention, response)
    
    def should_auto_respond(self, mention):
        """Détermine si une réponse automatique est appropriée"""
        # Critères pour réponse auto
        auto_keywords = AUTOMATION_CONFIG['auto_responses']['keywords'].keys()
        
        content = mention.get('content', '').lower()
        
        for keyword in auto_keywords:
            if keyword in content:
                return True
        
        return False
    
    def generate_auto_response(self, mention):
        """Génère une réponse automatique personnalisée"""
        content = mention.get('content', '').lower()
        gym_id = mention.get('gym_id', 1)
        gym = next((g for g in APOLLO_GYMS if g['id'] == gym_id), APOLLO_GYMS[0])
        
        responses = AUTOMATION_CONFIG['auto_responses']['keywords']
        
        for keyword, template in responses.items():
            if keyword in content:
                return template.format(
                    phone=gym['phone'],
                    opening_hours=gym['opening_hours'].get('monday', '6h-22h')
                )
        
        return "Merci pour votre intérêt ! Contactez-nous pour plus d'informations 💪"
    
    # Méthodes utilitaires (simulation)
    def get_new_leads(self):
        """Simule la récupération de nouveaux leads"""
        return []
    
    def get_recent_mentions(self):
        """Simule la récupération des mentions récentes"""
        return []
    
    def collect_daily_metrics(self):
        """Simule la collecte des métriques quotidiennes"""
        return {
            'posts_published': 12,
            'total_engagement': 1450,
            'new_followers': 25,
            'leads_generated': 8
        }
    
    def log_posted_content(self, content):
        """Log le contenu publié pour analyse"""
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'platform': content['platform'],
            'gym': content['gym']['name'],
            'type': content['type'],
            'content_preview': content['content'][:100]
        }
        
        # En production, sauvegarder en base de données
        print(f"📝 Log: {log_entry}")
    
    def get_scheduled_posts(self):
        """Retourne la liste des posts programmés"""
        return self.scheduled_posts
    
    def cancel_scheduled_post(self, job_id):
        """Annule un post programmé"""
        try:
            self.scheduler.remove_job(job_id)
            self.scheduled_posts = [p for p in self.scheduled_posts if p['id'] != job_id]
            print(f"🗑️ Post annulé: {job_id}")
            return True
        except:
            print(f"❌ Impossible d'annuler le post: {job_id}")
            return False

# =============================================================================
# FONCTIONS DE DÉMONSTRATION
# =============================================================================

def demo_scheduler():
    """Démo du scheduler Apollo"""
    print("🚀 Apollo AI Scheduler - DÉMO")
    print("=" * 50)
    
    scheduler = ApolloScheduler()
    
    # Test de planification d'un post
    print("\n📅 Test planification d'un post personnalisé...")
    future_time = datetime.now() + timedelta(minutes=2)
    
    job_id = scheduler.schedule_custom_post(
        gym_id=1,
        platform='instagram',
        post_type='motivation',
        publish_time=future_time
    )
    
    print(f"✅ Post programmé avec ID: {job_id}")
    print(f"⏰ Publication prévue dans 2 minutes: {future_time}")
    
    # Démarrage du scheduler pour la démo
    print("\n🚀 Démarrage du scheduler (5 secondes)...")
    scheduler.start()
    
    # Attendre un peu pour voir les logs
    time.sleep(5)
    
    print(f"\n📋 Posts programmés: {len(scheduler.get_scheduled_posts())}")
    for post in scheduler.get_scheduled_posts():
        print(f"   - {post['platform']} - Gym {post['gym_id']} - {post['scheduled_time']}")
    
    # Arrêt du scheduler
    scheduler.stop()
    print("\n🎉 Démo terminée!")

if __name__ == "__main__":
    demo_scheduler()