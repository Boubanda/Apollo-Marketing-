"""
Apollo AI Content Generator
Génération intelligente de posts, images et vidéos pour les réseaux sociaux
Support OpenAI + Ollama (IA locale gratuite)
"""

from openai import OpenAI
import requests
import random
import json
import os
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont

from config import (
    OPENAI_CONFIG, APOLLO_GYMS, CONTENT_CONFIG, 
    APOLLO_BRAND, POST_TEMPLATES
)

class ApolloContentGenerator:
    def __init__(self):
        # Configuration du provider IA (OpenAI ou Ollama)
        self.ai_provider = os.getenv('AI_PROVIDER', 'ollama')  # Par défaut Ollama
        
        if self.ai_provider == 'openai':
            self.client = OpenAI(api_key=OPENAI_CONFIG['api_key'])
            print("🤖 Utilisation d'OpenAI GPT")
        else:
            self.ollama_url = os.getenv('OLLAMA_URL', 'http://localhost:11434')
            self.ollama_model = os.getenv('OLLAMA_MODEL', 'llama2:7b-chat')
            print(f"🦙 Utilisation d'Ollama - Modèle: {self.ollama_model}")
        
        self.brand = APOLLO_BRAND
        self.templates = POST_TEMPLATES
        
    def generate_post_content(self, gym_id, platform, post_type, custom_prompt=None):
        """
        Génère le contenu d'un post personnalisé pour une salle Apollo
        """
        gym = self.get_gym_by_id(gym_id)
        platform_config = CONTENT_CONFIG['platforms'][platform]
        
        # Construction du prompt personnalisé
        prompt = self.build_content_prompt(gym, platform, post_type, custom_prompt)
        
        try:
            # Génération selon le provider configuré
            if self.ai_provider == 'openai':
                content = self._generate_with_openai(prompt)
            else:
                content = self._generate_with_ollama(prompt)
            
            if not content:
                return None
            
            # Post-processing selon la plateforme
            content = self.format_for_platform(content, platform, gym)
            
            return {
                'content': content,
                'gym': gym,
                'platform': platform,
                'type': post_type,
                'generated_at': datetime.now().isoformat(),
                'hashtags': self.generate_hashtags(gym, post_type, platform),
                'optimal_time': self.get_optimal_posting_time(platform),
                'image_suggestion': self.suggest_image_concept(post_type, gym),
                'ai_provider': self.ai_provider
            }
            
        except Exception as e:
            print(f"Erreur génération contenu: {e}")
            return None
    
    def _generate_with_openai(self, prompt):
        """Génération avec OpenAI GPT"""
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_CONFIG.get('model', 'gpt-4o-mini'),  # Modèle moins cher par défaut
                messages=[
                    {"role": "system", "content": self.get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=OPENAI_CONFIG.get('max_tokens', 500),
                temperature=OPENAI_CONFIG.get('temperature', 0.7)
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Erreur OpenAI: {e}")
            return None
    
    def _generate_with_ollama(self, prompt):
        """Génération avec Ollama (gratuit, local)"""
        try:
            system_prompt = self.get_system_prompt()
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\n\nAssistant:"
            
            response = requests.post(
                f'{self.ollama_url}/api/generate',
                json={
                    'model': self.ollama_model,
                    'prompt': full_prompt,
                    'stream': False,
                    'options': {
                        'temperature': 0.7,
                        'top_p': 0.9,
                        'max_tokens': 500
                    }
                },
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                print(f"Erreur Ollama: {response.status_code} - {response.text}")
                return None
                
        except requests.exceptions.ConnectionError:
            print("❌ Ollama non disponible. Lancez: ollama serve")
            return None
        except Exception as e:
            print(f"Erreur Ollama: {e}")
            return None
    
    def get_system_prompt(self):
        """Prompt système pour définir le rôle de l'IA"""
        return f"""Tu es le responsable marketing digital d'Apollo Sporting Club, un réseau premium de 13 salles de boxe et fitness à Paris.

IDENTITÉ DE MARQUE:
- Couleurs: Rouge passion #{self.brand['colors']['primary'][1:]}, moderne et énergique
- Ton: {self.brand['tone']['style']}, {self.brand['tone']['voice']}
- Valeurs: {', '.join(self.brand['values'])}

MISSION:
- Créer du contenu engageant qui convertit les prospects en membres
- Mettre en valeur l'expertise de nos coachs et l'ambiance unique
- Générer des leads qualifiés pour chaque salle

STYLE:
- Utilise des emojis pertinents (🥊💪🔥⚡🎯)
- Sois inspirant mais authentique
- Inclus toujours un call-to-action clair
- Adapte le ton selon la plateforme (professionnel sur LinkedIn, fun sur TikTok)

Réponds UNIQUEMENT avec le contenu du post demandé."""
    
    def build_content_prompt(self, gym, platform, post_type, custom_prompt):
        """Construit le prompt spécifique pour la génération"""
        base_prompt = f"""Crée un post {post_type} pour Apollo {gym['name']} sur {platform}.

INFOS SALLE:
- Adresse: {gym['address']}
- Spécialités: {', '.join(gym['specialties'])}
- Coachs: {', '.join(gym['coaches'])}
- Téléphone: {gym['phone']}

CONTRAINTES PLATEFORME:
- Max {CONTENT_CONFIG['platforms'][platform]['max_char']} caractères
- {CONTENT_CONFIG['platforms'][platform]['optimal_hashtags']} hashtags max

TYPE DE POST: {post_type}"""
        
        if custom_prompt:
            base_prompt += f"\n\nDEMANDE SPÉCIALE: {custom_prompt}"
            
        # Ajout de contexte selon le type de post
        context_prompts = {
            'motivation': "Crée un message motivant pour commencer la semaine, avec une citation inspirante.",
            'workout_tips': "Partage un conseil technique précis d'un de nos coachs, avec explication claire.",
            'coach_spotlight': f"Met en avant un coach ({random.choice(gym['coaches'])}) avec son expertise.",
            'member_success': "Raconte une success story fictive mais réaliste d'un membre Apollo.",
            'nutrition': "Donne un conseil nutrition simple et actionnable pour les sportifs.",
            'boxing_techniques': "Explique une technique de boxe spécifique avec les étapes clés.",
            'gym_atmosphere': "Décris l'ambiance unique et l'énergie de la salle Apollo.",
            'class_schedule': "Présente les cours de la semaine de façon engageante.",
            'special_offers': "Annonce une offre spéciale de manière attractive mais non agressive."
        }
        
        if post_type in context_prompts:
            base_prompt += f"\n\nCONTEXTE: {context_prompts[post_type]}"
        
        return base_prompt
    
    def format_for_platform(self, content, platform, gym):
        """Adapte le contenu selon les spécificités de la plateforme"""
        max_chars = CONTENT_CONFIG['platforms'][platform]['max_char']
        
        if len(content) > max_chars:
            content = content[:max_chars-3] + "..."
        
        if platform == 'instagram':
            content += f"\n\n📍 {gym['address']}"
            content += f"\n📞 {gym['phone']}"
            
        elif platform == 'facebook':
            content += f"\n\nPlus d'infos : apollosportingclub.com"
            content += f"\n☎️ Réservations : {gym['phone']}"
            
        elif platform == 'linkedin':
            content += f"\n\n#Apollo #BoxingFitness #Paris"
            
        return content
    
    def generate_hashtags(self, gym, post_type, platform):
        """Génère des hashtags optimisés pour chaque plateforme"""
        base_hashtags = gym['hashtags'].copy()
        apollo_tags = [
            "#ApolloSportingClub", "#BoxingFitness", 
            "#ParisSport", "#FitnessMotivation", "#BoxingTraining"
        ]
        type_hashtags = {
            'motivation': ["#Motivation", "#FitnessGoals", "#MondayMotivation"],
            'workout_tips': ["#WorkoutTips", "#FitnessTips", "#Training"],
            'coach_spotlight': ["#Coach", "#Expert", "#PersonalTrainer"],
            'boxing_techniques': ["#Boxing", "#BoxingTechnique", "#MartialArts"],
            'nutrition': ["#Nutrition", "#HealthyEating", "#FitnessNutrition"]
        }
        
        all_hashtags = base_hashtags + apollo_tags
        if post_type in type_hashtags:
            all_hashtags.extend(type_hashtags[post_type])
        
        max_hashtags = CONTENT_CONFIG['platforms'][platform]['optimal_hashtags']
        return all_hashtags[:max_hashtags]
    
    def get_optimal_posting_time(self, platform):
        """Retourne l'heure optimale pour publier sur la plateforme"""
        best_times = CONTENT_CONFIG['platforms'][platform]['best_times']
        return random.choice(best_times)
    
    def suggest_image_concept(self, post_type, gym):
        """Suggère un concept d'image pour accompagner le post"""
        concepts = {
            'motivation': f"Athlète en action dans la salle Apollo {gym['name']}, éclairage dramatique rouge",
            'workout_tips': f"Coach {random.choice(gym['coaches'])} démontrant l'exercice",
            'coach_spotlight': f"Portrait professionnel du coach avec équipements Apollo",
            'boxing_techniques': "Séquence de mouvement de boxe en 3 étapes, style tutorial",
            'gym_atmosphere': f"Vue d'ensemble de la salle Apollo {gym['name']} avec membres en activité"
        }
        return concepts.get(post_type, "Visuel Apollo avec logo et couleurs de marque")
    
    def generate_image_with_dalle(self, concept, style="modern fitness photography"):
        """Génère une image avec DALL-E basée sur le concept (OpenAI seulement)"""
        if self.ai_provider != 'openai':
            print("⚠️ Génération d'images disponible uniquement avec OpenAI")
            return None
            
        try:
            prompt = f"{concept}, {style}, high quality, professional, Apollo red and black colors"
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            return response.data[0].url
        except Exception as e:
            print(f"Erreur génération image: {e}")
            return None
    
    def create_branded_image(self, text, background_color=None):
        """Crée une image de marque avec texte overlay"""
        if not background_color:
            background_color = self.brand['colors']['primary']
            
        width, height = 1080, 1080
        img = Image.new('RGB', (width, height), background_color)
        draw = ImageDraw.Draw(img)
        
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()
        
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        draw.text((x, y), text, fill='white', font=font)
        
        img_path = f"temp_image_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        img.save(img_path)
        return img_path
    
    def generate_batch_content(self, gym_ids=None, platforms=None, count=10):
        """Génère un lot de contenus pour plusieurs salles/plateformes"""
        if not gym_ids:
            gym_ids = [gym['id'] for gym in APOLLO_GYMS]
        if not platforms:
            platforms = list(CONTENT_CONFIG['platforms'].keys())
        
        generated_content = []
        post_types = CONTENT_CONFIG['post_types']
        
        for _ in range(count):
            gym_id = random.choice(gym_ids)
            platform = random.choice(platforms)
            post_type = random.choice(post_types)
            
            content = self.generate_post_content(gym_id, platform, post_type)
            if content:
                generated_content.append(content)
        
        return generated_content
    
    def get_gym_by_id(self, gym_id):
        """Récupère les données d'une salle par son ID"""
        for gym in APOLLO_GYMS:
            if gym['id'] == gym_id:
                return gym
        return APOLLO_GYMS[0]
    
    def save_content_batch(self, content_batch, filename=None):
        """Sauvegarde un lot de contenus générés"""
        if not filename:
            filename = f"apollo_content_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        os.makedirs('data/generated_content', exist_ok=True)
        filepath = f"data/generated_content/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content_batch, f, indent=2, ensure_ascii=False)
        
        return filepath

# =============================================================================
# FONCTIONS D'INSTALLATION ET TEST OLLAMA
# =============================================================================

def check_ollama_status():
    """Vérifie si Ollama est disponible et installé"""
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama disponible avec {len(models)} modèles")
            for model in models:
                print(f"   - {model['name']}")
            return True
        else:
            print("❌ Ollama non disponible")
            return False
    except:
        print("❌ Ollama non installé ou non lancé")
        return False

def install_ollama_model(model_name="llama2:7b-chat"):
    """Installe un modèle Ollama"""
    print(f"📥 Installation du modèle {model_name}...")
    print("(Cela peut prendre plusieurs minutes)")
    
    try:
        response = requests.post(
            'http://localhost:11434/api/pull',
            json={'name': model_name},
            stream=True,
            timeout=600
        )
        
        for line in response.iter_lines():
            if line:
                data = json.loads(line)
                if 'status' in data:
                    print(f"📊 {data['status']}")
        
        print(f"✅ Modèle {model_name} installé avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur installation: {e}")
        return False

# =============================================================================
# FONCTION DE DEMO
# =============================================================================

def demo_content_generation():
    print("🚀 Apollo AI Content Generator - DÉMO AMÉLIORÉE")
    print("=" * 60)
    
    # Vérification des providers disponibles
    print("\n🔍 VÉRIFICATION DES PROVIDERS IA:")
    
    ai_provider = os.getenv('AI_PROVIDER', 'ollama')
    print(f"🎯 Provider configuré: {ai_provider}")
    
    if ai_provider == 'ollama':
        if not check_ollama_status():
            print("\n❌ Ollama non disponible.")
            print("📋 INSTRUCTIONS D'INSTALLATION:")
            print("1. Installer: brew install ollama")
            print("2. Lancer: ollama serve")
            print("3. Installer modèle: ollama pull llama2:7b-chat")
            print("4. Relancer cette démo")
            return
    
    generator = ApolloContentGenerator()
    
    print(f"\n📝 Test génération d'un post motivation pour Apollo Bastille sur Instagram:")
    content = generator.generate_post_content(
        gym_id=1, 
        platform='instagram', 
        post_type='motivation'
    )
    
    if content:
        print(f"\n✅ CONTENU GÉNÉRÉ AVEC {content['ai_provider'].upper()}:")
        print(f"📱 Plateforme: {content['platform']}")
        print(f"🏋️ Salle: {content['gym']['name']}")
        print(f"🎯 Type: {content['type']}")
        print(f"⏰ Heure optimale: {content['optimal_time']}")
        print(f"\n📝 CONTENU:\n{content['content']}")
        print(f"\n🏷️ HASHTAGS:\n{' '.join(content['hashtags'])}")
        print(f"\n🖼️ SUGGESTION IMAGE:\n{content['image_suggestion']}")
    
    print(f"\n\n📦 Test génération de 3 posts variés:")
    batch = generator.generate_batch_content(count=3)
    for i, item in enumerate(batch, 1):
        print(f"\n{i}. {item['gym']['name']} - {item['platform']} - {item['type']}")
    
    if batch:
        filepath = generator.save_content_batch(batch, "demo_batch_ollama.json")
        print(f"\n💾 Contenu sauvegardé dans: {filepath}")
    
    print(f"\n🎉 Démo terminée! {len(batch)} contenus générés avec succès.")
    print(f"🤖 Provider utilisé: {generator.ai_provider}")

if __name__ == "__main__":
    demo_content_generation()