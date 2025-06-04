from django import forms
from content.models import SeekingAd

class CommentForm(forms.Form):
    name = forms.CharField(max_length=100, required=True, label='Your Name')
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), required=True, label='Your Comment')

class SeekingAdForm(forms.ModelForm):
    class Meta:
        model = SeekingAd
        fields = ['seeking', 'musician', 'band', 'content']

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        self.fields['seeking'].label = "I am seeking a"
        self.fields['musician'].help_text="Fill in if you are seeking a musician"
        self.fields['band'].help_text="Fill in if you are seeking a band"