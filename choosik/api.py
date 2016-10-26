from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from models import *



# class UserResource(ModelResource):
#
#     class Meta:
#         queryset = User.objects.all()
#         resource_name = 'users'
#         authorization = Authorization()
#         allowed_methods = ['post', 'get']

from django.db.models import signals
from tastypie.models import create_api_key

#signals.post_save.connect(create_api_key, sender=User)


class UtenteResource(ModelResource):

    class Meta:
        queryset = Utente.objects.all()
        resource_name = 'utente'
        authorization = Authorization()
        allowed_methods = ['post', 'get']
        filtering = {
            "username": ('exact',),
            "password": ('exact',)
        }


class CanzoneResource(ModelResource):
    autore = fields.ToOneField(UtenteResource, 'autore', full=True)
    class Meta:
        queryset = Canzone.objects.all()
        resource_name = 'canzone'
        authorization = Authorization()



class TourResource(ModelResource):
    artista = fields.ForeignKey(UtenteResource, 'artista', full=True)

    class Meta:
        queryset = Tour.objects.all()
        resource_name = 'tour'
        authorization = Authorization()


class TappaResource(ModelResource):

    tour = fields.ForeignKey(TourResource, 'tour', full=True)

    class Meta:
        queryset = Tappa.objects.all()
        resource_name = 'tappa'
        authorization = Authorization()
        allowed_methods = ['get',]
        filtering = {
            "citta": ('exact',),
        }

class CanzoneInTappaResource(ModelResource):

    canzone = fields.ForeignKey(CanzoneResource, 'canzone', full=True)
    tappa = fields.ForeignKey(TappaResource, 'tappa', full=True)

    class Meta:
        queryset = CanzoneInTappa.objects.all()
        resource_name = 'canzoneintappa'
        authorization = Authorization()
