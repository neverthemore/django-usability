import json

from django.core.exceptions import ValidationError
from django.db import models


class JSONListField(models.TextField):
    """Хранит Python-список как JSON-текст без зависимости от SQLite JSON1."""

    description = "Список в формате JSON"

    def from_db_value(self, value, expression, connection):
        return self.to_python(value)

    def to_python(self, value):
        if isinstance(value, list):
            return value
        if value in (None, ""):
            return []
        try:
            result = json.loads(value)
        except (TypeError, json.JSONDecodeError) as exc:
            raise ValidationError("В базе сохранён некорректный JSON.") from exc
        if not isinstance(result, list):
            raise ValidationError("Значение должно быть JSON-списком.")
        return result

    def get_prep_value(self, value):
        return json.dumps(self.to_python(value), ensure_ascii=False)
