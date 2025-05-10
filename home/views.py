from django.shortcuts import render
from django.http import HttpResponse, JsonResponse


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
