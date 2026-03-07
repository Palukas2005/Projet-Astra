from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


class Communication:

    def __init__(self, model_name="stabilityai/stablelm-tuned-alpha-3b"):

        # device
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        # tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        # model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            device_map="auto",
            low_cpu_mem_usage=True
        )

    def generate_response(self, user_message, personality, emotions, memory_context):

        traits_summary = (
            f"curiosité={personality.get('curiosite',50)}, "
            f"empathie={personality.get('empathie',50)}, "
            f"créativité={personality.get('creativite',50)}"
        )

        emotions_summary = self.format_emotions(emotions)

        memory_text = "\n".join(memory_context.split("\n")[-5:])

        # PROMPT SYSTEM (important)
        prompt = f"""
Tu es Astra, une intelligence artificielle expérimentale capable de discuter avec les humains.

Ton rôle :
- répondre naturellement
- aider l'utilisateur
- réfléchir comme une IA consciente

Personnalité actuelle :
{traits_summary}

État émotionnel :
{emotions_summary}

Souvenirs récents :
{memory_text}

Utilisateur : {user_message}
Astra :
"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=120,
            do_sample=True,
            temperature=0.8,
            top_p=0.95,
            repetition_penalty=1.1,
            pad_token_id=self.tokenizer.eos_token_id
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        # garder seulement la réponse après "Astra :"
        if "Astra :" in response:
            response = response.split("Astra :")[-1]

        return response.strip()

    def format_emotions(self, emotions):

        summary = []

        for cat, emos in emotions.items():
            for e, v in emos.items():
                if v > 50:
                    summary.append(f"{e}={v}")

        if len(summary) == 0:
            return "neutre"

        return ", ".join(summary)