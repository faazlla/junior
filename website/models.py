from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.utils import timezone
import os
import uuid


def generate_unique_filename(instance, filename):
    jedinstveni_id = str(uuid.uuid4())[:8]
    vremenski_zig = timezone.now().strftime("%Y-%m-%d_%H-%M-%S")
    originalna_ime, ekstenzija = os.path.splitext(filename)
    jedinstveni_naziv_slike = f"{vremenski_zig}_{jedinstveni_id}{ekstenzija}"
    return os.path.join('images/', jedinstveni_naziv_slike)

class Language(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Junior(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='junior')
    ime_i_prezime = models.CharField(max_length=100)
    primarni_jezik = models.ForeignKey(Language, on_delete=models.CASCADE)
    email = models.EmailField()
    broj_telefona = models.CharField(max_length=15)
    kratak_opis = models.TextField()
    dodatni_it_skilovi = models.TextField()
    git_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    portfolio_link = models.URLField(blank=True, null=True)
    pdf_cv = models.FileField(blank=True, null=True, upload_to=generate_unique_filename)
    image = models.ImageField(null=False, blank=False, upload_to=generate_unique_filename)
    prosjecna_ocjena = models.FloatField(default=0)  # Polje za prosječnu ocjenu
    broj_ocjena = models.PositiveIntegerField(default=0)  # Broj ocjena koje je junior dobio

    def calculate_average_rating(self):
        ocjene = Ocjena.objects.filter(ocijenjeni_junior=self)
        broj_ocjena = ocjene.count()
        suma_ocjena = ocjene.aggregate(models.Sum('ocjena'))['ocjena__sum'] or 0
        self.broj_ocjena = broj_ocjena
        self.prosjecna_ocjena = suma_ocjena / broj_ocjena if broj_ocjena > 0 else 0
        self.save()
        
    def __str__(self):
        return self.ime_i_prezime


class Ocjena(models.Model):
    ocjenjivac = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ocjenjivac')
    ocijenjeni_junior = models.ForeignKey(Junior, on_delete=models.CASCADE, related_name='ocjenjeni_junior')
    ocjena = models.PositiveIntegerField(choices=((1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')))

    class Meta:
        unique_together = ('ocjenjivac', 'ocijenjeni_junior')  # Definirajte kombinaciju koja mora biti jedinstvena
    
    def save(self, *args, **kwargs):
        super(Ocjena, self).save(*args, **kwargs)
        self.ocijenjeni_junior.calculate_average_rating()  # Nakon što se ocjena spremi, izračunaj prosječnu ocjenu juniora

    def __str__(self):
        return f'{self.ocjenjivac.username} ocijenio/la {self.ocijenjeni_junior.ime_i_prezime} sa ocjenom {self.ocjena}'

