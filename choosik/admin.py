from django.contrib import admin
from models import *

# Register your models here.

admin.site.register(Utente)
admin.site.register(Canzone)
admin.site.register(Tour)
admin.site.register(Tappa)
admin.site.register(CanzoneInTappa)
admin.site.register(VotoCanzoneInTappa)
