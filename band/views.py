from django.shortcuts import render,get_object_or_404
from .models import Musician 
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from django.shortcuts  import render
from band.models import Musician, UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from band.form import VenueForm

def viewAllBands(request):
    musicians_list = Musician.objects.all()
    paginator = Paginator(musicians_list, 10) 

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
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
        per_page = min(max(1, per_page), 50)  # Constrain between 1-50
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
        per_page = min(max(1, per_page), 50)
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
        'content': '<h1>You are logged in</h1>',

    }    

    return render(request,"general.xhtml", data)


...
from django.http import Http404  
...
@login_required
def musician_restricted(request, musician_id):
    musician = get_object_or_404(Musician, id=musician_id)
    profile = request.user.userprofile  
    allowed = False  

    if profile.musician_profiles.filter(  
        id=musician_id).exists():
        allowed = True
    else:
        
        musician_profiles = set(
            profile.musician_profiles.all()  
        )
        for band in musician.band_set.all():
            band_musicians = set(band.musicians.all())
            if musician_profiles.intersection(
                band_musicians):  
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
        'title': 'Musician Restricted',
        'content': content,
    }

    return render(request, "general.xhtml", data)   

@receiver(post_save,sender=User)
def create_user_profile(sender, **kwargs):
        if kwargs['created'] and not kwargs['raw']:
            user = kwargs['instance']
            try:
                UserProfile.objects.get(user=user)
            except UserProfile.DoesNotExist:
                UserProfile.objects.create(user=user)
@login_required
def edit_venue(request, venue_id=0):
    if venue_id !=0:
        venue = get_object_or_404(Venue,
           id=venue_id)
        if not request.user.userprofile.venue_controlled.filter(
            id=venue_id).exists():
           raise Http404("can only edit controlled venues")
       
    if request.method == 'GET':
        if venue_id == 0:
            form = VenueForm()
        else:
            form = VenueForm(instance=venue)
            
    else:
        if venue_id == 0:
            venue = Venue.object.create()
            
        form = VenueForm(request.POST, request.FILES,
            instance=venue)
        
        if form.is_valid():
            venue = form.save()
            
            
    data = {
        "form": form,
    }
    
    return render(request, "edit_venue.html", data)