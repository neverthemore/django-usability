#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    if sys.version_info[:2] != (3, 11):
        current = ".".join(map(str, sys.version_info[:3]))
        raise SystemExit(
            f"Для проекта требуется Python 3.11, сейчас используется Python {current}.\n"
            "Создайте окружение версией 3.11 и запускайте команды через его python."
        )
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django не найден. Активируйте .venv и выполните "
            "python -m pip install -r requirements.txt"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
