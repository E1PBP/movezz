from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm

# Create your views here.
@login_required
def main_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('feeds_module:main_view')
    else:
        form = PostForm()

    context = {'form': form}
    return render(request, 'main.html', context)