from django.core.mail import send_mail
from django.shortcuts import render, redirect,get_object_or_404
from content.models import MusicianBandChoice,SeekingAd
from django.contrib.auth.decorators import login_required
from content.form import SeekingAdForm
from content.models import MusicianBandChoice,SeekingAd

from content.form import CommentForm

def comment(request):
    if request.method == 'GET':
        form = CommentForm()
    else:
        form = CommentForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            comment = form.cleaned_data['comment']
            message = f"""\
            Recieved comment from {name}\n\n
            {comment}
            """
            send_mail("Recieved comment", message, 'admin@example.com', ['admin@example.com'], fail_silently=False)
            return redirect('comment_accepted')
    data={
        "form":form,
    }
    return render(request, 'comment.html', data)

def comment_accepted(request):
    data ={
        "content":"""
        <h1> Comment accepted</h1>
        <p>Thank you for your comment to <i>Riffmates</i></p>
        """
    }
    return render(request, 'general.html', data)


def list_ads(request):
    data ={
        'seeking_musician':SeekingAd.objects.filter(seeking=MusicianBandChoice.MUSICIAN),
        'seeking_band':SeekingAd.objects.filter(seeking=MusicianBandChoice.BAND),
    }
    return render(request, 'registration/list_ads.html', data)

@login_required
def seeking_ad(request, ad_id=0):
    if request.method == 'GET':
        if ad_id == 0:
            form = SeekingAdForm()
        else:
            ad = get_object_or_404(SeekingAd, id = ad_id, owner = request.user)
            form = SeekingAdForm(instance=ad)
    if request.method == 'POST':
        if ad_id == 0:
            form = SeekingAdForm(request.POST)
        else:
            ad = get_object_or_404(SeekingAd, id= ad_id,
                                   owner = request.user)
            form = SeekingAdForm(request.POST, instance=ad)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.owner = request.user
            ad.save()

            return redirect("list_ads")
            
    data = {
        "form": form,
    }    
    return render(request, "registration/Seeking_ad.html", data)