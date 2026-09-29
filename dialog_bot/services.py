from functools import lru_cache

from core.ml import ModelServiceError


MODEL_NAME = "cointegrated/rut5-small-chitchat"


class ChatPredictor:
    def __init__(self, torch_module, tokenizer, model):
        self.torch = torch_module
        self.tokenizer = tokenizer
        self.model = model

    def predict(self, messages):
        prompt = "\n\n".join(messages[-4:])
        try:
            inputs = self.tokenizer(prompt, return_tensors="pt", truncation=True, max_length=512)
            with self.torch.inference_mode():
                output = self.model.generate(
                    **inputs,
                    do_sample=True,
                    top_p=0.85,
                    temperature=0.8,
                    repetition_penalty=2.0,
                    max_new_tokens=48,
                )[0]
            answer = self.tokenizer.decode(output, skip_special_tokens=True).strip()
        except Exception as exc:
            raise ModelServiceError("Диалоговая модель не смогла сформировать ответ.") from exc
        return answer or "Мне пока нечего ответить. Попробуйте сформулировать вопрос иначе."


@lru_cache(maxsize=1)
def get_predictor():
    try:
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=False)
        model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        model.eval()
        return ChatPredictor(torch, tokenizer, model)
    except Exception as exc:
        raise ModelServiceError(
            "Не удалось загрузить диалоговую модель. Проверьте интернет и выполните "
            "python manage.py prepare_models --service chat."
        ) from exc

