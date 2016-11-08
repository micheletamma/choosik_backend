from django.db.models import Q
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.constants import ALL_WITH_RELATIONS
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
            "password": ('exact',),
            "artista":('exact',),
            "nome": ('exact',),


        }


class CanzoneResource(ModelResource):
    autore = fields.ToOneField(UtenteResource, 'autore', full=True)
    class Meta:
        queryset = Canzone.objects.all()
        resource_name = 'canzone'
        authorization = Authorization()
        filtering = {
            "autore": ALL_WITH_RELATIONS,
            "titolo":('contains',),
            "titolocontains": ['icontains',],
        }

    def build_filters(self, filters=None):

        if filters is None:  # if you don't pass any filters at all
            filters = {}
        orm_filters = super(CanzoneResource, self).build_filters(filters)
        if ('titolocontains' in filters):
            query = filters['titolocontains']
            #qset = query
            qset = (
                Q(titolo__icontains=query)
            )
            print qset
            orm_filters.update({'custom': qset})
        return orm_filters

    def apply_filters(self, request, applicable_filters):
        if 'custom' in applicable_filters:
            custom = applicable_filters.pop('custom')
            print custom
            #return Canzone.objects.filter(titolo__icontains=custom)
        else:
            custom = None

        semi_filtered = super(CanzoneResource, self).apply_filters(request, applicable_filters)

        return semi_filtered.filter(custom) if custom else semi_filtered


class TourResource(ModelResource):
    artista = fields.ForeignKey(UtenteResource, 'artista', full=True)
    nomeTour = fields.CharField('nome')

    class Meta:
        queryset = Tour.objects.all()
        resource_name = 'tour'
        authorization = Authorization()
        filtering = {
            "artista": ALL_WITH_RELATIONS,
            "id": ('exact',),
        }
        allowed_methods = ['get', 'post', 'delete']


class TappaResource(ModelResource):

    tour = fields.ForeignKey(TourResource, 'tour', full=True)


    class Meta:
        queryset = Tappa.objects.all()
        resource_name = 'tappa'
        authorization = Authorization()
        allowed_methods = ['get','post', 'delete']
        filtering = {
            "citta": ('exact',),
            "data": ('exact',),
            "id":('exact',),
            "tour": ALL_WITH_RELATIONS,

        }

class CanzoneInTappaResource(ModelResource):

    canzone = fields.ForeignKey(CanzoneResource, 'canzone', full=True)
    tappa = fields.ForeignKey(TappaResource, 'tappa', full=True)

    class Meta:
        queryset = CanzoneInTappa.objects.all()
        resource_name = 'canzoneintappa'
        authorization = Authorization()
        filtering = {
            "tappa": ALL_WITH_RELATIONS,
            "canzone": ALL_WITH_RELATIONS,
        }
        allowed_methods = ['get', 'post', 'delete']

class VotoCanzoneInTappaResource(ModelResource):

    utente = fields.ForeignKey(UtenteResource, 'utente', full=True)
    canzoneInTappa = fields.ForeignKey(CanzoneInTappaResource, 'canzoneInTappa', full=True)

    class Meta:
        queryset = VotoCanzoneInTappa.objects.all()
        resource_name = 'votocanzoneintappa'
        authorization = Authorization()
        filtering = {
            "canzoneInTappa":ALL_WITH_RELATIONS,
            "utente": ALL_WITH_RELATIONS,
        }

class MieiConcertiResource(ModelResource):

    tour = fields.ForeignKey(TourResource, 'tour', full=True)

    # la querset di tappa andra' filtrata in base a varie informazioni prelevate da vari modelli, le informazioni
    # verranno prelevate nel metodo get_object_list.
    class Meta:
        queryset = Tappa.objects.all()
        resource_name = 'mieiconcerti'
        authorization = Authorization()

    # la return di questo metodo si riferisce al campo queryset del Meta, dunque fa un filtraggio sugli id delle tappe
    # dove l'utente ha votato almeno una canzone.
    def get_object_list(self, request):

        username = request.GET['username']
        myVoti = VotoCanzoneInTappa.objects.filter(utente__username=username)
        myVoti = list(myVoti)
        mytappeIds = list()
        for v in myVoti:
            if not (mytappeIds.__contains__(v.canzoneInTappa.tappa.id)):
                mytappeIds.append(v.canzoneInTappa.tappa.id)
        return super(MieiConcertiResource, self).get_object_list(request).filter(id__in = mytappeIds)

class CanzoniInTappaVotateResource(ModelResource):

    class Meta:
        queryset = CanzoneInTappa.objects.all()
        resource_name = 'canzoniintappavotate'
        authorization = Authorization()
        filtering = {
            "tappa": ALL_WITH_RELATIONS,
            "canzone": ALL_WITH_RELATIONS,
            "id":('exact',),
        }

    canzone = fields.ForeignKey(CanzoneResource, 'canzone', full=True)
    tappa = fields.ForeignKey(TappaResource, 'tappa', full=True)

    def get_object_list(self, request):
        return super(CanzoniInTappaVotateResource, self).get_object_list(request).filter(tappa=request.GET['idTappa'])

    # viene passato al vaglio ogni canzone in tappa.
    def dehydrate(self, bundle):
        username = bundle.request.GET['username']
        idCanzoneInTappa = bundle.data['id']
        voto = VotoCanzoneInTappa.objects.filter(canzoneInTappa=idCanzoneInTappa, utente__username=username)
        if voto.__len__() == 1:
            bundle.data['votata'] = True
            for v in voto:
                bundle.data['numVoto'] = v.votoNum
        else:
            bundle.data['votata'] = False
        return super(CanzoniInTappaVotateResource, self).dehydrate(bundle)
