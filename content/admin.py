from django.contrib import admin
from django.utils.text import Truncator
from content.models import SeekingAd

@admin.register(SeekingAd)
class SeekingAdAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'seeking', 'date','show_ad')
    list_filter = ('seeking', 'owner')

    def show_ad(self, obj):
        return Truncator(obj.content).words(5, truncate='...')
    show_ad.show_short_description = 'Ad Content'