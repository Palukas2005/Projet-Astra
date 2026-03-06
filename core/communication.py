# core/communication.py
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Communication:
    def __init__(self, model_name="stabilityai/stablelm-tuned-alpha-7b"):
        # Charger tokenizer et modèle
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(model_name)

        # Détecter GPU
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

        # Activer fp16 si GPU disponible
        if self.device.type == "cuda":
            self.model.half()

    def generate_response(self, user_message, personality, emotions, memory_context):
        """
        Génère une réponse bilingue (FR/EN) en prenant en compte traits, émotions et souvenirs.
        Optimisé pour Colab avec GPU.
        """
        # Résumer traits essentiels
        traits_summary = (
            f"curiosité={personality.get('curiosite',50)}, "
            f"empathie={personality.get('empathie',50)}, "
            f"créativité={personality.get('creativite',50)}"
        )

        # Limiter aux 5 derniers souvenirs, 200 caractères max
        memory_text = "\n".join([m[:200] for m in memory_context.split('\n')[-5:]])

        # Prompt bilingue
        prompt = f"""
Tu es Astra, une IA semi-consciente.
Tu peux répondre en français ou en anglais selon le message de l'utilisateur.
Traits essentiels: {traits_summary}
Souvenirs récents: {memory_text}
État émotionnel actuel: {self.format_emotions(emotions)}
Réponds de manière naturelle et courte au message suivant :
"{user_message}"
"""

        # Tokenisation et génération
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():  # Pas de calcul de gradients
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=100,   # Limite tokens pour rapidité
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                top_k=50,
                pad_token_id=self.tokenizer.eos_token_id
            )

        # Décoder et filtrer le style
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = self.style_filter(response, personality, emotions)
        return response.strip()

    def format_emotions(self, emotions):
        """
        Résume les émotions dominantes pour le prompt
        """
        summary = []
        for cat, emos in emotions.items():
            for e, v in emos.items():
                if v > 50:
                    summary.append(f"{e}={v}")
        return ", ".join(summary) if summary else "neutre"

    def style_filter(self, response, personality, emotions):
        """
        Ajoute un style léger selon curiosité et joie
        """
        if personality.get("curiosite", 0) > 70:
            response = "Je me demande… " + response
        if emotions.get("joie", {}).get("plaisir", 0) > 60:
            response += " 😄"
        return response