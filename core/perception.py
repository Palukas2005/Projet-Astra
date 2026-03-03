class Perception:
    def __init__(self):
        # Mémoire sensorielle ou entrée brute
        self.inputs = []

    def perceive(self, user_message):
        """
        Ajouter un nouveau message ou stimulus perçu par Astra.
        """
        self.inputs.append(user_message)

    def get_latest_input(self):
        """
        Retourner la perception la plus récente.
        """
        return self.inputs[-1] if self.inputs else None

    def clear_inputs(self):
        """
        Réinitialiser les perceptions.
        """
        self.inputs = []