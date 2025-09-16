"""
Apollo AI Analytics
Analyse des performances marketing et génération de insights IA
"""

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json
import random
from dataclasses import dataclass
from typing import Dict, List, Optional

from config import APOLLO_GYMS, ANALYTICS_CONFIG

@dataclass
class PerformanceMetric:
    """Classe pour représenter une métrique de performance"""
    name: str
    value: float
    target: float
    trend: str  # 'up', 'down', 'stable'
    platform: str
    gym_id: int
    date: datetime

class ApolloAnalytics:
    def __init__(self):
        self.metrics_config = ANALYTICS_CONFIG['metrics']
        self.goals = ANALYTICS_CONFIG['goals']
        self.data_cache = {}
        
    def collect_platform_metrics(self, platform: str, gym_id: int = None, days: int = 30) -> pd.DataFrame:
        """Collecte les métriques d'une plateforme"""
        print(f"📊 Collecte des métriques {platform} (derniers {days} jours)")
        
        # En production, connecter aux APIs des plateformes
        # Ici, simulation de données réalistes
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Génération de données simulées mais cohérentes
        base_followers = 15000 if gym_id == 1 else random.randint(8000, 12000)
        
        metrics_data = []
        for date in dates:
            daily_data = self._generate_realistic_daily_metrics(platform, base_followers, date)
            daily_data['gym_id'] = gym_id or 1
            daily_data['date'] = date
            metrics_data.append(daily_data)
        
        df = pd.DataFrame(metrics_data)
        return df
    
    def _generate_realistic_daily_metrics(self, platform: str, base_followers: int, date: datetime) -> Dict:
        """Génère des métriques quotidiennes réalistes"""
        # Variation selon le jour de la semaine
        weekday_multiplier = {0: 1.2, 1: 1.1, 2: 1.0, 3: 1.1, 4: 1.3, 5: 1.4, 6: 0.8}
        day_mult = weekday_multiplier.get(date.weekday(), 1.0)
        
        # Base metrics selon la plateforme
        if platform == 'instagram':
            base_metrics = {
                'followers': base_followers + random.randint(-5, 15),
                'posts': random.randint(1, 3),
                'likes': int(base_followers * 0.08 * day_mult * random.uniform(0.7, 1.3)),
                'comments': int(base_followers * 0.01 * day_mult * random.uniform(0.5, 1.5)),
                'saves': int(base_followers * 0.02 * day_mult * random.uniform(0.3, 1.2)),
                'shares': int(base_followers * 0.005 * day_mult * random.uniform(0.5, 1.8)),
                'reach': int(base_followers * 1.5 * day_mult * random.uniform(0.8, 1.4)),
                'impressions': int(base_followers * 2.2 * day_mult * random.uniform(0.9, 1.6))
            }
        elif platform == 'facebook':
            base_metrics = {
                'followers': base_followers + random.randint(-3, 10),
                'posts': random.randint(0, 2),
                'likes': int(base_followers * 0.06 * day_mult * random.uniform(0.6, 1.2)),
                'comments': int(base_followers * 0.008 * day_mult * random.uniform(0.4, 1.3)),
                'shares': int(base_followers * 0.015 * day_mult * random.uniform(0.3, 1.5)),
                'reach': int(base_followers * 1.2 * day_mult * random.uniform(0.7, 1.3)),
                'impressions': int(base_followers * 1.8 * day_mult * random.uniform(0.8, 1.5))
            }
        else:  # linkedin, tiktok
            base_metrics = {
                'followers': base_followers + random.randint(-2, 8),
                'posts': random.randint(0, 1),
                'likes': int(base_followers * 0.04 * day_mult * random.uniform(0.5, 1.1)),
                'comments': int(base_followers * 0.006 * day_mult * random.uniform(0.3, 1.0)),
                'shares': int(base_followers * 0.01 * day_mult * random.uniform(0.2, 1.2)),
                'reach': int(base_followers * 0.8 * day_mult * random.uniform(0.6, 1.2)),
                'impressions': int(base_followers * 1.3 * day_mult * random.uniform(0.7, 1.4))
            }
        
        # Calcul des métriques dérivées
        total_engagement = base_metrics['likes'] + base_metrics['comments'] + base_metrics['shares']
        base_metrics['engagement_rate'] = total_engagement / max(base_metrics['reach'], 1)
        base_metrics['ctr'] = total_engagement / max(base_metrics['impressions'], 1)
        
        # Métriques business
        base_metrics['leads_generated'] = random.randint(0, 5) if random.random() > 0.6 else 0
        base_metrics['website_clicks'] = random.randint(5, 25)
        base_metrics['phone_calls'] = random.randint(0, 3) if random.random() > 0.7 else 0
        
        return base_metrics
    
    def analyze_performance_trends(self, df: pd.DataFrame, metric: str) -> Dict:
        """Analyse les tendances d'une métrique"""
        if len(df) < 7:
            return {'trend': 'insufficient_data', 'change': 0}
        
        # Calcul de la tendance sur les 7 derniers jours
        recent_avg = df[metric].tail(7).mean()
        previous_avg = df[metric].iloc[-14:-7].mean() if len(df) >= 14 else df[metric].head(7).mean()
        
        change = (recent_avg - previous_avg) / previous_avg * 100 if previous_avg > 0 else 0
        
        if abs(change) < 5:
            trend = 'stable'
        elif change > 0:
            trend = 'up'
        else:
            trend = 'down'
        
        return {
            'trend': trend,
            'change': change,
            'recent_avg': recent_avg,
            'previous_avg': previous_avg
        }
    
    def generate_performance_report(self, gym_id: int = None, days: int = 30) -> Dict:
        """Génère un rapport de performance complet"""
        print(f"📋 Génération du rapport de performance (derniers {days} jours)")
        
        platforms = ['instagram', 'facebook', 'linkedin']
        report = {
            'period': f'{days} derniers jours',
            'generated_at': datetime.now().isoformat(),
            'gym_id': gym_id,
            'platforms': {},
            'summary': {},
            'recommendations': []
        }
        
        all_metrics = []
        
        for platform in platforms:
            df = self.collect_platform_metrics(platform, gym_id, days)
            platform_analysis = self.analyze_platform_performance(df, platform)
            report['platforms'][platform] = platform_analysis
            
            # Collecte pour le résumé global
            all_metrics.extend(platform_analysis['key_metrics'])
        
        # Génération du résumé global
        report['summary'] = self.generate_summary_insights(all_metrics, days)
        
        # Recommandations IA
        report['recommendations'] = self.generate_ai_recommendations(report['platforms'])
        
        return report
    
    def analyze_platform_performance(self, df: pd.DataFrame, platform: str) -> Dict:
        """Analyse la performance d'une plateforme spécifique"""
        key_metrics = ['engagement_rate', 'reach', 'followers', 'leads_generated']
        
        analysis = {
            'platform': platform,
            'total_posts': df['posts'].sum(),
            'avg_daily_reach': df['reach'].mean(),
            'total_leads': df['leads_generated'].sum(),
            'key_metrics': [],
            'trends': {},
            'goals_status': {}
        }
        
        # Analyse des métriques clés
        for metric in key_metrics:
            if metric in df.columns:
                trend_data = self.analyze_performance_trends(df, metric)
                
                metric_info = {
                    'name': metric,
                    'current_value': df[metric].iloc[-1] if len(df) > 0 else 0,
                    'average': df[metric].mean(),
                    'trend': trend_data['trend'],
                    'change_percent': trend_data['change']
                }
                
                analysis['key_metrics'].append(metric_info)
                analysis['trends'][metric] = trend_data
        
        # Vérification des objectifs
        platform_goals = self.goals.get(platform, {})
        for goal_name, goal_value in platform_goals.items():
            if goal_name in df.columns:
                current_performance = df[goal_name].mean()
                status = 'achieved' if current_performance >= goal_value else 'below_target'
                gap = ((current_performance - goal_value) / goal_value * 100) if goal_value > 0 else 0
                
                analysis['goals_status'][goal_name] = {
                    'target': goal_value,
                    'current': current_performance,
                    'status': status,
                    'gap_percent': gap
                }
        
        return analysis
    
    def generate_summary_insights(self, all_metrics: List, days: int) -> Dict:
        """Génère des insights de résumé global"""
        # Calculs des totaux
        total_leads = sum([m['current_value'] for m in all_metrics if m['name'] == 'leads_generated'])
        avg_engagement = np.mean([m['average'] for m in all_metrics if m['name'] == 'engagement_rate'])
        total_reach = sum([m['current_value'] for m in all_metrics if m['name'] == 'reach'])
        
        # Identification des points forts et faibles
        strong_metrics = [m for m in all_metrics if m['trend'] == 'up' and m['change_percent'] > 10]
        weak_metrics = [m for m in all_metrics if m['trend'] == 'down' and m['change_percent'] < -10]
        
        return {
            'total_leads_generated': total_leads,
            'average_engagement_rate': round(avg_engagement, 4),
            'total_reach': int(total_reach),
            'leads_per_day': round(total_leads / days, 2),
            'strong_performing_metrics': len(strong_metrics),
            'underperforming_metrics': len(weak_metrics),
            'top_performing_metric': max(strong_metrics, key=lambda x: x['change_percent'], default=None),
            'most_concerning_metric': min(weak_metrics, key=lambda x: x['change_percent'], default=None)
        }
    
    def generate_ai_recommendations(self, platforms_data: Dict) -> List[Dict]:
        """Génère des recommandations basées sur l'analyse IA"""
        recommendations = []
        
        for platform, data in platforms_data.items():
            # Analyse des tendances pour recommandations
            for metric_info in data['key_metrics']:
                metric = metric_info['name']
                trend = metric_info['trend']
                change = metric_info['change_percent']
                
                if metric == 'engagement_rate' and trend == 'down':
                    recommendations.append({
                        'platform': platform,
                        'type': 'optimization',
                        'priority': 'high' if change < -15 else 'medium',
                        'title': 'Améliorer l\'engagement',
                        'description': f'Le taux d\'engagement sur {platform} a baissé de {abs(change):.1f}%. Recommandations: varier les types de contenu, poser plus de questions, utiliser des stories interactives.',
                        'expected_impact': '+15-25% engagement'
                    })
                
                elif metric == 'leads_generated' and metric_info['current_value'] < 5:
                    recommendations.append({
                        'platform': platform,
                        'type': 'conversion',
                        'priority': 'high',
                        'title': 'Optimiser la génération de leads',
                        'description': f'Peu de leads générés via {platform}. Ajouter plus de call-to-action, créer du contenu éducatif, utiliser les formulaires de contact intégrés.',
                        'expected_impact': '+40-60% leads'
                    })
                
                elif metric == 'reach' and trend == 'up' and change > 20:
                    recommendations.append({
                        'platform': platform,
                        'type': 'scaling',
                        'priority': 'medium',
                        'title': 'Capitaliser sur la croissance',
                        'description': f'Excellente croissance de reach (+{change:.1f}%). Moment idéal pour intensifier le contenu et lancer des campagnes payantes.',
                        'expected_impact': '+30-50% reach'
                    })
        
        # Recommandations globales
        if len(recommendations) == 0:
            recommendations.append({
                'platform': 'all',
                'type': 'maintenance',
                'priority': 'low',
                'title': 'Continuer la stratégie actuelle',
                'description': 'Les performances sont stables. Maintenir la qualité du contenu et tester de nouveaux formats occasionnellement.',
                'expected_impact': 'Maintien des performances'
            })
        
        return sorted(recommendations, key=lambda x: {'high': 3, 'medium': 2, 'low': 1}[x['priority']], reverse=True)
    
    def create_performance_dashboard_data(self, gym_id: int = None, days: int = 30) -> Dict:
        """Prépare les données pour le dashboard Streamlit"""
        platforms = ['instagram', 'facebook', 'linkedin']
        dashboard_data = {
            'metrics_evolution': {},
            'platform_comparison': {},
            'kpi_cards': {},
            'recommendations': []
        }
        
        # Collecte des données pour chaque plateforme
        for platform in platforms:
            df = self.collect_platform_metrics(platform, gym_id, days)
            
            # Évolution temporelle des métriques clés
            dashboard_data['metrics_evolution'][platform] = {
                'dates': df['date'].dt.strftime('%Y-%m-%d').tolist(),
                'engagement_rate': df['engagement_rate'].tolist(),
                'reach': df['reach'].tolist(),
                'leads': df['leads_generated'].tolist()
            }
            
            # Métriques pour comparaison
            dashboard_data['platform_comparison'][platform] = {
                'total_reach': df['reach'].sum(),
                'avg_engagement': df['engagement_rate'].mean(),
                'total_leads': df['leads_generated'].sum(),
                'total_posts': df['posts'].sum()
            }
        
        # KPI Cards
        all_data = pd.concat([
            self.collect_platform_metrics(p, gym_id, days) for p in platforms
        ])
        
        dashboard_data['kpi_cards'] = {
            'total_reach': {
                'value': int(all_data['reach'].sum()),
                'change': '+12.5%',
                'trend': 'up'
            },
            'total_engagement': {
                'value': f"{all_data['engagement_rate'].mean():.2%}",
                'change': '+3.2%',
                'trend': 'up'
            },
            'total_leads': {
                'value': int(all_data['leads_generated'].sum()),
                'change': '+28.1%',
                'trend': 'up'
            },
            'conversion_rate': {
                'value': f"{(all_data['leads_generated'].sum() / all_data['website_clicks'].sum() * 100):.1f}%",
                'change': '+5.7%',
                'trend': 'up'
            }
        }
        
        # Recommandations
        report = self.generate_performance_report(gym_id, days)
        dashboard_data['recommendations'] = report['recommendations']
        
        return dashboard_data
    
    def export_report_to_json(self, report: Dict, filename: str = None) -> str:
        """Exporte un rapport en JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"apollo_report_{timestamp}.json"
        
        filepath = f"data/analytics_data/{filename}"
        
        # Créer le dossier s'il n'existe pas
        import os
        os.makedirs('data/analytics_data', exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False, default=str)
        
        return filepath
    
    def create_performance_charts(self, dashboard_data: Dict) -> Dict[str, go.Figure]:
        """Crée les graphiques pour le dashboard"""
        charts = {}
        
        # 1. Évolution de l'engagement par plateforme
        fig_engagement = go.Figure()
        
        for platform, data in dashboard_data['metrics_evolution'].items():
            fig_engagement.add_trace(go.Scatter(
                x=data['dates'],
                y=data['engagement_rate'],
                mode='lines+markers',
                name=platform.capitalize(),
                line=dict(width=3)
            ))
        
        fig_engagement.update_layout(
            title='Évolution du taux d\'engagement',
            xaxis_title='Date',
            yaxis_title='Taux d\'engagement',
            template='plotly_white',
            height=400
        )
        charts['engagement_evolution'] = fig_engagement
        
        # 2. Comparaison des plateformes (reach total)
        platforms = list(dashboard_data['platform_comparison'].keys())
        reach_values = [dashboard_data['platform_comparison'][p]['total_reach'] for p in platforms]
        
        fig_comparison = px.bar(
            x=[p.capitalize() for p in platforms],
            y=reach_values,
            title='Reach total par plateforme',
            color=reach_values,
            color_continuous_scale='Reds'
        )
        charts['platform_comparison'] = fig_comparison
        
        # 3. Génération de leads par jour
        fig_leads = go.Figure()
        
        for platform, data in dashboard_data['metrics_evolution'].items():
            fig_leads.add_trace(go.Bar(
                x=data['dates'],
                y=data['leads'],
                name=platform.capitalize()
            ))
        
        fig_leads.update_layout(
            title='Leads générés par jour',
            xaxis_title='Date',
            yaxis_title='Nombre de leads',
            barmode='stack',
            template='plotly_white',
            height=400
        )
        charts['leads_generation'] = fig_leads
        
        return charts

# =============================================================================
# FONCTION DE DÉMONSTRATION
# =============================================================================

def demo_analytics():
    """Démo du système d'analytics Apollo"""
    print("🚀 Apollo AI Analytics - DÉMO")
    print("=" * 50)
    
    analytics = ApolloAnalytics()
    
    # Test de collecte de métriques
    print("\n📊 Test collecte de métriques Instagram (derniers 7 jours)...")
    df = analytics.collect_platform_metrics('instagram', gym_id=1, days=7)
    
    print(f"✅ {len(df)} jours de données collectées")
    print(f"📈 Reach moyen: {df['reach'].mean():.0f}")
    print(f"💬 Engagement moyen: {df['engagement_rate'].mean():.2%}")
    print(f"🎯 Total leads: {df['leads_generated'].sum()}")
    
    # Test de génération de rapport
    print(f"\n📋 Génération du rapport de performance complet...")
    report = analytics.generate_performance_report(gym_id=1, days=14)
    
    print(f"✅ Rapport généré pour {len(report['platforms'])} plateformes")
    print(f"📊 Résumé: {report['summary']['total_leads_generated']} leads générés")
    print(f"💡 {len(report['recommendations'])} recommandations")
    
    # Affichage des recommandations
    print(f"\n🎯 Top 3 recommandations:")
    for i, rec in enumerate(report['recommendations'][:3], 1):
        print(f"{i}. [{rec['priority'].upper()}] {rec['title']}")
        print(f"   {rec['description'][:100]}...")
        print(f"   Impact attendu: {rec['expected_impact']}")
    
    # Sauvegarde du rapport
    filepath = analytics.export_report_to_json(report)
    print(f"\n💾 Rapport sauvegardé: {filepath}")
    
    # Test des données dashboard
    print(f"\n📱 Préparation des données dashboard...")
    dashboard_data = analytics.create_performance_dashboard_data(gym_id=1, days=7)
    
    print(f"✅ Données dashboard préparées:")
    for platform in dashboard_data['platform_comparison']:
        comp = dashboard_data['platform_comparison'][platform]
        print(f"   {platform.capitalize()}: {comp['total_reach']:,} reach, {comp['total_leads']} leads")
    
    print(f"\n🎉 Démo analytics terminée!")

if __name__ == "__main__":
    demo_analytics()