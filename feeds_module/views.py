from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PostForm, PostImageForm
from .models import Post, PostHashtag, Hashtag, PostLike
from profile_module.models import Follow
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, Exists, OuterRef, F
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.template.loader import render_to_string

@login_required
def main_view(request):
    active_tab = request.GET.get('tab', 'foryou') 

    # Annotate posts with whether the current user has liked them
    user_likes = PostLike.objects.filter(post=OuterRef('pk'), user=request.user)
    
    if active_tab == 'following':
        following_users = Follow.objects.filter(follower=request.user).values_list('followee', flat=True)
        post_list = Post.objects.filter(user__in=following_users).annotate(has_liked=Exists(user_likes)).order_by('-created_at')
    else:
        post_list = Post.objects.all().annotate(has_liked=Exists(user_likes)).order_by('-created_at')

    paginator = Paginator(post_list, 5)  # Show 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    form = PostForm()
    image_form = PostImageForm()

    # Popular tags
    popular_tags = Hashtag.objects.annotate(post_count=Count('posthashtag')).order_by('-post_count')[:3]

    # Suggested followers
    following_users_ids = Follow.objects.filter(follower=request.user).values_list('followee_id', flat=True)
    suggested_followers = User.objects.exclude(id__in=list(following_users_ids) + [request.user.id]).order_by('?')[:2]


    context = {
        'form': form,
        'image_form': image_form,
        'posts': posts,
        'active_tab': active_tab,
        'popular_tags': popular_tags,
        'suggested_followers': suggested_followers,
    }
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

    time_h = request.POST.get('time_h')
    time_m = request.POST.get('time_m')
    if time_h and time_m:
        post.created_at = post.created_at.replace(hour=int(time_h), minute=int(time_m), second=0, microsecond=0)
        post.save()

    if image_form.is_valid() and request.FILES.get('image'):
        post_image = image_form.save(commit=False)
        post_image.post = post
        post_image.save()

    return JsonResponse({'status': 'success', 'message': 'Post created successfully!'})

@login_required
@require_POST
def like_post_ajax(request):
    post_id = request.POST.get('post_id')
    post = get_object_or_404(Post, id=post_id)
    
    like, created = PostLike.objects.get_or_create(post=post, user=request.user)

    if not created:
        like.delete()
        post.likes_count = F('likes_count') - 1
        liked = False
    else:
        post.likes_count = F('likes_count') + 1
        liked = True
    
    post.save(update_fields=['likes_count'])
    post.refresh_from_db()

    return JsonResponse({'status': 'success', 'likes_count': post.likes_count, 'liked': liked})

@login_required
def load_more_posts(request):
    active_tab = request.GET.get('tab', 'foryou')
    user_likes = PostLike.objects.filter(post=OuterRef('pk'), user=request.user)
    if active_tab == 'following':
        following_users = Follow.objects.filter(follower=request.user).values_list('followee', flat=True)
        post_list = Post.objects.filter(user__in=following_users).annotate(has_liked=Exists(user_likes)).order_by('-created_at')
    else:
        post_list = Post.objects.all().annotate(has_liked=Exists(user_likes)).order_by('-created_at')

    paginator = Paginator(post_list, 5)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    html = render_to_string('components/post_list.html', {'posts': posts})
    return JsonResponse({'html': html, 'has_next': posts.has_next()})