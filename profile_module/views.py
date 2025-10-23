from datetime import timedelta
from typing import List, Dict, Any

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.db.models import Prefetch

from .models import Profile, Follow, UserBadge, UserSport
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

MOCK_POSTS = [
    {"id": "p-01", "image_url": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?auto=format&fit=crop&w=900&q=80", "alt_text": "Badminton court"},
    {"id": "p-02", "image_url": "https://images.unsplash.com/photo-1502877338535-766e1452684a?auto=format&fit=crop&w=900&q=80", "alt_text": "Football stadium sprinklers"},
    {"id": "p-03", "image_url": "https://images.unsplash.com/photo-1517649763962-0c623066013b?auto=format&fit=crop&w=900&q=80", "alt_text": "Tennis player shadow"},
    {"id": "p-04", "image_url": "https://images.unsplash.com/photo-1500048993953-d23a436266cf?auto=format&fit=crop&w=900&q=80", "alt_text": "Snowboard jump"},
    {"id": "p-05", "image_url": "https://images.unsplash.com/photo-1546519638-68e109498ffc?auto=format&fit=crop&w=900&q=80", "alt_text": "Tennis balls in the air"},
    {"id": "p-06", "image_url": "https://images.unsplash.com/photo-1557180295-76eee20ae8aa?auto=format&fit=crop&w=900&q=80", "alt_text": "Court texture"},
    {"id": "p-07", "image_url": "https://images.unsplash.com/photo-1508804185872-d7badad00f7d?auto=format&fit=crop&w=900&q=80", "alt_text": "Football training cones"},
    {"id": "p-08", "image_url": "https://images.unsplash.com/photo-1491438590914-bc09fcaaf77a?auto=format&fit=crop&w=900&q=80", "alt_text": "Basketball hoop"},
    {"id": "p-09", "image_url": "https://images.unsplash.com/photo-1508609349937-5ec4ae374ebf?auto=format&fit=crop&w=900&q=80", "alt_text": "Skatepark lines"},
    {"id": "p-10", "image_url": "https://images.unsplash.com/photo-1521417531083-11b3b1e3ff66?auto=format&fit=crop&w=900&q=80", "alt_text": "Runner on track"},
    {"id": "p-11", "image_url": "https://images.unsplash.com/photo-1500048993953-d23a436266cf?auto=format&fit=crop&w=900&q=80", "alt_text": "Snowboarder"},
    {"id": "p-12", "image_url": "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=900&q=80", "alt_text": "Tennis ball on court"},
]

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

def profile_detail(request, username: str):
    page_user = get_object_or_404(User, username=username)
    profile = _get_or_create_profile(page_user)

    badges = (
        UserBadge.objects
        .select_related("badge")
        .filter(user=page_user)
    )

    current_sport_duration = timedelta(0)
    if profile.current_sport:
        user = (
            UserSport.objects
            .filter(user=page_user, sport=profile.current_sport)
            .first()
        )
        if user and user.time_elapsed:
            current_sport_duration = user.time_elapsed

    is_following = False
    if request.user.is_authenticated and request.user != page_user:
        is_following = Follow.objects.filter(
            follower=request.user, followee=page_user
        ).exists()

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
    }

    posts = []

    try:
        from feeds_module.models import Post as FeedPost  
        qs = FeedPost.objects.filter(user=page_user).order_by("-created_at")[:12]
        for p in qs:
            src = (
                getattr(getattr(p, "image", None), "url", None)
                or getattr(p, "image_url", None)
                or getattr(p, "photo_url", None)
            )
            if src:
                posts.append({
                    "image_url": src,
                    "alt_text": getattr(p, "caption", "") or "post",
                })
    except Exception:
        posts = []
    if not posts:
        posts = MOCK_POSTS[:12]
    context["posts"] = posts

    return render(request, "profile.html", context)


@require_POST
@login_required
def follow_user(request, username: str):
    target = get_object_or_404(User, username=username)
    if request.user != target:
        Follow.objects.get_or_create(follower=request.user, followee=target)
    return redirect("profile_module:profile-detail", username=username)

@require_POST
@login_required
def unfollow_user(request, username: str):
    target = get_object_or_404(User, username=username)
    if request.user != target:
        Follow.objects.filter(follower=request.user, followee=target).delete()
    return redirect("profile_module:profile-detail", username=username)





