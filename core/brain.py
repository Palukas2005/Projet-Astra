# core/brain.py
from langdetect import detect, DetectorFactory
DetectorFactory.seed = 0  # Cohérence pour la détection de langue

class Brain:
    def __init__(self, personality, emotions, memory, reasoning, communication, evolution, logger):
        self.personality = personality
        self.emotions = emotions
        self.memory = memory
        self.reasoning = reasoning
        self.communication = communication
        self.evolution = evolution
        self.logger = logger

    def process_message(self, user_message: str):
        """
        Traite un message utilisateur : décide, génère réponse, applique style et log.
        Optimisé pour Colab.
        """

        # 1️⃣ Mise à jour émotionnelle simple
        self.emotions.update_emotion({"joie": {"amusement": 5}})

        # 2️⃣ Récupération des souvenirs récents et limitation pour rapidité
        recent_memories = self.memory.get_memories()
        memory_context = self._shorten_memory("\n".join([m[0] for m in recent_memories]))

        # 3️⃣ Décision stratégique via reasoning
        action = self.reasoning.decide_action(user_message)

        # 4️⃣ Évolution autonome
        self.evolution.evolve()

        # 5️⃣ Déterminer style et ton
        style_instruction = self.choose_style(user_message)

        # 6️⃣ Génération réponse via communication
        response = self.communication.generate_response(
            user_message,
            self.personality.traits,
            self.emotions.emotions,
            memory_context,
        )

        # 7️⃣ Appliquer style
        response = f"{style_instruction} {response}".strip()

        # 8️⃣ Sauvegarder le message comme souvenir
        self.memory.add_memory("conversation", user_message, self.emotions.emotions)

        # 9️⃣ Logger l’action
        self.logger.log_decision(user_message, response, action)

        return response

    def choose_style(self, user_message: str):
        """
        Détermine le ton et le style de réponse selon personnalité, émotions
        et détecte automatiquement la langue (FR/EN).
        """
        style = ""

        # Style selon curiosité
        if self.personality.traits.get("curiosite", 0) > 70:
            style += "Je me demande… "

        # Style selon joie
        if self.emotions.emotions.get("joie", {}).get("plaisir", 0) > 60:
            style += "😄 "

        # Détection automatique de la langue
        try:
            lang = detect(user_message)
            if lang == "en":
                style += "(In English) "
        except:
            pass

        return style.strip()

    def _shorten_memory(self, memory_text: str):
        """
        Limite les souvenirs à 5 derniers et 200 caractères chacun pour accélérer le prompt.
        """
        lines = memory_text.split("\n")[-5:]  # 5 derniers souvenirs
        return "\n".join([line[:200] for line in lines])