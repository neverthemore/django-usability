from functools import lru_cache

from core.ml import ModelServiceError


class ImagePredictor:
    def __init__(self, torch_module, model, preprocess, categories):
        self.torch = torch_module
        self.model = model
        self.preprocess = preprocess
        self.categories = categories

    def predict(self, image_path):
        try:
            from PIL import Image

            with Image.open(image_path) as source:
                image = source.convert("RGB")
                batch = self.preprocess(image).unsqueeze(0)
            with self.torch.inference_mode():
                probabilities = self.model(batch).squeeze(0).softmax(0)
            values, indexes = self.torch.topk(probabilities, 3)
        except Exception as exc:
            raise ModelServiceError("Модель не смогла обработать это изображение.") from exc

        return [
            {"label": self.categories[int(index)], "score": round(float(value) * 100, 1)}
            for value, index in zip(values, indexes)
        ]


@lru_cache(maxsize=1)
def get_predictor():
    try:
        import torch
        from torchvision.models import MobileNet_V3_Small_Weights, mobilenet_v3_small

        weights = MobileNet_V3_Small_Weights.DEFAULT
        model = mobilenet_v3_small(weights=weights)
        model.eval()
        return ImagePredictor(torch, model, weights.transforms(), weights.meta["categories"])
    except Exception as exc:
        raise ModelServiceError(
            "Не удалось загрузить модель изображений. Проверьте интернет и выполните "
            "python manage.py prepare_models --service image."
        ) from exc

