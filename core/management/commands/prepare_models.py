from django.core.management.base import BaseCommand, CommandError


LOADERS = {
    "text": ("модель анализа эмоций", "text_classifier.services", "get_predictor"),
    "chat": ("диалоговая модель", "dialog_bot.services", "get_predictor"),
    "image": ("модель изображений", "image_classifier.services", "get_predictor"),
}


def root_cause(exception):
    current = exception
    visited = set()
    while id(current) not in visited:
        visited.add(id(current))
        next_exception = current.__cause__ or current.__context__
        if next_exception is None:
            break
        current = next_exception
    return f"{type(current).__name__}: {current}"


class Command(BaseCommand):
    help = "Загружает модели заранее и проверяет их инициализацию."

    def add_arguments(self, parser):
        parser.add_argument(
            "--service",
            choices=[*LOADERS, "all"],
            default="all",
            help="Какую модель подготовить (по умолчанию все).",
        )

    def handle(self, *args, **options):
        import gc
        import importlib

        selected = LOADERS if options["service"] == "all" else {options["service"]: LOADERS[options["service"]]}
        for key, (label, module_name, function_name) in selected.items():
            self.stdout.write(f"Подготовка: {label}…")
            try:
                module = importlib.import_module(module_name)
                loader = getattr(module, function_name)
                loader()
            except Exception as exc:
                raise CommandError(
                    f"Не удалось подготовить сервис {key}: {exc}\n"
                    f"Исходная причина: {root_cause(exc)}"
                ) from exc
            self.stdout.write(self.style.SUCCESS(f"Готово: {label}"))
            # Команде нужно проверить и скачать файлы, а не держать все модели
            # одновременно. Это заметно снижает расход памяти в режиме all.
            if hasattr(loader, "cache_clear"):
                loader.cache_clear()
            del loader
            gc.collect()
