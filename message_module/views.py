import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Conversation, Message, ConversationMember
import logging
from django.contrib.auth.models import User

logger = logging.getLogger(__name__)


# =========================
# 📩 VIEW CHAT PAGE
# =========================

@login_required
def chat_view(request, conversation_id=None):
    user = request.user
    conversations = Conversation.objects.filter(
        members__user=user
    ).order_by('-last_message_at', '-created_at')

    for convo in conversations:
        convo.other_user = convo.get_participants().exclude(id=user.id).first()

    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            target_user = get_object_or_404(User, username=username)
            existing_convo = (
                Conversation.objects.filter(members__user=user)
                .filter(members__user=target_user)
                .first()
            )
            if existing_convo:
                return redirect("message_module:chat_view", existing_convo.id)

            new_convo = Conversation.objects.create(created_by=user)
            new_convo.members.create(user=user)
            new_convo.members.create(user=target_user)
            return redirect("message_module:chat_view", new_convo.id)

    selected_conversation = None
    messages = []
    last_message_id = ""

    if conversation_id:
        try:
            selected_conversation = get_object_or_404(Conversation, id=conversation_id)
            selected_conversation.other_user = selected_conversation.get_participants().exclude(id=user.id).first()
            messages = Message.objects.filter(conversation=selected_conversation).order_by("created_at")
            last = messages.last()
            last_message_id = str(last.id) if last else ""
        except Exception:
            return redirect("message_module:chat_home")

    users = User.objects.exclude(id=user.id)

    context = {
        "conversations": conversations,
        "selected_conversation": selected_conversation,
        "messages": messages,
        "users": users,
        "last_message_id": last_message_id,   # <-- penting untuk anti dobel
    }
    return render(request, "chat.html", context)



# =========================
# 📨 KIRIM PESAN (AJAX)
# =========================

@login_required
@require_POST
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    body = (request.POST.get("message") or "").strip()
    image_file = request.FILES.get("image")

    if not body and not image_file:
        return JsonResponse({"error": "Empty message"}, status=400)

    # (opsional) Validasi tipe gambar
    if image_file:
        allowed = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if image_file.content_type not in allowed:
            return JsonResponse({"error": "Unsupported image type"}, status=400)

    msg = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        body=body,
        image=image_file if image_file else None,
    )
    conversation.update_last_message(msg)

    return JsonResponse({
        "id": str(msg.id),
        "sender": msg.sender.username,
        "body": msg.body,
        "image_url": (msg.image.url if msg.image else None),
        "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M"),
    })



# =========================
# 🔁 LONG POLLING
# =========================
@login_required
def poll_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    last_msg_id = (request.GET.get("last_msg_id") or "").strip()

    if last_msg_id:
        ref = Message.objects.filter(id=last_msg_id, conversation=conversation).only("created_at").first()
        if ref:
            new_messages = Message.objects.filter(
                conversation=conversation,
                created_at__gt=ref.created_at
            ).order_by("created_at")
        else:
            new_messages = Message.objects.none()
    else:
        new_messages = Message.objects.filter(conversation=conversation).order_by("created_at")

    data = [
        {
            "id": str(msg.id),
            "sender": msg.sender.username,
            "sender_avatar": (
                msg.sender.profile.avatar.url
                if hasattr(msg.sender, "profile") and getattr(msg.sender.profile, "avatar", None)
                else "/static/img/default-avatar.png"
            ),
            "body": msg.body,
            "image_url": (msg.image.url if msg.image else None),
            "is_self": msg.sender == request.user,
            "created_at": msg.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for msg in new_messages
    ]
    return JsonResponse({"messages": data})