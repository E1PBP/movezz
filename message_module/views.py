import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Conversation, Message, ConversationMember
import logging
from django.contrib.auth.models import User
from profile_module.models import Profile
from django.db.models import Prefetch

logger = logging.getLogger(__name__)

@login_required
def chat_view(request, conversation_id=None):
    """Render the chat interface with conversations and messages.
    Args:
        request : http request object.
        conversation_id : (optional) ID of the selected conversation.
    Returns:
        HttpResponse: Rendered chat interface.
    """
    user = request.user
    conversations = (
    Conversation.objects
        .filter(members__user=user)
        .prefetch_related(
            Prefetch(
                'members',
                queryset=ConversationMember.objects.select_related('user__profile')
            )
    )
    .order_by('-last_message_at', '-created_at')
)

    for c in conversations:
        participants = [m.user for m in c.members.all()]
        c.other_user = next((u for u in participants if u.id != user.id), None)
    
    if request.method == "POST":
        username = request.POST.get("username")
        if username:
            target_user = get_object_or_404(User, username=username)
            existing_convo = (Conversation.objects
                  .filter(members__user=user)
                  .filter(members__user=target_user)
                  .distinct()
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
            messages = (
                Message.objects
                .filter(conversation=selected_conversation)
                .select_related('sender__profile')
                .order_by('created_at')
            )
            last = messages.last()
            last_message_id = str(last.id) if last else ""
        except Exception:
            return redirect("message_module:chat_home")

    users = User.objects.exclude(id=user.id).select_related('profile')    

    context = {
        "conversations": conversations,
        "selected_conversation": selected_conversation,
        "messages": messages,
        "users": users,
        "last_message_id": last_message_id,  
    }
    return render(request, "chat.html", context)



@login_required
@require_POST
def send_message(request, conversation_id):
    """Handle sending a new message in a conversation.
    Args:
        request : http request object.
        conversation_id : ID of the conversation to send message to.
    Returns:
        JsonResponse: A JSON response containing the new message details.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)

    body = (request.POST.get("message") or "").strip()
    image_file = request.FILES.get("image")

    if not body and not image_file:
        return JsonResponse({"error": "Empty message"}, status=400)

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
        "created_at": timezone.localtime(msg.created_at).strftime("%Y-%m-%d %H:%M"),
    })



@login_required
def poll_messages(request, conversation_id):
    """Fetch new messages for a conversation since the last known message ID.
    Args:
        request : http request object.
        conversation_id : ID of the conversation to poll messages from.
    Returns:
        JsonResponse: A JSON response containing a list of new messages.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    last_msg_id = (request.GET.get("last_msg_id") or "").strip()

    if last_msg_id:
        ref = Message.objects.filter(id=last_msg_id, conversation=conversation).only("created_at").first()
        if ref:
            new_messages = (Message.objects
                            .filter(conversation=conversation, created_at__gt=ref.created_at)
                            .select_related('sender__profile')  
                            .order_by("created_at"))
        else:
            new_messages = Message.objects.none()
    else:
        new_messages = (Message.objects
                        .filter(conversation=conversation)
                        .select_related('sender__profile')
                        .order_by("created_at"))

    def initial_for(user):
        prof = getattr(user, 'profile', None)
        base = (getattr(prof, 'display_name', None) or user.username or '').strip()
        return (base[:1].upper() if base else 'U')

    data = []
    for msg in new_messages:
        prof = getattr(msg.sender, 'profile', None)
        avatar_url = getattr(getattr(prof, 'avatar_url', None), 'url', None) if prof else None
        local_created = timezone.localtime(msg.created_at)
        data.append({
            "id": str(msg.id),
            "sender": msg.sender.username,
            "sender_avatar": avatar_url,
            "sender_initial": initial_for(msg.sender),
            "body": msg.body,
            "image_url": (msg.image.url if msg.image else None),
            "is_self": msg.sender == request.user,
            "created_at": local_created.strftime("%Y-%m-%d %H:%M"),
        })
    return JsonResponse({"messages": data})
