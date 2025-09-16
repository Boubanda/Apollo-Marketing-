"""
Configuration centrale pour Apollo AI Marketing Toolkit
Toutes les clés API, paramètres et données de base
"""

import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# =============================================================================
# CONFIGURATION API
# =============================================================================

# OpenAI Configuration
OPENAI_CONFIG = {
    'api_key': os.getenv('OPENAI_API_KEY', ''),
    'model': 'gpt-3.5-turbo',
    'max_tokens': 1000,
    'temperature': 0.7
}

# Social Media APIs
SOCIAL_MEDIA_CONFIG = {
    'instagram': {
        'username': os.getenv('INSTAGRAM_USERNAME', ''),
        'password': os.getenv('INSTAGRAM_PASSWORD', ''),
        'access_token': os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
    },
    'facebook': {
        'app_id': os.getenv('FACEBOOK_APP_ID', ''),
        'app_secret': os.getenv('FACEBOOK_APP_SECRET', ''),
        'access_token': os.getenv('FACEBOOK_ACCESS_TOKEN', '')
    },
    'linkedin': {
        'client_id': os.getenv('LINKEDIN_CLIENT_ID', ''),
        'client_secret': os.getenv('LINKEDIN_CLIENT_SECRET', ''),
        'access_token': os.getenv('LINKEDIN_ACCESS_TOKEN', '')
    },
    'tiktok': {
        'app_id': os.getenv('TIKTOK_APP_ID', ''),
        'app_secret': os.getenv('TIKTOK_APP_SECRET', ''),
        'access_token': os.getenv('TIKTOK_ACCESS_TOKEN', '')
    }
}

# =============================================================================
# DONNÉES APOLLO SPORTING CLUB
# =============================================================================

APOLLO_GYMS = [
    {
        'id': 1,
        'name': 'Apollo Bastille',
        'address': '15 rue de la Roquette, 75011 Paris',
        'arrondissement': '11e',
        'phone': '01 43 57 89 12',
        'email': 'bastille@apollosportingclub.com',
        'specialties': ['Boxe', 'CrossFit', 'HIIT', 'Musculation'],
        'coaches': ['Sarah Martinez', 'Mike Johnson', 'Julie Dubois'],
        'capacity': 50,
        'opening_hours': {
            'monday': '06:00-23:00',
            'tuesday': '06:00-23:00',
            'wednesday': '06:00-23:00',
            'thursday': '06:00-23:00',
            'friday': '06:00-23:00',
            'saturday': '08:00-20:00',
            'sunday': '09:00-19:00'
        },
        'instagram_handle': '@apollo_bastille',
        'hashtags': ['#ApolloBastille', '#BoxeParis11', '#FitnessBastille']
    },
    {
        'id': 2,
        'name': 'Apollo Châtelet',
        'address': '8 rue du Pont Neuf, 75001 Paris',
        'arrondissement': '1er',
        'phone': '01 42 36 78 94',
        'email': 'chatelet@apollosportingclub.com',
        'specialties': ['Boxe', 'Fitness', 'Yoga', 'Pilates'],
        'coaches': ['Alex Chen', 'Emma Rousseau', 'David Lopez'],
        'capacity': 40,
        'opening_hours': {
            'monday': '06:30-22:30',
            'tuesday': '06:30-22:30',
            'wednesday': '06:30-22:30',
            'thursday': '06:30-22:30',
            'friday': '06:30-22:30',
            'saturday': '09:00-19:00',
            'sunday': '10:00-18:00'
        },
        'instagram_handle': '@apollo_chatelet',
        'hashtags': ['#ApolloChatelet', '#BoxeParis1', '#FitnessChatelet']
    },
    {
        'id': 3,
        'name': 'Apollo Montmartre',
        'address': '25 rue des Martyrs, 75009 Paris',
        'arrondissement': '9e',
        'phone': '01 48 78 45 23',
        'email': 'montmartre@apollosportingclub.com',
        'specialties': ['Boxe', 'Musculation', 'Cardio', 'TRX'],
        'coaches': ['Tom Wilson', 'Lisa Martin', 'Marc Fontaine'],
        'capacity': 35,
        'opening_hours': {
            'monday': '07:00-22:00',
            'tuesday': '07:00-22:00',
            'wednesday': '07:00-22:00',
            'thursday': '07:00-22:00',
            'friday': '07:00-22:00',
            'saturday': '09:00-18:00',
            'sunday': '10:00-17:00'
        },
        'instagram_handle': '@apollo_montmartre',
        'hashtags': ['#ApolloMontmartre', '#BoxeParis9', '#FitnessMontmartre']
    },
    {
        'id': 4,
        'name': 'Apollo Boulogne',
        'address': '12 avenue Jean Baptiste Clément, 92100 Boulogne-Billancourt',
        'arrondissement': 'Boulogne',
        'phone': '01 46 05 78 91',
        'email': 'boulogne@apollosportingclub.com',
        'specialties': ['Boxe', 'TRX', 'Pilates', 'Coaching Personnel'],
        'coaches': ['Sophie Laurent', 'Kevin Moreau', 'Marine Petit'],
        'capacity': 60,
        'opening_hours': {
            'monday': '06:00-23:00',
            'tuesday': '06:00-23:00',
            'wednesday': '06:00-23:00',
            'thursday': '06:00-23:00',
            'friday': '06:00-23:00',
            'saturday': '08:00-20:00',
            'sunday': '09:00-19:00'
        },
        'instagram_handle': '@apollo_boulogne',
        'hashtags': ['#ApolloBoulogne', '#BoxeBoulogne', '#FitnessBoulogne']
    }
]

# =============================================================================
# CONFIGURATION CONTENT GENERATION
# =============================================================================

CONTENT_CONFIG = {
    'post_types': [
        'motivation',
        'workout_tips',
        'coach_spotlight',
        'member_success',
        'nutrition',
        'boxing_techniques',
        'gym_atmosphere',
        'class_schedule',
        'special_offers'
    ],
    'platforms': {
        'instagram': {
            'max_char': 2200,
            'image_size': (1080, 1080),
            'optimal_hashtags': 25,
            'best_times': ['07:00', '12:00', '19:00']
        },
        'facebook': {
            'max_char': 63206,
            'image_size': (1200, 630),
            'optimal_hashtags': 3,
            'best_times': ['09:00', '13:00', '15:00']
        },
        'linkedin': {
            'max_char': 1300,
            'image_size': (1200, 627),
            'optimal_hashtags': 5,
            'best_times': ['08:00', '12:00', '17:00']
        },
        'tiktok': {
            'max_char': 150,
            'video_duration': 60,
            'optimal_hashtags': 5,
            'best_times': ['06:00', '10:00', '19:00']
        }
    }
}

# =============================================================================
# BRAND IDENTITY
# =============================================================================

APOLLO_BRAND = {
    'colors': {
        'primary': '#DC2626',      # Rouge Apollo
        'secondary': '#991B1B',    # Rouge foncé
        'accent': '#F59E0B',       # Jaune/Orange
        'dark': '#1F2937',         # Gris foncé
        'light': '#F9FAFB'         # Blanc cassé
    },
    'fonts': {
        'primary': 'Inter',
        'secondary': 'Roboto',
        'accent': 'Montserrat'
    },
    'tone': {
        'style': 'moderne, dynamique, motivant',
        'voice': 'expert mais accessible',
        'personality': 'passionné, bienveillant, déterminé'
    },
    'values': [
        'Excellence',
        'Dépassement de soi',
        'Communauté',
        'Innovation',
        'Bien-être'
    ]
}

# =============================================================================
# TEMPLATES DE POSTS
# =============================================================================

POST_TEMPLATES = {
    'motivation': [
        "🔥 {motivation_quote}\n\n💪 Chez Apollo {gym_name}, on croit que {personal_message}\n\n📍 Rejoins-nous : {address}\n\n{hashtags}",
        "⚡ Lundi = nouveau départ !\n\n{workout_motivation}\n\n🥊 Rendez-vous chez Apollo {gym_name} pour {activity}\n\n{hashtags}",
        "🌟 {success_story}\n\n💯 C'est ça l'esprit Apollo !\n\n📲 Réserve ton cours : {phone}\n\n{hashtags}"
    ],
    'workout_tips': [
        "💡 CONSEIL PRO : {tip_title}\n\n{tip_content}\n\n👨‍🏫 Par {coach_name}, coach chez Apollo {gym_name}\n\n{hashtags}",
        "🎯 TECHNIQUE DU JOUR : {technique}\n\n{explanation}\n\n🥊 Viens l'apprendre avec nous !\n\n{hashtags}",
        "⚠️ ERREUR À ÉVITER : {common_mistake}\n\n✅ LA BONNE FAÇON : {correct_way}\n\n📚 Plus de conseils chez Apollo {gym_name}\n\n{hashtags}"
    ]
}

# =============================================================================
# CONFIGURATION ANALYTICS
# =============================================================================

ANALYTICS_CONFIG = {
    'metrics': [
        'engagement_rate',
        'reach',
        'impressions',
        'likes',
        'comments',
        'shares',
        'saves',
        'click_through_rate',
        'conversion_rate',
        'lead_generation'
    ],
    'goals': {
        'instagram': {
            'followers_growth': 0.05,  # +5% par mois
            'engagement_rate': 0.08,   # 8% minimum
            'weekly_posts': 5
        },
        'facebook': {
            'reach_growth': 0.10,      # +10% par mois
            'engagement_rate': 0.06,   # 6% minimum
            'weekly_posts': 3
        }
    }
}

# =============================================================================
# CONFIGURATION AUTOMATION
# =============================================================================

AUTOMATION_CONFIG = {
    'posting_schedule': {
        'monday': [
            {'time': '07:00', 'platform': 'instagram', 'type': 'motivation'},
            {'time': '12:00', 'platform': 'facebook', 'type': 'workout_tips'},
            {'time': '19:00', 'platform': 'linkedin', 'type': 'coach_spotlight'}
        ],
        'tuesday': [
            {'time': '08:00', 'platform': 'instagram', 'type': 'workout_tips'},
            {'time': '17:00', 'platform': 'tiktok', 'type': 'boxing_techniques'}
        ],
        # ... autres jours
    },
    'auto_responses': {
        'keywords': {
            'prix': "Nos tarifs varient selon la formule choisie. Contacte-nous au {phone} pour une offre personnalisée ! 💪",
            'horaires': "Nous sommes ouverts {opening_hours}. Retrouve tous nos créneaux sur apollosportingclub.com 📅",
            'essai': "Premier cours gratuit ! Viens tester notre ambiance unique 🔥 Réserve : {phone}"
        }
    }
}