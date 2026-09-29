from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from core.ml import ModelServiceError
from core.session import get_session_key

from .forms import TextAnalysisForm
from .models import TextAnalysis
from .services import get_predictor


@require_http_methods(["GET", "POST"])
def index(request):
    session_key = get_session_key(request)
    current = None

    if request.method == "POST":
        form = TextAnalysisForm(request.POST)
        if form.is_valid():
            try:
                scores = get_predictor().predict(form.cleaned_data["text"])
            except ModelServiceError as exc:
                form.add_error(None, str(exc))
            else:
                analysis = form.save(commit=False)
                analysis.session_key = session_key
                analysis.scores = scores
                analysis.save()
                return redirect(f"{request.path}?result={analysis.pk}#result")
    else:
        form = TextAnalysisForm()

    result_id = request.GET.get("result")
    if result_id and result_id.isdigit():
        current = get_object_or_404(TextAnalysis, pk=result_id, session_key=session_key)

    history = TextAnalysis.objects.filter(session_key=session_key)[:6]
    return render(
        request,
        "text_classifier/index.html",
        {"form": form, "current": current, "history": history, "active_page": "emotions"},
    )

