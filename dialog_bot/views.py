from django.db import transaction
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST, require_http_methods

from core.ml import ModelServiceError
from core.session import get_session_key

from .forms import ChatForm
from .models import ChatMessage
from .services import get_predictor


@require_http_methods(["GET", "POST"])
def index(request):
    session_key = get_session_key(request)
    if request.method == "POST":
        form = ChatForm(request.POST)
        if form.is_valid():
            user_text = form.cleaned_data["message"]
            previous = list(
                ChatMessage.objects.filter(session_key=session_key)
                .order_by("-created_at")
                .values_list("text", flat=True)[:3]
            )
            context = [*reversed(previous), user_text]
            try:
                answer = get_predictor().predict(context)
            except ModelServiceError as exc:
                form.add_error(None, str(exc))
            else:
                with transaction.atomic():
                    ChatMessage.objects.create(
                        session_key=session_key, role=ChatMessage.Role.USER, text=user_text
                    )
                    ChatMessage.objects.create(
                        session_key=session_key, role=ChatMessage.Role.ASSISTANT, text=answer
                    )
                return redirect(f"{request.path}#conversation")
    else:
        form = ChatForm()

    latest_messages = list(
        ChatMessage.objects.filter(session_key=session_key).order_by("-created_at")[:20]
    )
    messages = list(reversed(latest_messages))
    return render(
        request,
        "dialog_bot/index.html",
        {
            "form": form,
            "chat_messages": messages,
            "has_messages": bool(messages),
            "active_page": "chat",
        },
    )


@require_POST
def clear(request):
    session_key = get_session_key(request)
    ChatMessage.objects.filter(session_key=session_key).delete()
    return redirect("dialog_bot:index")

