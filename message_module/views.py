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
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


logger = logging.getLogger(__name__)
HISTORY_LIMIT_FETCH = 50


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
    logger.debug(f"Fetched {conversations.count()} conversations for user {user.username}.")
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
                logger.info(f"User {user.username} attempted to start a conversation with {target_user.username}, but it already exists.")
                return redirect("message_module:chat_view", existing_convo.id)

            new_convo = Conversation.objects.create(created_by=user)
            new_convo.members.create(user=user)
            new_convo.members.create(user=target_user)
            logger.info(f"User {user.username} started new conversation {new_convo.id} with {target_user.username}.")
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
            logger.debug(f"Loaded {messages.count()} messages for conversation {selected_conversation.id}.")
        except Exception:
            logger.error(f"Error loading conversation {conversation_id} for user {user.username}. Redirecting to chat home.")
            return redirect("message_module:chat_home")


    users = User.objects.exclude(id=user.id).select_related('profile')    
    logger.debug(f"Fetched {users.count()} users for chat view.")    
    context = {
        "conversations": conversations,
        "selected_conversation": selected_conversation,
        "messages": messages,
        "users": users,
        "last_message_id": last_message_id,  
    }
    logger.info(f"User {user.username} accessed chat view.")
    return render(request, "chat.html", context)


@csrf_exempt
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
    conversation = get_object_or_404(
        Conversation.objects.filter(members__user=request.user), 
        id=conversation_id
    )
    logger.debug(f"User {request.user.username} is sending a message to conversation {conversation.id}.")
    body = (request.POST.get("message") or "").strip()
    image_file = request.FILES.get("image")
    logger.debug(f"Message body length: {len(body)}. Image file present: {'yes' if image_file else 'no'}.")
    if not body and not image_file:
        logger.warning(f"User {request.user.username} attempted to send an empty message in conversation {conversation.id}.")
        return JsonResponse({"error": "Empty message"}, status=400)

    if image_file:
        logger.debug(f"Uploaded image content type: {image_file.content_type}.")
        allowed = {"image/jpeg", "image/png", "image/webp", "image/gif"}
        if image_file.content_type not in allowed:
            logger.warning(f"User {request.user.username} attempted to upload unsupported image type in conversation {conversation.id}.")
            return JsonResponse({"error": "Unsupported image type"}, status=400)


    msg = Message.objects.create(
        conversation=conversation,
        sender=request.user,
        body=body,
        image=image_file if image_file else None,
    )
    logger.debug(f"Created message {msg.id} in conversation {conversation.id} by user {request.user.username}.")
    conversation.update_last_message(msg)
    
    logger.info(f"User {request.user.username} sent message {msg.id} in conversation {conversation.id}.")
    return JsonResponse({
        "id": str(msg.id),
        "sender": msg.sender.username,
        "body": escape(msg.body),
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
    logger.debug(f"User {request.user.username} is polling messages for conversation {conversation.id}.")
    last_msg_id = (request.GET.get("last_msg_id") or "").strip()
    logger.debug(f"Last known message ID from client: {last_msg_id}.")
    if last_msg_id:
        ref = Message.objects.filter(id=last_msg_id, conversation=conversation).only("created_at").first()
        if ref:
            logger.debug(f"Found reference message {ref.id} for polling in conversation {conversation.id}.")
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
    
    logger.debug(f"Found {new_messages.count()} new messages for conversation {conversation.id}.")

    def initial_for(user):
        prof = getattr(user, 'profile', None)
        base = (getattr(prof, 'display_name', None) or user.username or '').strip()
        return (base[:1].upper() if base else 'U')

    data = []
    for msg in new_messages:
        try:
            prof = msg.sender.profile

        except Exception:
            prof = None
        avatar_url = getattr(getattr(prof, 'avatar_url', None), 'url', None) if prof else None
        local_created = timezone.localtime(msg.created_at)
        data.append({
            "id": str(msg.id),
            "sender": msg.sender.username,
            "sender_avatar": avatar_url,
            "sender_initial": initial_for(msg.sender),
            "body": escape(msg.body),
            "image_url": (msg.image.url if msg.image else None),
            "is_self": msg.sender == request.user,
            "created_at": local_created.strftime("%Y-%m-%d %H:%M"),
        })
    logger.debug(f"Prepared {len(data)} messages for JSON response in conversation {conversation.id}.")
    logger.info(f"User {request.user.username} polled messages in conversation {conversation.id}, found {len(data)} new messages.")
    return JsonResponse({"messages": data})



@login_required
def start_chat(request, username: str):
    """Create/find a private conversation with target user, then redirect."""
    target_user = get_object_or_404(User, username=username)
    logger.debug(f"User {request.user.username} is attempting to start chat with {target_user.username}.")
    if target_user == request.user:
        logger.warning(f"User {request.user.username} attempted to start a chat with themselves.")
        return redirect("message_module:chat_home")

    existing_convo = (
        Conversation.objects
        .filter(members__user=request.user)
        .filter(members__user=target_user)
        .distinct()
        .first()
    )
    logger.debug(f"Existing conversation check between {request.user.username} and {target_user.username} returned: {'found' if existing_convo else 'not found'}.")
    if existing_convo:
        logger.info(f"User {request.user.username} attempted to start a conversation with {target_user.username}, but it already exists.")
        return redirect("message_module:chat_view", existing_convo.id)

    convo = Conversation.objects.create(created_by=request.user)
    ConversationMember.objects.create(conversation=convo, user=request.user)
    ConversationMember.objects.create(conversation=convo, user=target_user)
    logger.info(f"User {request.user.username} started new conversation {convo.id} with {target_user.username}.")
    return redirect("message_module:chat_view", convo.id)


@csrf_exempt
@login_required
def get_conversations_api(request):
    """Fetch the list of conversations for the logged-in user.
    Args:
        request: this is the http request object.
    Returns:
        JsonResponse: A JSON response containing a list of conversations.
    """
    user = request.user
    conversations = (
        Conversation.objects
        .filter(members__user=user)
        .prefetch_related('members__user__profile')
        .order_by('-last_message_at', '-created_at')
    )
    logger.debug(f"Fetched {conversations.count()} conversations for user {user.username} via API.")
    data = []
    for c in conversations:

        other_user = next((m.user for m in c.members.all() if m.user.id != user.id), None)
        
        display_name = other_user.username
        avatar_url = None
        if hasattr(other_user, 'profile'):
            display_name = other_user.profile.display_name or other_user.username
            if other_user.profile.avatar_url:
                avatar_url = other_user.profile.avatar_url.url

        data.append({
            "id": str(c.id),
            "other_user_username": other_user.username,
            "other_user_display_name": display_name,
            "other_user_avatar": avatar_url,
            "last_message": c.last_message_preview or "No messages yet",
            "last_message_at": c.last_message_at.strftime("%Y-%m-%d %H:%M") if c.last_message_at else None,
        })

    logger.info(f"User {user.username} fetched conversation list, found {len(data)} conversations.")
    return JsonResponse({"conversations": data})



@login_required
def get_messages_api(request, conversation_id):
    """Fetch messages for a specific conversation.

    Args:
        request: http request object.
        conversation_id: ID of the conversation to fetch messages from.

    Returns:
        JsonResponse: A JSON response containing a list of messages.
    """
    conversation = get_object_or_404(Conversation, id=conversation_id)
    logger.debug(f"User {request.user.username} is fetching messages for conversation {conversation.id} via API.")
    if not conversation.members.filter(user=request.user).exists():
        logger.warning(f"Unauthorized access attempt by user {request.user.username} to conversation {conversation.id}.")
        return JsonResponse({"error": "Unauthorized"}, status=403)
    before_id = request.GET.get('before_id') 
    messages_query = Message.objects.filter(conversation=conversation).select_related('sender__profile')
    logger.debug(f"Initial message query for conversation {conversation.id} prepared.")
    if before_id:
        try:
            ref_msg = Message.objects.get(id=before_id)
            messages_query = messages_query.filter(created_at__lt=ref_msg.created_at)
        except Message.DoesNotExist:
            pass

    messages_queryset = messages_query.order_by('-created_at')[:HISTORY_LIMIT_FETCH]
    messages = list(reversed(messages_queryset))
    logger.debug(f"Fetched {len(list(messages))} messages for conversation {conversation.id}.")
    data = []
    for msg in messages:
        prof = getattr(msg.sender, 'profile', None)
        avatar_url = prof.avatar_url.url if (prof and prof.avatar_url) else None
        data.append({
            "id": str(msg.id),
            "sender": msg.sender.username,
            "body": msg.body,
            "image_url": msg.image.url if msg.image else None,
            "is_self": msg.sender == request.user,
            "created_at": timezone.localtime(msg.created_at).strftime("%Y-%m-%d %H:%M"),
            "sender_avatar": avatar_url
        })
    logger.debug(f"Prepared {len(data)} messages for JSON response in conversation {conversation.id}.")
    logger.info(f"User {request.user.username} fetched messages for conversation {conversation.id}, found {len(data)} messages.")
    logger.debug(f"Messages data: {data}")
    return JsonResponse({"messages": data})



@csrf_exempt
@login_required
def start_chat_api(request, username):
    """Create/find a private conversation with target user via API.

    Args:
        request: http request object.
        username: target user's username.

    Returns:
        JsonResponse: A JSON response indicating conversation status.
    """
    target_user = get_object_or_404(User, username=username)
    user = request.user
    logger.debug(f"User {user.username} is attempting to start chat with {target_user.username} via API.")
    if target_user == user:
        logger.warning(f"User {user.username} attempted to start a chat with themselves via API.")
        return JsonResponse({"error": "Cannot chat with self"}, status=400)
    
    existing_convo = (
        Conversation.objects
        .filter(members__user=user)
        .filter(members__user=target_user)
        .distinct()
        .first()
    )
    logger.debug(f"Existing conversation check between {user.username} and {target_user.username} via API returned: {'found' if existing_convo else 'not found'}.")
    if existing_convo:
        return JsonResponse({
            "status": "exists", 
            "conversation_id": str(existing_convo.id)
        })
    convo = Conversation.objects.create(created_by=user)
    ConversationMember.objects.create(conversation=convo, user=user)
    ConversationMember.objects.create(conversation=convo, user=target_user)
    logger.info(f"User {user.username} started new conversation {convo.id} with {target_user.username} via API.")
    return JsonResponse({
        "status": "created", 
        "conversation_id": str(convo.id)
    }, status=201)
    
    
    
@login_required
def search_users_api(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return JsonResponse({"users": []})
    users = User.objects.filter(
        Q(username__icontains=query) | 
        Q(profile__display_name__icontains=query)
    ).select_related('profile')
    logger.debug(f"User {request.user.username} is searching users with query '{query}' via API, found {users.count()} users.")
    data = []
    for u in users:
        avatar = None
        if hasattr(u, 'profile') and u.profile.avatar_url:
            avatar = u.profile.avatar_url.url
        display_name = u.username
        if hasattr(u, 'profile') and u.profile.display_name:
            display_name = u.profile.display_name
        data.append({
            "username": u.username,
            "display_name": display_name,
            "avatar_url": avatar,
            "is_verified": getattr(u.profile, 'is_verified', False) if hasattr(u, 'profile') else False
        })
    logger.info(f"User {request.user.username} searched users with query '{query}', found {len(data)} users.")
    return JsonResponse({"users": data})


