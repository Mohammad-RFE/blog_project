from django.shortcuts import render, redirect, get_object_or_404
from .models import Account
from django.http import JsonResponse
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import ProfileUpdateForm, CustomLoginForm, CustomRegisterForm
from blog.models import Article
from django.core.paginator import Paginator


def register_page(request):
    if request.method == "POST":
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()

    return render(request, "authentication/register.html", {"form": form})

def login_page(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = CustomLoginForm()
    return render(request, 'authentication/login.html', {'form': form})



def logout_page(request):
    logout(request)
    return redirect("home")


User = get_user_model()
@login_required
def user_panel(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ProfileUpdateForm(instance=request.user)

    target_user = get_object_or_404(User, username=request.user.username)

    user_articles = Article.objects.filter(author=target_user).order_by('-created_at')

    paginator = Paginator(user_articles, 3)
    current_page = request.GET.get('page', 1)
    page_objects = paginator.get_page(current_page)

    return render(request, 'authentication/user_panel.html', {'form': form, 'articles': page_objects})



def user_public_profile(request, username):
    target_user = get_object_or_404(User, username=username)

    user_articles = Article.objects.filter(author=target_user).order_by('-created_at')

    paginator = Paginator(user_articles, 3)
    current_page = request.GET.get('page', 1)
    page_objects = paginator.get_page(current_page)

    context = {
        'author': target_user,
        'articles': page_objects,
    }

    return render(request, 'authentication/user_profile.html', context)


@login_required
def delete_profile_image_ajax(request):
    if request.method == "POST":
        user = request.user

        if user.profile:
            user.profile.delete(save=False)
            user.profile = None
            user.save()

            default_avatar_url = "/static/images/default-profile.jpg"
            return JsonResponse({"success": True, "default_url": default_avatar_url})

        return JsonResponse({"success": False, "error": "No profile image found."}, status=400)

    return JsonResponse({"success": False, "error": "Invalid request method."}, status=400)
