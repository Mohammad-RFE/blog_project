from django.shortcuts import render, redirect
from blog.models import Article, Category, Tag
from django.contrib import messages
from .forms import ContactForm

def home_page(request):

    context = {
        "banner_articles": Article.objects.order_by('-created_at')[:3],
        "main_articles": Article.objects.order_by('-created_at')[3:9],
    }
    return render(request, "main/index.html", context)


def about_page(request):
    return render(request, "main/about.html")

def contact_us(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')

    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})
