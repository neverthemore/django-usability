from functools import lru_cache

from core.ml import ModelServiceError


MODEL_NAME = "cointegrated/rubert-tiny2-cedr-emotion-detection"
LABELS_RU = [
    "Нет выраженной эмоции",
    "Радость",
    "Грусть",
    "Удивление",
    "Страх",
    "Злость",
]


class EmotionPredictor:
    def __init__(self, torch_module, tokenizer, model):
        self.torch = torch_module
        self.tokenizer = tokenizer
        self.model = model

    def predict(self, text):
        try:
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                truncation=True,
                max_length=512,
            )
            with self.torch.inference_mode():
                logits = self.model(**inputs).logits[0]
                values = self.torch.sigmoid(logits).cpu().tolist()
        except Exception as exc:
            raise ModelServiceError("Модель не смогла обработать этот текст.") from exc

        scores = [
            {"label": label, "score": round(float(score) * 100, 1)}
            for label, score in zip(LABELS_RU, values)
        ]
        return sorted(scores, key=lambda item: item["score"], reverse=True)


@lru_cache(maxsize=1)
def get_predictor():
    try:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        model.eval()
        return EmotionPredictor(torch, tokenizer, model)
    except Exception as exc:
        raise ModelServiceError(
            "Не удалось загрузить модель эмоций. Проверьте интернет и выполните "
            "python manage.py prepare_models --service text."
        ) from exc

