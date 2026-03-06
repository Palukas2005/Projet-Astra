# main.py
import json
from core.emotion_engine import EmotionEngine
from core.personality import Personality
from core.memory import Memory
from core.reasoning import Reasoning
from core.communication import Communication
from core.evolution import Evolution
from core.brain import Brain
from core.autonomy.initiative import Initiative
from utils.logger import Logger

# 🔹 Chargement config
with open("data/config.json", encoding="utf-8") as f:
    config = json.load(f)

# 🔹 Initialisation modules
emotions = EmotionEngine(config["emotions"])
personality = Personality(config["traits"])
memory = Memory()
reasoning = Reasoning(emotions, personality, memory)
communication = Communication(model_name="microsoft/phi-2")
evolution = Evolution(personality, emotions)
logger = Logger()
brain = Brain(personality, emotions, memory, reasoning, communication, evolution, logger)
autonomy = Initiative(brain)

print("Astra est prête. Tapez 'exit' pour quitter.")

# 🔹 Boucle d’interaction
while True:
    # 1️⃣ Vérifier initiative autonome
    autonomous_response = autonomy.try_action()
    if autonomous_response:
        print("Astra (spontanée) :", autonomous_response)

    # 2️⃣ Interaction classique
    user_message = input("Vous : ")
    if user_message.lower() in ["exit", "quit"]:
        break

    response = brain.process_message(user_message)
    print("Astra :", response)
    print("Traits actuels :", personality.traits)