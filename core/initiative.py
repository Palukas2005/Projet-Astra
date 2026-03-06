# core/autonomy/initiative.py
import random

class Initiative:
    def __init__(self, brain):
        self.brain = brain

    def try_action(self):
        """
        L’IA décide de parler spontanément selon sa curiosité.
        """
        curiosite = self.brain.personality.traits.get("curiosite", 50)
        chance = random.randint(0, 100)

        if chance < curiosite:
            # Générer message autonome
            recent_memories = self.brain.memory.get_memories()
            memory_context = self.brain._shorten_memory(
                "\n".join([m[0] for m in recent_memories])
            )
            user_message = "Je veux dire quelque chose de spontané."

            response = self.brain.communication.generate_response(
                user_message,
                self.brain.personality.traits,
                self.brain.emotions.emotions,
                memory_context
            )

            # Style et log
            style_instruction = self.brain.choose_style(user_message)
            response = f"{style_instruction} {response}".strip()
            self.brain.memory.add_memory("autonome", response, self.brain.emotions.emotions)
            self.brain.logger.log_decision("Autonome", response, "autonomous_action")

            return response

        return None