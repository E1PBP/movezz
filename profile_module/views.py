from datetime import timedelta
from typing import List

from django.apps import apps
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.db.models import Prefetch
from .models import Profile, Follow, UserBadge, UserSport
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.http import JsonResponse, Http404

def format_short_number(number: int) -> str:
    integer_number = int(number or 0)
    absolute_value = abs(integer_number)
    if absolute_value >= 1_000_000_000:
        return f"{integer_number/1_000_000_000:.1f}".rstrip("0").rstrip(".") + "B"
    if absolute_value >= 1_000_000:
        return f"{integer_number/1_000_000:.1f}".rstrip("0").rstrip(".") + "M"
    if absolute_value >= 1_000:
        return f"{integer_number/1_000:.1f}".rstrip("0").rstrip(".") + "k"
    return str(integer_number)

def format_hours_minutes(duration: timedelta | None) -> str:
    if not duration:
        return "0m"
    total_seconds = int(duration.total_seconds())
    total_minutes = total_seconds // 60
    hours, minutes = divmod(total_minutes, 60)
    parts: List[str] = []
    if hours:
        parts.append(f"{hours}h")
    parts.append(f"{minutes}m")
    return " ".join(parts)

def _get_or_create_profile(u: User) -> Profile:
    profile, _ = Profile.objects.get_or_create(user=u)
    return profile

def _get_post_model():
    candidates = [("feeds_module", "Post"), ("posts", "Post"), ("feed", "Post")]
    for app_label, model_name in candidates:
        try:
            return apps.get_model(app_label, model_name)
        except LookupError:
            continue
    return None

def profile_detail(request, username: str):
    page_user = get_object_or_404(User, username=username)
    profile = _get_or_create_profile(page_user)

    badges = UserBadge.objects.select_related("badge").filter(user=page_user)

    current_sport_duration = timedelta(0)
    if profile.current_sport:
        user = UserSport.objects.filter(user=page_user, sport=profile.current_sport).first()
    
        if user and user.time_elapsed:
            current_sport_duration = user.time_elapsed

    is_following = False
    if request.user.is_authenticated and request.user != page_user:
        is_following = Follow.objects.filter(follower=request.user, followee=page_user).exists()

    active_tab = request.GET.get("tab", "posts")
    if active_tab not in ("posts", "broadcasts"):
        active_tab = "posts"

    context = {
        "page_user": page_user,
        "profile": profile,
        "badges": badges,
        "current_sport_duration": current_sport_duration, 
        "is_self": request.user.is_authenticated and request.user == page_user,
        "is_following": is_following,
        "post_count": profile.post_count,
        "broadcast_count": profile.broadcast_count,
        "followers_count": profile.followers_count,
        "following_count": profile.following_count,
        "format_short_number": format_short_number,
        "format_hours_minutes": format_hours_minutes,
    }

    posts = []
    Post = _get_post_model()
    if Post:
        qs = Post.objects.filter(user=page_user).order_by("-created_at")[:12]
        for p in qs:
            src = (
                getattr(getattr(p, "image", None), "url", None)
                or getattr(p, "image_url", None)
                or getattr(p, "photo_url", None)
            )
            if src:
                posts.append({"id": getattr(p, "pk", None), "image_url": src, "alt_text": getattr(p, "caption", "") or "post"})

    broadcasts = []
    try:
        Broadcast = apps.get_model("broadcast_module", "Broadcast")
        bqs = Broadcast.objects.filter(user=page_user).order_by("-created_at")[:10]
        for b in bqs:
            broadcasts.append({
                "title": getattr(b, "title", "Broadcast"),
                "subtitle": getattr(b, "location", "") or getattr(b, "subtitle", ""),
                "summary": getattr(b, "summary", "") or (getattr(b, "body", "")[:120] + "..."),
                "image_url": getattr(getattr(b, "cover", None), "url", None) or getattr(b, "image_url", None),
            })
    except LookupError:
        broadcasts = []

    context["active_tab"] = active_tab
    context["posts"] = posts
    context["broadcasts"] = broadcasts

    return render(request, "profile.html", context)

@require_POST
@login_required
def follow_toggle_ajax(request, username: str):
    target = get_object_or_404(User, username=username)
    if request.user == target:
        return JsonResponse({"detail": "Cannot follow yourself."}, status=400)

    object, created = Follow.objects.get_or_create(follower=request.user, followee=target)
    if not created:
        object.delete()
        following = False
    else:
        following = True

    try:
        target.profile.refresh_from_db()
        followers_count = target.profile.followers_count
    except Profile.DoesNotExist:
        followers_count = Follow.objects.filter(followee=target).count()

    return JsonResponse({"following": following, "followers_count": followers_count})

@require_POST
@login_required
def follow_user(request, username: str):
    target = get_object_or_404(User, username=username)
    if request.user != target:
        Follow.objects.get_or_create(follower=request.user, followee=target)
    return redirect("profile_detail", username=username)

@require_POST
@login_required
def unfollow_user(request, username: str):
    target = get_object_or_404(User, username=username)
    if request.user != target:
        Follow.objects.filter(follower=request.user, followee=target).delete()
    return redirect("profile_detail", username=username)

def post_detail(request, username: str, pk):
    Post = _get_post_model()
    if not Post:
        raise Http404("Post model not found.")
    post = get_object_or_404(Post, pk=pk, user__username=username)
    is_owner = request.user.is_authenticated and request.user == post.user

    more_posts = Post.objects.filter(user=post.user).exclude(pk=post.pk).order_by("-created_at")[:6]

    def image(p):
        return getattr(getattr(p, "image", None), "url", None) or getattr(p, "image_url", None) or getattr(p, "photo_url", None)

    context = {
        "post": post,
        "is_owner": is_owner,
        "more_posts": [{"id": p.pk, "image_url": image(p)} for p in more_posts if image(p)],
    }
    return render(request, "post_detail.html", context)

@require_POST
@login_required
def post_update_ajax(request, pk):
    Post = _get_post_model()
    if not Post:
        return JsonResponse({"detail": "Post model not found."}, status=404)
    postingan = get_object_or_404(Post, pk=pk)
    if request.user != postingan.user:
        return JsonResponse({"detail": "Forbidden"}, status=403)

    caption = request.POST.get("caption", "").strip()
    if hasattr(postingan, "caption"):
        postingan.caption = caption
        update_fields = ["caption"]
    else:
        update_fields = []
    if hasattr(postingan, "updated_at"):
        postingan.updated_at = timezone.now()
        update_fields.append("updated_at")
    postingan.save(update_fields=update_fields or None)
    return JsonResponse({"ok": True, "caption": caption})


@require_POST
@login_required
def post_delete_ajax(request, pk):
    Post = _get_post_model()
    if not Post:
        return JsonResponse({"detail": "Post model not found."}, status=404)
    postingan = get_object_or_404(Post, pk=pk)
    if request.user != postingan.user:
        return JsonResponse({"detail": "Forbidden"}, status=403)
    postingan.delete()
    return JsonResponse({"ok": True})





