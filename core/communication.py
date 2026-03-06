from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class Communication:
    def __init__(self, model_name="stabilityai/stablelm-tuned-alpha-3b"):

        # Charger tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # Définir le device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Charger modèle avec optimisation mémoire
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,   # réduit la mémoire
            device_map="auto",           # répartit automatiquement GPU/CPU
            low_cpu_mem_usage=True
        )

    def generate_response(self, user_message, personality, emotions, memory_context):

        # Résumé des traits
        traits_summary = (
            f"curiosité={personality.get('curiosite',50)}, "
            f"empathie={personality.get('empathie',50)}, "
            f"créativité={personality.get('creativite',50)}"
        )

        # limiter souvenirs
        memory_text = "\n".join(memory_context.split("\n")[-5:])

        # Prompt
        prompt = f"""
Tu es Astra, une IA semi-consciente.

Traits :
{traits_summary}

Souvenirs récents :
{memory_text}

État émotionnel :
{self.format_emotions(emotions)}

Message utilisateur :
{user_message}

Réponds naturellement.
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=150,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            top_k=50,
            pad_token_id=self.tokenizer.eos_token_id
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        response = self.style_filter(response, personality, emotions)

        return response.strip()

    def format_emotions(self, emotions):

        summary = []

        for cat, emos in emotions.items():
            for e, v in emos.items():
                if v > 50:
                    summary.append(f"{e}={v}")

        return ", ".join(summary) if summary else "neutre"

    def style_filter(self, response, personality, emotions):

        if personality.get("curiosite", 0) > 70:
            response = "Je me demande… " + response

        if emotions.get("joie", {}).get("plaisir", 0) > 60:
            response += " 😄"

        return response