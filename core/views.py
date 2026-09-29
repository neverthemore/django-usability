from django.shortcuts import render


SERVICES = [
    {
        "title": 'Анализ эмоций',
        "description": 'Оцените, какие эмоции выражены в русском тексте.',
        "url_name": "text_classifier:index",
        "icon": 'Aa',
    },
    {
        "title": 'Диалоговый бот',
        "description": 'Проведите короткий диалог с компактной локальной моделью.',
        "url_name": "dialog_bot:index",
        "icon": '…',
    },
    {
        "title": 'Классификация изображений',
        "description": 'Загрузите изображение и получите три наиболее вероятных класса.',
        "url_name": "image_classifier:index",
        "icon": '▧',
    },
]


def home(request): 
 return render( 
 request, 
 "core/home.html", 
 {"services": SERVICES, "active_page": "home"},
 ) 
