from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from band.models import Musician, Band
from datetime import date, datetime

class DecadeListFilter(admin.SimpleListFilter):
    title = 'decade of birth'
    parameter_name = 'decade'
    
    def lookups(self, request, model_admin):
        result = []
        this_year = datetime.now().year
        # Generate decades from 1900 up to the current decade
        for start in range(1900, this_year + 1, 10):
            end = start + 9
            # Ensure we don't go beyond current year for the end of the decade
            end = min(end, this_year)
            result.append((start, f'{start}-{end}'))
        return result
    
    def queryset(self, request, queryset):
        value = self.value()
        if not value:
            return queryset
        start = int(value)
        end_year = min(start + 9, datetime.now().year)
        return queryset.filter(
            birth__gte=date(start, 1, 1),
            birth__lte=date(end_year, 12, 31)
        )

@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'birth', 'show_weekday', 'show_bands')
    search_fields = ('first_name__startswith', 'last_name__startswith')
    list_filter = (DecadeListFilter,)
    
    def show_weekday(self, obj):
        return obj.birth.strftime('%A')
    show_weekday.short_description = 'Weekday of Birth'
    
    def show_bands(self, obj):
        bands = obj.band_set.all()
        if not bands.exists():
            return format_html('<i>no bands</i>')
        
        count = bands.count()
        plural = 's' if count > 1 else ''
        band_ids = bands.values_list('id', flat=True)
        url = (
            reverse('admin:band_band_changelist') 
            + f'?musician__id__exact={obj.id}'
        )
        return format_html(
            '<a href="{}">{} band{}</a>',
            url,
            count,
            plural
        )
    show_bands.short_description = 'Bands'

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    ordering = ('name',)
    list_display = ('name', 'genre', 'founded')