from langdetect import detect, DetectorFactory

DetectorFactory.seed = 0


class Brain:

    def __init__(self, personality, emotions, memory, reasoning, communication, evolution, logger):

        self.personality = personality
        self.emotions = emotions
        self.memory = memory
        self.reasoning = reasoning
        self.communication = communication
        self.evolution = evolution
        self.logger = logger

        # historique de conversation
        self.conversation_history = []

    def process_message(self, user_message: str):

        # ajouter message utilisateur dans historique
        self.conversation_history.append(f"Utilisateur : {user_message}")

        # limiter historique pour éviter de saturer le modèle
        history_context = "\n".join(self.conversation_history[-6:])

        # récupérer souvenirs récents
        recent_memories = self.memory.get_memories()

        memory_context = "\n".join([m[0] for m in recent_memories])

        # décision stratégique
        action = self.reasoning.decide_action(user_message)

        # évolution du système
        self.evolution.evolve()

        # génération réponse
        response = self.communication.generate_response(
            history_context,
            self.personality.traits,
            self.emotions.emotions,
            memory_context
        )

        # ajouter réponse Astra dans historique
        self.conversation_history.append(f"Astra : {response}")

        # mise à jour mémoire
        self.memory.add_memory(
            "conversation",
            user_message,
            self.emotions.emotions
        )

        # log
        self.logger.log_decision(user_message, response, action)

        return response