from django.shortcuts import render,get_object_or_404
from .models import Musician 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.http import Http404

def viewAllBands(request):
    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, 5) 

    page_number = request.GET.get('page')
    try:
        musicians = paginator.page(page_number)
    except PageNotAnInteger:
        musicians = paginator.page(1)
    except EmptyPage:
        musicians = paginator.page(paginator.num_pages)

    context = {'musicians': musicians}
    return render(request, 'all_bands.html', context)

def viewMusicianDetails(request, id):

    musician = get_object_or_404(Musician, id=id)
    context = {
        'musician': musician
    }
    return render(request, 'musician_detail.html', context)


# views.py
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Musician, Band, Venue

def musician_list(request):
    # Handle per_page parameter
    per_page = request.GET.get('per_page', 5)
    try:
        per_page = int(per_page)
        per_page = min(max(1, per_page), 5)  # Constrain between 1-50
    except ValueError:
        per_page = 10

    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, per_page)
    
    page_number = request.GET.get('page')
    try:
        musicians = paginator.page(page_number)
    except PageNotAnInteger:
        musicians = paginator.page(1)
    except EmptyPage:
        musicians = paginator.page(paginator.num_pages)

    context = {
        'musicians': musicians,
        'per_page': per_page,
    }
    return render(request, 'musician_list.html', context)


# views.py
def band_list(request):
    # Handle per_page parameter
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        per_page = min(max(1, per_page), 5)
    except ValueError:
        per_page = 10

    bands_list = Band.objects.all()
    paginator = Paginator(bands_list, per_page)
    
    page_number = request.GET.get('page')
    try:
        bands = paginator.page(page_number)
    except PageNotAnInteger:
        bands = paginator.page(1)
    except EmptyPage:
        bands = paginator.page(paginator.num_pages)

    context = {
        'bands': bands,
        'per_page': per_page,
    }
    return render(request, 'band_list.html', context)

def band_detail(request, id):
    band = get_object_or_404(Band, id=id)
    return render(request, 'band_detail.html', {'band': band})

# views.py
def venue_list(request):
    venues = Venue.objects.prefetch_related('room_set').all()
    return render(request, 'venue_list.html', {'venues': venues})

@login_required
def restricted_page(request):
    data = {
        'title': 'Restricted Page',
        'content': '<h1>You are logged in </h1>'
    }
    
    return render(request, "adnew.html", data)


@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    profile = request.user.userprofile
    allowed= False
    
    if profile.musician_profiles.filter(
        id=musician_id).exists():
        allowed = True
    else:
        musician_profiles = set (profile.musician_profiles.all()
    )
    for band in musician.band_set.all():
        band_musician = set(band.musician.all())
        if musician_profiles.intersection(
            band_musician):
            allowed = True
            break
        
        
        if not allowed:
            raise Http404("Permission denied")
        content = f"""
            <h1>Musician Page: {musician.last_name}</h1>
            <p>{musician.first_name}</h1>
            <p>{musician.last_name}</h1>
            <p>{musician.birth}</h1>
        """
        data = {
            'title': 'musician Restricted',
            'content': content,
        }
        
        return render (request, 'musician.html', data)