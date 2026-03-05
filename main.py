import json
from core.emotion_engine import EmotionEngine
from core.personality import Personality
from core.memory import Memory
from core.reasoning import Reasoning
from core.communication import Communication
from core.evolution import Evolution
from utils.logger import Logger  # <-- Ajout du logger

# Chargement config
with open("data/config.json", encoding="utf-8") as f:
    config = json.load(f)

# Initialisation des modules
emotions = EmotionEngine(config["emotions"])
personality = Personality(config["traits"])
memory = Memory()
reasoning = Reasoning(emotions, personality, memory)
comm = Communication()
evolution = Evolution(personality, emotions)
logger = Logger()  # <-- Initialisation

print("Astra est prête. Tapez 'exit' pour quitter.")

# Boucle d'interaction
while True:
    user_message = input("Vous : ")
    if user_message.lower() in ["exit", "quit"]:
        break

    # --- Logger ---
    logger.log_user_message(user_message)

    # Mise à jour émotionnelle simple à chaque message
    emotions.update_emotion({"joie": {"amusement": 5}})

    # Récupération des souvenirs récents
    recent_memories = memory.get_memories()
    memory_context = "\n".join([m[0] for m in recent_memories])  # seulement contenu

    # Décision autonome de l'action (pour évolutions futures)
    action = reasoning.decide_action(user_message)

    # Génération de la réponse autonome (français / anglais)
    response = comm.generate_response(
        user_message,
        personality.traits,
        emotions.emotions,
        memory_context
    )

    # Sauvegarder le message comme souvenir
    memory.add_memory("conversation", user_message, emotions.emotions)

    # Logger la réponse d’Astra
    logger.log_ai_response(response)

    # Évolution autonome
    evolution.evolve()

    # Affichage
    print("Astra :", response)
    print("Traits actuels :", personality.traits)