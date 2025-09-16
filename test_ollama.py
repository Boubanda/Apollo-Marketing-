import requests

def test_ollama():
    response = requests.post('http://localhost:11434/api/generate', 
        json={
            'model': 'mistral:7b',
            'prompt': 'Écris un post Instagram pour une salle de sport en 30 mots',
            'stream': False
        },
        timeout=30
    )
    print(response.json()['response'])

test_ollama()
