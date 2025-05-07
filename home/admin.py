from django.contrib import admin
from band.models import Musician, Band, Venue, Room  
from datetime import datetime
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class DecadeListFilter(admin.SimpleListFilter):
    title = 'Decade'
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        result = []
        this_year = datetime.now().year
        for i in range(1900, this_year + 10, 10):
            result.append((i, f'{i}-{i + 9}'))
        return result

    def queryset(self, request, queryset):
        if self.value():
            start_year = int(self.value())
            end_year = start_year + 9
            return queryset.filter(birth__year__gte=start_year, birth__year__lte=end_year)
        return queryset

@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'show_birth', 'show_weekday', 'show_bands')
    search_fields = ['first_name__startswith']
    list_filter = (DecadeListFilter, 'birth')
    ordering = ['first_name']  # Default sorting

    def show_birth(self, obj):
        return obj.birth.strftime("%Y-%m-%d")
    show_birth.short_description = 'Birth Date'

    def show_weekday(self, obj):
        return obj.birth.strftime("%A")
    show_weekday.short_description = 'Day of the week'

    def show_bands(self, obj):
        bands = obj.band_set.all()
        if not bands:
            return format_html("<span style='color: red;'>No bands</span>")
        return mark_safe(", ".join([f'<a href="/admin/band/band/{b.id}/">{b.name}</a>' for b in bands]))
    show_bands.short_description = 'Bands'

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name__startswith']
    ordering = ['name']

@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'show_rooms')
    search_fields = ['name__startswith']
    ordering = ['name']  # Default sorting

    def show_rooms(self, obj):
        rooms = obj.room_set.all()
        if not rooms:
            return format_html("<span style='color: red;'>No rooms</span>")
        return mark_safe(", ".join([f'<a href="/admin/band/room/{r.id}/">{r.name}</a>' for r in rooms]))
    show_rooms.short_description = 'Rooms'

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'show_venue')
    search_fields = ['name__startswith']
    ordering = ['name']  # Default sorting

    def show_venue(self, obj):
        if obj.venue:
            return mark_safe(f'<a href="/admin/band/venue/{obj.venue.id}/">{obj.venue.name}</a>')
        return format_html("<span style='color: red;'>No venue</span>")
    show_venue.short_description = 'Venue'