from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.db.models import F
from django.utils import timezone

from .models import Event
from .forms import EventForm


@require_http_methods(["GET"])
def broadcast_list(request):
    """Main broadcast list page with trending/latest tabs."""
    events = Event.objects.order_by('-total_click').select_related('user')
    paginator = Paginator(events, 10)
    
    try:
        events_page = paginator.page(1)
    except Exception:
        events_page = paginator.page(1)
    
    return render(request, 'broadcasts/event_list.html', {
        'events': events_page.object_list,
        'initial_tab': 'trending',
        'has_next': events_page.has_next(),
    })


@require_http_methods(["GET"])
def get_trending_events(request):
    """AJAX endpoint for trending events (sorted by clicks)."""
    page = request.GET.get('page', 1)
    events = Event.objects.select_related('user').order_by('-total_click')
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
    """AJAX endpoint for latest events (sorted by upcoming start time)."""
    page = request.GET.get('page', 1)
    events = Event.objects.select_related('user').order_by('start_time')
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

        # Ensure timezone-aware datetimes
        for key in ("start_time", "end_time"):
            dt = cleaned.get(key)
            if dt and timezone.is_naive(dt):
                cleaned[key] = timezone.make_aware(dt, timezone.get_current_timezone())

        author_display = request.user.get_full_name() or request.user.username

        # Create new event
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

