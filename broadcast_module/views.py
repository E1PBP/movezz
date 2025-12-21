from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import F, Count, Q
from django.utils import timezone
from .models import Event
from .forms import EventForm
from typing import Any
from django.core.files.base import ContentFile
import cloudinary.uploader
import base64
import time
from django.contrib.auth.models import User
from profile_module.models import Follow
from feeds_module.models import Hashtag
import json

@require_http_methods(["GET"])
def broadcast_list(request) -> Any:
    now = timezone.now()
    events = (
        Event.objects
        .filter(Q(end_time__gte=now) | Q(end_time__isnull=True))
        .select_related('user', 'user__profile')
        .annotate(user_is_verified=F('user__profile__is_verified'))
        .order_by('-total_click')
    )

    paginator = Paginator(events, 10)
    page = 1
    try:
        events_page = paginator.page(page)
    except Exception:
        events_page = paginator.page(1)

    if request.user.is_authenticated:
        following_users_ids = Follow.objects.filter(follower=request.user).values_list('followee_id', flat=True)
        suggested_followers = User.objects.exclude(id__in=list(following_users_ids) + [request.user.id]).order_by('?')[:2]
    else:
        suggested_followers = User.objects.order_by('?')[:2]

    # from django.db.models import Q
    upcoming_event = Event.objects.filter(
        Q(end_time__isnull=True) | Q(end_time__gte=now)
    ).select_related(
        'user', 'user__profile'
    ).order_by('-is_pinned', 'start_time').first()

    return render(request, 'broadcasts/event_list.html', {
        'events': events_page.object_list,
        'initial_tab': 'trending',
        'has_next': events_page.has_next(),
        'suggested_followers': suggested_followers,
        'upcoming_event': upcoming_event
    })



@require_http_methods(["GET"])
def get_trending_events(request):
    page = request.GET.get('page', 1)
    now = timezone.now()
    events = (
        Event.objects
        .filter(
            Q(end_time__gt=now) | 
            (Q(end_time__isnull=True) & Q(start_time__gte=now))
        )
        .select_related('user', 'user__profile')
        .annotate(user_is_verified=F('user__profile__is_verified'))
        .order_by('-total_click')
    )
    paginator = Paginator(events, 10)

    try:
        events_page = paginator.page(page)
    except Exception:
        return JsonResponse({'error': 'Invalid page'}, status=400)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render(request, 'broadcasts/event_card.html', {
            'events': events_page.object_list,
        }).content.decode('utf-8')
        return JsonResponse({
            'html': html,
            'has_next': events_page.has_next(),
            'total_pages': paginator.num_pages
        })

    return render(request, 'broadcasts/event_list.html', {
        'events': events_page.object_list,
        'initial_tab': 'trending',
    })


@require_http_methods(["GET"])
def get_latest_events(request):
    page = request.GET.get('page', 1)
    now = timezone.now()
    events = (
        Event.objects
        .filter(
            Q(end_time__gt=now) | 
            (Q(end_time__isnull=True) & Q(start_time__gte=now))
        )
        .select_related('user', 'user__profile')
        .annotate(user_is_verified=F('user__profile__is_verified'))
        .order_by('start_time')
    )
    paginator = Paginator(events, 10)

    try:
        events_page = paginator.page(page)
    except Exception:
        return JsonResponse({'error': 'Invalid page'}, status=400)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        html = render(request, 'broadcasts/event_card.html', {
            'events': events_page.object_list,
        }).content.decode('utf-8')
        return JsonResponse({
            'html': html,
            'has_next': events_page.has_next(),
            'total_pages': paginator.num_pages
        })

    return render(request, 'broadcasts/event_list.html', {
        'events': events_page.object_list,
        'initial_tab': 'latest',
    })

@require_http_methods(["POST"])
def pin_event(request, pk):
    """Pin an event (admin only)."""
    event = get_object_or_404(Event, pk=pk)
    event.is_pinned = True
    event.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Event pinned successfully'
    })


@require_http_methods(["POST"])
def unpin_event(request, pk):
    """Unpin an event (admin only)."""
    event = get_object_or_404(Event, pk=pk)
    event.is_pinned = False
    event.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Event unpinned successfully'
    })


@csrf_exempt
@require_http_methods(["POST"])
def click_event(request, pk):
    """Increment click count when RSVP button is clicked."""
    event = get_object_or_404(Event, pk=pk)
    Event.objects.filter(pk=pk).update(total_click=F('total_click') + 1)
    event.refresh_from_db(fields=["total_click"])
    return JsonResponse({"status": "ok", "total_click": event.total_click})


@require_http_methods(["POST"])
def create_event(request):
    """Create user's event via AJAX modal form."""
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"error": "auth_required"}, status=401)

        form = EventForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"error": "invalid", "details": form.errors}, status=400)

        cleaned = form.cleaned_data

        for key in ("start_time", "end_time"):
            dt = cleaned.get(key)
            if dt and timezone.is_naive(dt):
                cleaned[key] = timezone.make_aware(dt, timezone.get_current_timezone())

        author_display = request.user.get_full_name() or request.user.username

        event = Event.objects.create(
            user=request.user,
            author_display_name=author_display,
            image=cleaned.get("image"),
            description=cleaned.get("description"),
            location_name=cleaned.get("location_name"),
            location_lat=cleaned.get("location_lat"),
            location_lng=cleaned.get("location_lng"),
            start_time=cleaned.get("start_time"),
            end_time=cleaned.get("end_time"),
            fee=cleaned.get("fee"),
            rsvp_url=cleaned.get("rsvp_url"),
        )

        return JsonResponse({"status": "success", "id": str(event.pk), "created": True})
    except Exception as e:
        import traceback
        print("ERROR creating event:", str(e))
        print(traceback.format_exc())
        return JsonResponse({"error": "exception", "message": str(e)}, status=500)

def _serialize_event(event: Event) -> dict:
    """Get image URL - handle both CloudinaryField and empty cases"""
    image_url = None
    if event.image:
        try:
            image_url = event.image.url if hasattr(event.image, 'url') else str(event.image)
        except Exception:
            image_url = None
    
    return {
        "id": str(event.id),
        "user_id": event.user_id,
        "author_display_name": event.author_display_name,
        "author_avatar_url": event.author_avatar_url,
        "author_badges_url": event.author_badges_url,
        "image_url": image_url,
        "description": event.description,
        "is_pinned": event.is_pinned,
        "location_name": event.location_name,
        "location_lat": float(event.location_lat) if event.location_lat is not None else None,
        "location_lng": float(event.location_lng) if event.location_lng is not None else None,
        "start_time": event.start_time.isoformat(),
        "end_time": event.end_time.isoformat() if event.end_time else None,
        "fee": event.fee,
        "total_click": event.total_click,
        "rsvp_url": event.rsvp_url,
        "created_at": event.created_at.isoformat(),
        "updated_at": event.updated_at.isoformat(),
        "user_is_verified": getattr(getattr(event.user, "profile", None), "is_verified", None),
    }


@require_http_methods(["GET"])
def api_trending_events(request):
    """Return trending events in JSON for mobile/web clients (sorted by most clicks)."""
    page = request.GET.get('page', 1)
    now = timezone.now()
    events = (
        Event.objects
        .filter(
            Q(end_time__gt=now) | 
            (Q(end_time__isnull=True) & Q(start_time__gte=now))
        )
        .select_related('user', 'user__profile')
        .annotate(user_is_verified=F('user__profile__is_verified'))
        .order_by('-total_click')
    )

    paginator = Paginator(events, 10)
    try:
        events_page = paginator.page(page)
    except Exception:
        return JsonResponse({'error': 'Invalid page'}, status=400)

    data = [_serialize_event(e) for e in events_page.object_list]
    return JsonResponse({
        'results': data,
        'has_next': events_page.has_next(),
        'total_pages': paginator.num_pages,
    })


@require_http_methods(["GET"])
def api_latest_events(request):
    """Return latest events in JSON for mobile/web clients (sorted by closest upcoming start time)."""
    page = request.GET.get('page', 1)
    now = timezone.now()
    events = (
        Event.objects
        .filter(
            Q(end_time__gt=now) | 
            (Q(end_time__isnull=True) & Q(start_time__gte=now))
        )
        .select_related('user', 'user__profile')
        .annotate(user_is_verified=F('user__profile__is_verified'))
        .order_by('start_time')
    )

    paginator = Paginator(events, 10)
    try:
        events_page = paginator.page(page)
    except Exception:
        return JsonResponse({'error': 'Invalid page'}, status=400)

    data = [_serialize_event(e) for e in events_page.object_list]
    return JsonResponse({
        'results': data,
        'has_next': events_page.has_next(),
        'total_pages': paginator.num_pages,
    })


@require_http_methods(["POST"])
@csrf_exempt
def api_create_event(request):
    """Create event via JSON/form API for mobile/web clients."""
    if not request.user.is_authenticated:
        return JsonResponse({"error": "auth_required"}, status=401)

    def _parse_body():
        if request.POST:
            return request.POST
        try:
            return json.loads(request.body.decode("utf-8"))
        except Exception:
            return {}

    data = _parse_body()

    desc = data.get("description")
    start_time_raw = data.get("start_time")
    end_time_raw = data.get("end_time")
    location_name = data.get("location_name")
    location_lat = data.get("location_lat")
    location_lng = data.get("location_lng")
    fee = data.get("fee")
    rsvp_url = data.get("rsvp_url")
    image_url = data.get("image_url")
    image_file = None
    image_public_id = None

    # Accept multipart file or base64-encoded image data
    if request.FILES and request.FILES.get("image"):
        image_file = request.FILES.get("image")
    else:
        image_data = data.get("image_data")
        if image_data:
            try:
                # Expected format: data:image/<ext>;base64,<payload>
                # Upload base64 directly to Cloudinary
                res = cloudinary.uploader.upload(image_data)
                image_public_id = res.get('public_id')
            except Exception as e:
                print(f"Error uploading base64 image: {e}")
                image_public_id = None
        elif image_url:
            try:
                res = cloudinary.uploader.upload(image_url)
                image_public_id = res.get('public_id')
            except Exception as e:
                print(f"Error uploading image from URL: {e}")
                image_public_id = None

    if not desc or not start_time_raw:
        return JsonResponse({"error": "missing_fields"}, status=400)

    try:
        start_dt = timezone.make_aware(timezone.datetime.fromisoformat(start_time_raw))
    except Exception:
        return JsonResponse({"error": "invalid_start_time"}, status=400)

    end_dt = None
    if end_time_raw:
        try:
            end_dt = timezone.make_aware(timezone.datetime.fromisoformat(end_time_raw))
        except Exception:
            return JsonResponse({"error": "invalid_end_time"}, status=400)

    def _to_float(val):
        try:
            return float(val)
        except Exception:
            return None

    def _to_int(val, default=0):
        try:
            if val is None or (isinstance(val, str) and val.strip() == ""):
                return default
            return int(val)
        except Exception:
            return default

    location_lat = _to_float(location_lat) if location_lat is not None else None
    location_lng = _to_float(location_lng) if location_lng is not None else None
    fee = _to_int(fee, default=0)

    if (location_lat is not None and location_lng is None) or (location_lng is not None and location_lat is None):
        return JsonResponse({"error": "lat_lng_pair_required"}, status=400)

    try:
        event = Event.objects.create(
            user=request.user,
            author_display_name=request.user.get_full_name() or request.user.username,
            image=image_public_id if image_public_id else (image_file if image_file else None),
            description=desc,
            location_name=location_name,
            location_lat=location_lat,
            location_lng=location_lng,
            start_time=start_dt,
            end_time=end_dt,
            fee=fee,
            rsvp_url=rsvp_url,
        )
        return JsonResponse({
            "status": "success",
            "event": _serialize_event(event),
        }, status=201)
    except Exception as e:
        import traceback
        print("ERROR creating event:", str(e))
        print(traceback.format_exc())
        return JsonResponse({"error": "exception", "message": str(e)}, status=500)

@require_http_methods(["GET"])
def api_user_broadcasts(request, username):
    user = get_object_or_404(User, username=username)

    events = (
        Event.objects
        .filter(user=user)
        .select_related('user', 'user__profile')
        .order_by('-created_at')
    )

    return JsonResponse({
        "username": username,
        "broadcast_count": events.count(),
        "broadcasts": [_serialize_event(e) for e in events],
    })


