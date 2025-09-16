"""
Apollo AI Dashboard
Interface web interactive avec Streamlit pour le marketing automation
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta
import json
import time

from config import APOLLO_GYMS, APOLLO_BRAND
from content_generator import ApolloContentGenerator
from scheduler import ApolloScheduler
from analytics import ApolloAnalytics

# Configuration de la page
st.set_page_config(
    page_title="Apollo AI Marketing Dashboard",
    page_icon="🥊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé Apollo
st.markdown(f"""
<style>
    .main-header {{
        background: linear-gradient(135deg, {APOLLO_BRAND['colors']['primary']}, {APOLLO_BRAND['colors']['secondary']});
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .metric-card {{
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid {APOLLO_BRAND['colors']['primary']};
    }}
    
    .sidebar-logo {{
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 1rem;
        background: {APOLLO_BRAND['colors']['primary']};
        color: white;
        border-radius: 10px;
        margin-bottom: 1rem;
    }}
    
    .recommendation-card {{
        background: #f8f9fa;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid {APOLLO_BRAND['colors']['accent']};
    }}
    
    .stMetric > div > div > div > div {{
        background: {APOLLO_BRAND['colors']['primary']};
        color: white;
    }}
</style>
""", unsafe_allow_html=True)

class ApolloDashboard:
    def __init__(self):
        self.content_generator = ApolloContentGenerator()
        self.scheduler = ApolloScheduler()
        self.analytics = ApolloAnalytics()
        
        # Initialisation du state
        if 'generated_content' not in st.session_state:
            st.session_state.generated_content = []
        if 'scheduled_posts' not in st.session_state:
            st.session_state.scheduled_posts = []
    
    def render_header(self):
        """Affiche l'en-tête principal"""
        st.markdown("""
        <div class="main-header">
            <h1>🥊 Apollo AI Marketing Dashboard</h1>
            <p>Automatisation intelligente du marketing digital pour les 13 salles Apollo</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar(self):
        """Affiche la sidebar avec navigation"""
        with st.sidebar:
            # Logo Apollo
            st.markdown("""
            <div class="sidebar-logo">
                <h2>🥊 Apollo AI</h2>
            </div>
            """, unsafe_allow_html=True)
            
            # Navigation
            page = st.selectbox(
                "Navigation",
                ["📊 Dashboard", "🤖 Content Generator", "📅 Scheduler", "📈 Analytics", "⚙️ Settings"]
            )
            
            # Sélection de salle
            st.markdown("### Sélection de salle")
            selected_gym = st.selectbox(
                "Choisir une salle",
                options=[gym['name'] for gym in APOLLO_GYMS],
                index=0
            )
            
            gym_id = next(gym['id'] for gym in APOLLO_GYMS if gym['name'] == selected_gym)
            
            # Période d'analyse
            st.markdown("### Période d'analyse")
            days = st.slider("Derniers jours", 7, 90, 30)
            
            # Statut en temps réel
            st.markdown("### Statut système")
            st.success("🟢 Content Generator: Actif")
            st.success("🟢 Scheduler: Actif")  
            st.success("🟢 Analytics: Actif")
            
            return page, gym_id, days
    
    def render_overview_dashboard(self, gym_id: int, days: int):
        """Affiche le dashboard principal"""
        st.markdown("## 📊 Vue d'ensemble des performances")
        
        # Récupération des données
        with st.spinner("Chargement des données..."):
            dashboard_data = self.analytics.create_performance_dashboard_data(gym_id, days)
        
        # KPI Cards
        col1, col2, col3, col4 = st.columns(4)
        
        kpis = dashboard_data['kpi_cards']
        
        with col1:
            st.metric(
                "🎯 Reach Total",
                f"{kpis['total_reach']['value']:,}",
                kpis['total_reach']['change']
            )
        
        with col2:
            st.metric(
                "💬 Engagement",
                kpis['total_engagement']['value'],
                kpis['total_engagement']['change']
            )
        
        with col3:
            st.metric(
                "🔥 Leads Générés",
                kpis['total_leads']['value'],
                kpis['total_leads']['change']
            )
        
        with col4:
            st.metric(
                "📈 Taux de Conversion",
                kpis['conversion_rate']['value'],
                kpis['conversion_rate']['change']
            )
        
        # Graphiques
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution de l'engagement
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
                title="Évolution du taux d'engagement",
                xaxis_title="Date",
                yaxis_title="Taux d'engagement",
                template="plotly_white",
                height=400
            )
            
            st.plotly_chart(fig_engagement, use_container_width=True)
        
        with col2:
            # Comparaison des plateformes
            platforms = list(dashboard_data['platform_comparison'].keys())
            reach_values = [dashboard_data['platform_comparison'][p]['total_reach'] for p in platforms]
            
            fig_comparison = px.bar(
                x=[p.capitalize() for p in platforms],
                y=reach_values,
                title="Reach par plateforme",
                color=reach_values,
                color_continuous_scale="Reds"
            )
            
            st.plotly_chart(fig_comparison, use_container_width=True)
        
        # Génération de leads
        st.markdown("### 🎯 Génération de leads par jour")
        
        fig_leads = go.Figure()
        
        for platform, data in dashboard_data['metrics_evolution'].items():
            fig_leads.add_trace(go.Bar(
                x=data['dates'],
                y=data['leads'],
                name=platform.capitalize()
            ))
        
        fig_leads.update_layout(
            title="",
            xaxis_title="Date",
            yaxis_title="Nombre de leads",
            barmode='stack',
            template="plotly_white",
            height=400
        )
        
        st.plotly_chart(fig_leads, use_container_width=True)
        
        # Recommandations IA
        st.markdown("### 💡 Recommandations IA")
        
        for i, rec in enumerate(dashboard_data['recommendations'][:3]):
            priority_color = {
                'high': '#dc3545',
                'medium': '#fd7e14', 
                'low': '#28a745'
            }[rec['priority']]
            
            st.markdown(f"""
            <div style="border-left: 4px solid {priority_color}; padding: 1rem; background: #f8f9fa; margin: 0.5rem 0; border-radius: 5px;">
                <h4 style="margin: 0; color: {priority_color};">[{rec['priority'].upper()}] {rec['title']}</h4>
                <p style="margin: 0.5rem 0;">{rec['description']}</p>
                <small style="color: #28a745;"><strong>Impact attendu:</strong> {rec['expected_impact']}</small>
            </div>
            """, unsafe_allow_html=True)
    
    def render_content_generator(self, gym_id: int):
        """Interface du générateur de contenu"""
        st.markdown("## 🤖 Générateur de Contenu IA")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Génération de contenu personnalisé")
            
            # Formulaire de génération
            with st.form("content_generation"):
                platform = st.selectbox(
                    "Plateforme",
                    ["instagram", "facebook", "linkedin", "tiktok"]
                )
                
                post_type = st.selectbox(
                    "Type de post",
                    ["motivation", "workout_tips", "coach_spotlight", "member_success", 
                     "nutrition", "boxing_techniques", "gym_atmosphere", "special_offers"]
                )
                
                custom_prompt = st.text_area(
                    "Demande personnalisée (optionnel)",
                    placeholder="Ex: Crée un post sur les bienfaits de la boxe pour les femmes..."
                )
                
                submitted = st.form_submit_button("🚀 Générer le contenu")
                
                if submitted:
                    with st.spinner("Génération du contenu IA en cours..."):
                        content = self.content_generator.generate_post_content(
                            gym_id=gym_id,
                            platform=platform,
                            post_type=post_type,
                            custom_prompt=custom_prompt if custom_prompt else None
                        )
                    
                    if content:
                        st.session_state.generated_content.append(content)
                        st.success("✅ Contenu généré avec succès!")
        
        with col2:
            st.markdown("### Génération en lot")
            
            count = st.number_input("Nombre de posts", 1, 50, 5)
            
            if st.button("📦 Générer un lot"):
                with st.spinner(f"Génération de {count} posts..."):
                    batch = self.content_generator.generate_batch_content(
                        gym_ids=[gym_id],
                        count=count
                    )
                
                st.session_state.generated_content.extend(batch)
                st.success(f"✅ {len(batch)} posts générés!")
        
        # Affichage du contenu généré
        if st.session_state.generated_content:
            st.markdown("### 📝 Contenu généré récemment")
            
            for i, content in enumerate(reversed(st.session_state.generated_content[-5:])):
                with st.expander(f"{content['platform'].capitalize()} - {content['type']} - {content['gym']['name']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown("**Contenu:**")
                        st.text_area("", content['content'], height=150, key=f"content_{i}", disabled=True)
                    
                    with col2:
                        st.markdown("**Détails:**")
                        st.write(f"🕐 Heure optimale: {content['optimal_time']}")
                        st.write(f"🏷️ Hashtags: {len(content['hashtags'])}")
                        st.write(f"🖼️ Image: {content['image_suggestion'][:30]}...")
                        
                        if st.button(f"📅 Programmer", key=f"schedule_{i}"):
                            # Redirection vers scheduler
                            st.info("Fonctionnalité de programmation disponible dans l'onglet Scheduler")
    
    def render_scheduler(self, gym_id: int):
        """Interface du scheduler"""
        st.markdown("## 📅 Planificateur de Publications")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### Programmer une publication")
            
            with st.form("schedule_post"):
                platform = st.selectbox(
                    "Plateforme",
                    ["instagram", "facebook", "linkedin", "tiktok"],
                    key="sched_platform"
                )
                
                post_type = st.selectbox(
                    "Type de post",
                    ["motivation", "workout_tips", "coach_spotlight", "member_success"],
                    key="sched_type"
                )
                
                # Sélection de date et heure
                col_date, col_time = st.columns(2)
                with col_date:
                    publish_date = st.date_input("Date de publication", datetime.now().date() + timedelta(days=1))
                with col_time:
                    publish_time = st.time_input("Heure de publication", datetime.now().time())
                
                publish_datetime = datetime.combine(publish_date, publish_time)
                
                submitted = st.form_submit_button("📅 Programmer la publication")
                
                if submitted:
                    if publish_datetime > datetime.now():
                        # Simulation de programmation
                        scheduled_post = {
                            'id': f"sched_{len(st.session_state.scheduled_posts)}",
                            'gym_id': gym_id,
                            'platform': platform,
                            'type': post_type,
                            'scheduled_time': publish_datetime.isoformat(),
                            'status': 'scheduled'
                        }
                        
                        st.session_state.scheduled_posts.append(scheduled_post)
                        st.success(f"✅ Publication programmée pour le {publish_datetime.strftime('%d/%m/%Y à %H:%M')}")
                    else:
                        st.error("❌ La date doit être dans le futur")
        
        with col2:
            st.markdown("### Actions rapides")
            
            if st.button("🔄 Activer auto-posting"):
                st.success("✅ Auto-posting activé!")
            
            if st.button("⏸️ Suspendre auto-posting"):
                st.warning("⏸️ Auto-posting suspendu")
            
            if st.button("📊 Optimiser horaires"):
                st.info("🧠 Optimisation des horaires basée sur l'engagement")
        
        # Liste des publications programmées
        st.markdown("### 📋 Publications programmées")
        
        if st.session_state.scheduled_posts:
            df_scheduled = pd.DataFrame(st.session_state.scheduled_posts)
            
            for i, post in enumerate(st.session_state.scheduled_posts):
                col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 2, 1])
                
                with col1:
                    st.write(f"**{post['platform'].capitalize()}**")
                
                with col2:
                    st.write(post['type'])
                
                with col3:
                    scheduled_time = datetime.fromisoformat(post['scheduled_time'])
                    st.write(scheduled_time.strftime('%d/%m/%Y %H:%M'))
                
                with col4:
                    status_color = {'scheduled': '🟡', 'published': '🟢', 'failed': '🔴'}
                    st.write(f"{status_color.get(post['status'], '⚪')} {post['status'].capitalize()}")
                
                with col5:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.scheduled_posts.remove(post)
                        st.rerun()
        else:
            st.info("Aucune publication programmée")
    
    def render_analytics(self, gym_id: int, days: int):
        """Interface d'analytics avancées"""
        st.markdown("## 📈 Analytics Avancées")
        
        # Génération du rapport complet
        with st.spinner("Génération du rapport d'analyse..."):
            report = self.analytics.generate_performance_report(gym_id, days)
        
        # Résumé exécutif
        st.markdown("### 📋 Résumé Exécutif")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"**Leads générés:** {report['summary']['total_leads_generated']}")
        
        with col2:
            st.info(f"**Engagement moyen:** {report['summary']['average_engagement_rate']:.2%}")
        
        with col3:
            st.info(f"**Reach total:** {report['summary']['total_reach']:,}")
        
        # Analyse par plateforme
        st.markdown("### 🔍 Analyse par Plateforme")
        
        tabs = st.tabs([platform.capitalize() for platform in report['platforms'].keys()])
        
        for i, (platform, data) in enumerate(report['platforms'].items()):
            with tabs[i]:
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Métriques Clés:**")
                    for metric in data['key_metrics']:
                        trend_icon = {'up': '📈', 'down': '📉', 'stable': '➡️'}
                        st.write(f"{metric['name']}: {metric['current_value']:.2f} {trend_icon[metric['trend']]}")
                
                with col2:
                    st.markdown("**Objectifs:**")
                    for goal, status in data['goals_status'].items():
                        status_icon = {'achieved': '✅', 'below_target': '❌'}
                        st.write(f"{goal}: {status_icon[status['status']]} ({status['gap_percent']:+.1f}%)")
        
        # Graphiques détaillés
        st.markdown("### 📊 Graphiques Détaillés")
        
        dashboard_data = self.analytics.create_performance_dashboard_data(gym_id, days)
        charts = self.analytics.create_performance_charts(dashboard_data)
        
        for chart_name, chart in charts.items():
            st.plotly_chart(chart, use_container_width=True)
        
        # Export de rapport
        st.markdown("### 📥 Export de Données")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📄 Télécharger Rapport JSON"):
                filepath = self.analytics.export_report_to_json(report)
                st.success(f"Rapport sauvegardé: {filepath}")
        
        with col2:
            if st.button("📊 Télécharger Données CSV"):
                # Simulation d'export CSV
                st.success("Données CSV exportées!")
    
    def render_settings(self):
        """Interface de configuration"""
        st.markdown("## ⚙️ Configuration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔑 Configuration API")
            
            openai_key = st.text_input("Clé OpenAI", type="password", placeholder="sk-...")
            instagram_token = st.text_input("Token Instagram", type="password")
            facebook_token = st.text_input("Token Facebook", type="password")
            
            if st.button("💾 Sauvegarder Configuration"):
                st.success("✅ Configuration sauvegardée!")
        
        with col2:
            st.markdown("### 📊 Préférences")
            
            default_platform = st.selectbox("Plateforme par défaut", ["instagram", "facebook", "linkedin"])
            auto_post = st.checkbox("Auto-posting activé", True)
            notifications = st.checkbox("Notifications email", True)
            
            st.markdown("### 🎨 Personnalisation")
            brand_color = st.color_picker("Couleur principale", APOLLO_BRAND['colors']['primary'])
        
        # Statut du système
        st.markdown("### 📡 Statut du Système")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Content Generator", "✅ Actif", "100%")
        
        with col2:
            st.metric("Scheduler", "✅ Actif", "12 tâches")
        
        with col3:
            st.metric("Analytics", "✅ Actif", "Real-time")

def main():
    """Fonction principale de l'application"""
    dashboard = ApolloDashboard()
    
    # Rendu de l'interface
    dashboard.render_header()
    page, gym_id, days = dashboard.render_sidebar()
    
    # Navigation
    if page == "📊 Dashboard":
        dashboard.render_overview_dashboard(gym_id, days)
    elif page == "🤖 Content Generator":
        dashboard.render_content_generator(gym_id)
    elif page == "📅 Scheduler":
        dashboard.render_scheduler(gym_id)
    elif page == "📈 Analytics":
        dashboard.render_analytics(gym_id, days)
    elif page == "⚙️ Settings":
        dashboard.render_settings()
    
    # Footer
    st.markdown("---")
    st.markdown("🥊 **Apollo AI Marketing Toolkit** - Powered by OpenAI & Streamlit")

if __name__ == "__main__":
    main()