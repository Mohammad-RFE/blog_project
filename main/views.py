# Views for landing pages, static informational pages, and contact submissions
from django.shortcuts import render, redirect
from blog.models import Article, Category, Tag
from django.contrib import messages
from .forms import ContactForm

def home_page(request):
    """
    Renders the homepage displaying top recent articles for the banner and main feed.
    """
    context = {
        "banner_articles": Article.objects.order_by('-created_at')[:3],
        "main_articles": Article.objects.order_by('-created_at')[3:9],
    }
    return render(request, "main/index.html", context)


def about_page(request):
    """
    Renders the static About Us page.
    """
    return render(request, "main/about.html")

def contact_us(request):
    """
    Handles rendering and submission of the Contact Us feedback form.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact_us')

    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})