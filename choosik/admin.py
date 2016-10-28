from django.contrib import admin
from models import *

# Register your models here.

class UtenteAdmin(admin.ModelAdmin):
    model = Utente
    search_fields = ('username',)

class CanzoneAdmin(admin.ModelAdmin):
    model = Canzone
    search_fields = ('titolo', 'autore__nome')
    list_display = ('titolo', 'autore')
    list_filter = ('autore',)

class CanzoneInTappaInLine(admin.TabularInline):
    model = CanzoneInTappa

    raw_id_fields = ('canzone', 'tappa')

class TappaAdmin(admin.ModelAdmin):
    model = Tappa
    list_display = ('tour', 'citta', 'data')
    search_fields = ('citta', 'tour__nome', 'tour__artista__username')
    list_filter = ('citta',)

    inlines = [CanzoneInTappaInLine, ]

class TappaInLine(admin.TabularInline):
    model = Tappa

class TourAdmin(admin.ModelAdmin):
    model = Tour
    inlines = [TappaInLine,]
    raw_id_fields = ('artista',)
    list_display = ('nome', 'artista')
    search_fields = ('artista__username','nome')

admin.site.register(Utente, UtenteAdmin)
admin.site.register(Canzone, CanzoneAdmin)
admin.site.register(Tour, TourAdmin)
admin.site.register(Tappa, TappaAdmin)
admin.site.register(CanzoneInTappa)
admin.site.register(VotoCanzoneInTappa)
