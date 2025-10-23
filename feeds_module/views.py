from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm, PostImageForm
from .models import Post, PostHashtag, Hashtag
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.
@login_required
def main_view(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm()
    image_form = PostImageForm()
    context = {'form': form, 'image_form': image_form, 'posts': posts}
    return render(request, 'main.html', context)

@login_required
@require_POST
def create_post_ajax(request):
    form = PostForm(request.POST)
    image_form = PostImageForm(request.POST, request.FILES)

    if not form.is_valid():
        return JsonResponse({'status': 'error', 'errors': form.errors})

    post = form.save(commit=False)
    post.user = request.user

    user_badges = post.user.userbadge_set.select_related('badge').all()
    badge_urls = [user_badge.badge.icon_url for user_badge in user_badges if user_badge.badge.icon_url]
    post.author_badges_url = ",".join(badge_urls)

    # Process hashtags first
    hashtag_str = request.POST.get('hashtags')
    hashtags_to_add = []
    if hashtag_str:
        hashtag_names = [name.strip() for name in hashtag_str.split(',') if name.strip()]
        for name in hashtag_names:
            hashtag, _ = Hashtag.objects.get_or_create(tag=name)
            hashtags_to_add.append(hashtag)

    # Now save the post
    post.save()

    # Then, create the relationships
    if hashtags_to_add:
        post.posthashtag_set.bulk_create([
            PostHashtag(post=post, hashtag=hashtag) for hashtag in hashtags_to_add
        ])

    time_str = request.POST.get('hour')
    if time_str:
        post.created_at = post.created_at.replace(hour=int(time_str), minute=0, second=0, microsecond=0)
        post.save()


    if image_form.is_valid() and request.FILES.get('image'):
        post_image = image_form.save(commit=False)
        post_image.post = post
        post_image.save()

    return JsonResponse({'status': 'success', 'message': 'Post created successfully!'})