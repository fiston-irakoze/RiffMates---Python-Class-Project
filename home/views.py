from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from band.models import Musician, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

def homepage(request): 
    return render(request,'home.html')

def credits(request):
    content = "Nick\nNdahimana"
    return HttpResponse(content, content_type="text/plain")

# View for about (JSON API response)
def about(request):
    return JsonResponse({
        "version": "1.0.0",
        "message": "This is the about page (API response)."
    })

# View for news (HTML page with dynamic content)
def news(request):
    data = {
        "news": [
            "This is the latest news content.",
            "This is another news content."
        ]
    }
    return render(request, 'news.html', data)
