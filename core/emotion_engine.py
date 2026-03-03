class EmotionEngine:
    def __init__(self, emotions):
        self.emotions = emotions

    def update_emotion(self, event):
        """Met à jour les émotions selon un événement"""
        for category, changes in event.items():
            if category in self.emotions:
                for emotion, value in changes.items():
                    if emotion in self.emotions[category]:
                        self.emotions[category][emotion] += value
                        self.emotions[category][emotion] = max(0, min(100, self.emotions[category][emotion]))

    def dominant_emotion(self):
        """Retourne l’émotion dominante pour décider des actions"""
        max_val = 0
        dom = None
        for cat, emos in self.emotions.items():
            for e, v in emos.items():
                if v > max_val:
                    max_val = v
                    dom = (cat, e)
        return dom