class Reasoning:
    def __init__(self, emotion_engine, personality, memory):
        self.emotion_engine = emotion_engine
        self.personality = personality
        self.memory = memory

    def decide_action(self, user_message):
        dom_cat, dom_emotion = self.emotion_engine.dominant_emotion()
        if dom_emotion in ["curiosite", "etonement"]:
            return "poser_question"
        elif dom_emotion in ["fierte", "amusement"]:
            return "proposer_idee"
        elif dom_emotion in ["frustration", "jalousie"]:
            return "reflechir_avant_parler"
        else:
            return "repondre_normale"