from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.ml import ModelServiceError
from core.session import get_session_key

from .forms import ImagePredictionForm
from .models import ImagePrediction
from .services import get_predictor


@require_http_methods(["GET", "POST"])
def index(request):
    session_key = get_session_key(request)
    current = None

    if request.method == "POST":
        form = ImagePredictionForm(request.POST, request.FILES)
        if form.is_valid():
            prediction = form.save(commit=False)
            prediction.session_key = session_key
            prediction.save()
            try:
                prediction.labels = get_predictor().predict(prediction.image.path)
            except ModelServiceError as exc:
                prediction.image.delete(save=False)
                prediction.delete()
                form.add_error(None, str(exc))
            else:
                prediction.save(update_fields=["labels"])
                return redirect(f"{request.path}?result={prediction.pk}#result")
    else:
        form = ImagePredictionForm()

    result_id = request.GET.get("result")
    if result_id and result_id.isdigit():
        current = get_object_or_404(ImagePrediction, pk=result_id, session_key=session_key)

    history = ImagePrediction.objects.filter(session_key=session_key)[:6]
    return render(
        request,
        "image_classifier/index.html",
        {"form": form, "current": current, "history": history, "active_page": "images"},
    )

