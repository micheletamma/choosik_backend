from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Utente(models.Model):
    class Meta:
        verbose_name = 'Utente'
        verbose_name_plural = 'Utenti'

    # user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    username = models.CharField(max_length=64, null=False, blank=False, unique=True)
    password = models.CharField(max_length=64, null=False, blank=False)
    email = models.CharField(max_length=64, null=False, blank=False)
    nome = models.CharField(max_length=64, null=True, blank=True)
    citta = models.CharField(max_length=64, null=True, blank=True)
    provincia = models.CharField(max_length=64, null=True, blank=True)
    nazione = models.CharField(max_length=64, default="Italia")
    artista = models.BooleanField(default=False)

    def __unicode__(self):
        return self.username

        # @receiver(post_save, sender=User)
        # def create_user_profile(sender, instance, created, **kwargs):
        #     if created:
        #         Utente.objects.create(user=instance)
        #
        # @receiver(post_save, sender=User)
        # def save_user_profile(sender, instance, **kwargs):
        #     instance.profile.save()


class Canzone(models.Model):
    titolo = models.CharField(max_length=64, null=False, blank=False)
    autore = models.ForeignKey(Utente)

    class Meta:
        unique_together = (("titolo", "autore"),)
        verbose_name = 'Canzone'
        verbose_name_plural = 'Canzoni'

    def __unicode__(self):
        return self.titolo + ' - ' + unicode(self.autore.nome)


class Tour(models.Model):
    nome = models.CharField(max_length=128, blank=False, null=False)
    artista = models.ForeignKey(Utente)

    class Meta:
        unique_together = (("nome", "artista"),)
        verbose_name = 'Tour'
        verbose_name_plural = 'Tours'

    def __unicode__(self):
        return self.nome + ' -di- ' + self.artista.username


class Tappa(models.Model):
    citta = models.CharField(max_length=64, null=False, blank=False)
    data = models.DateField()
    tour = models.ForeignKey(Tour)

    class Meta:
        unique_together = (("citta", "data", "tour"),)
        verbose_name = 'Tappa'
        verbose_name_plural = 'Tappe'

    def __unicode__(self):
        return self.tour.nome + ' a ' + self.citta + ' del ' + unicode(self.data)


class CanzoneInTappa(models.Model):
    canzone = models.ForeignKey(Canzone)
    tappa = models.ForeignKey(Tappa)
    votoMedio = models.FloatField(null=True, blank=True, default=0)
    numeroVoti = models.IntegerField(null=True, blank=True, default=0)

    class Meta:
        unique_together = (("canzone", "tappa"),)
        verbose_name = 'Canzone in tappa'
        verbose_name_plural = 'Canzoni in tappa'

    def __unicode__(self):
        return self.canzone.titolo + self.tappa.citta + unicode(self.tappa.data) + self.tappa.tour.nome


class VotoCanzoneInTappa(models.Model):
    utente = models.ForeignKey(Utente)
    canzoneInTappa = models.ForeignKey(CanzoneInTappa)
    votoNum = models.IntegerField()

    class Meta:
        unique_together = (("utente", "canzoneInTappa"),)
        verbose_name = 'Voto canzone in tappa'
        verbose_name_plural = 'Voti canzone in tappa'

    def __unicode__(self):
        return self.utente.username + ' ' + self.canzoneInTappa.canzone.titolo + ' ' + unicode(
            self.canzoneInTappa.tappa.data) + ' ' + self.canzoneInTappa.tappa.citta

    # modifica metodo save per aggiornare il voto medio della canzone in tappa appena votata
    # con troncamento a 2 cifre decimali.
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        canzone = CanzoneInTappa.objects.get(id=self.canzoneInTappa_id)
        canzone.votoMedio=(canzone.votoMedio*canzone.numeroVoti + self.votoNum)/(canzone.numeroVoti + 1)
        canzone.votoMedio="%.2f" % canzone.votoMedio
        canzone.numeroVoti += 1
        canzone.save()
        super(VotoCanzoneInTappa, self).save()
