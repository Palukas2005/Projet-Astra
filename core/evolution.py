class Evolution:
    def __init__(self, personality, emotion_engine):
        self.personality = personality
        self.emotion_engine = emotion_engine

    def evolve(self):
        dominant = self.emotion_engine.dominant_emotion()[1]
        if dominant == "curiosite":
            self.personality.adjust_trait("curiosite", 1)
        elif dominant == "fierte":
            self.personality.adjust_trait("empathie", 1)