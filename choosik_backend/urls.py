"""choosik_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin


from choosik.api import *

utente_resource = UtenteResource()
canzone_resource = CanzoneResource()
tour_resource = TourResource()
tappa_resource = TappaResource()
canzoneInTappa_resource = CanzoneInTappaResource()
votoCanzoneInTappa_resource = VotoCanzoneInTappaResource()



urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(utente_resource.urls)),
    url(r'^api/', include(canzone_resource.urls)),
    url(r'^api/', include(tour_resource.urls)),
    url(r'^api/', include(tappa_resource.urls)),
    url(r'^api/', include(canzoneInTappa_resource.urls)),
    url(r'^api/', include(votoCanzoneInTappa_resource.urls)),
]
