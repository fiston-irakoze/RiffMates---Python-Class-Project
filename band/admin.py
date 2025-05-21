from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from band.models import Musician,Band,Venue,Room,UserProfile
from datetime import date,datetime

class DecadeListFilter(admin.SimpleListFilter):
    title='decade of birth'
    parameter_name = 'decade'

    def lookups(self, request, model_admin):
        result = []
        this_year = datetime.now().year
        for i in range(1900, this_year, 10):
            result.append((i, str(i) + '-' + str(i+9)))
        return result

    def queryset(self, request, queryset):
        start=self.value()
        if start is None:
            return queryset
        start=int(start)
        return queryset.filter(birth_gte=date(start, 1, 1), birth_lte=date(start+9, 12, 31))
@admin.register(Musician)
class MusicianAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name','last_name', 'birth', 'show_weekday', 'show_bands')
    search_fields=('first_name__startswith',)
    list_filter = (DecadeListFilter,)
    

    def show_weekday(self, obj):
        return obj.birth.strftime('%A')
    show_weekday.short_description = 'Weekday of birth'

    def show_bands(self, obj):
        bands=obj.band_set.all()
        if len(bands)==0:
            return format_html('<i>no bands</i>')   
        plural = 's' if len(bands)>1 else ''
        param ='?id__in='+','.join([str(band.id) for band in bands])
        url = reverse('admin:bands_band_changelist')+param
        return format_html('<a href="{}">{}band</a>', url, len(bands),plural)
    show_bands.short_description = 'Bands'

@admin.register(Band)
class BandAdmin(admin.ModelAdmin):
    class Meta:
        ordering =('name',)
        
class UserProfileInline(admin.StackedInline):
    model=UserProfile
    can_delete=False
class UserAdmin(BaseUserAdmin):
    inlines=[UserProfileInline]
    
admin.site.unregister(User)
admin.site.register(User,UserAdmin)