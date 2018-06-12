import uuid

from django.db import models
from django.utils.crypto import get_random_string

from zrc.validators import alphanumeric_excluding_diacritic


class Zaak(models.Model):
    """
    Modelleer de structuur van een ZAAK.

    Een samenhangende hoeveelheid werk met een welgedefinieerde aanleiding
    en een welgedefinieerd eindresultaat, waarvan kwaliteit en doorlooptijd
    bewaakt moeten worden.
    """
    zaakidentificatie = models.CharField(
        max_length=40, unique=True, blank=True,
        help_text='De unieke identificatie van de ZAAK binnen de organisatie die '
                  'verantwoordelijk is voor de behandeling van de ZAAK.',
        validators=[alphanumeric_excluding_diacritic]
    )
    zaaktype = models.URLField(help_text="URL naar het zaaktype in de CATALOGUS waar deze voorkomt")
    registratiedatum = models.DateField(
        help_text='De datum waarop de zaakbehandelende organisatie de ZAAK heeft geregistreerd'
    )
    toelichting = models.TextField(
        max_length=1000, blank=True,
        help_text='Een toelichting op de zaak.'
    )

    class Meta:
        verbose_name = 'zaak'
        verbose_name_plural = 'zaken'

    def __str__(self):
        return self.zaakidentificatie

    def save(self, *args, **kwargs):
        if not self.zaakidentificatie:
            self.zaakidentificatie = str(uuid.uuid4())
        super().save(*args, **kwargs)

    @property
    def current_status_pk(self):
        status = self.status_set.order_by('-datum_status_gezet').first()
        return status.pk if status else None


class Status(models.Model):
    """
    Modelleer een status van een ZAAK.

    Een aanduiding van de stand van zaken van een ZAAK op basis van
    betekenisvol behaald resultaat voor de initiator van de ZAAK.
    """
    # relaties
    zaak = models.ForeignKey('Zaak', on_delete=models.CASCADE)
    status_type = models.URLField()

    # extra informatie
    datum_status_gezet = models.DateTimeField(
        help_text='De datum waarop de ZAAK de status heeft verkregen.'
    )
    statustoelichting = models.TextField(
        max_length=1000, blank=True,
        help_text='Een, voor de initiator van de zaak relevante, toelichting '
                  'op de status van een zaak.'
    )

    class Meta:
        verbose_name = 'status'
        verbose_name_plural = 'statussen'

    def __str__(self):
        return "Status op {}".format(self.datum_status_gezet)


class ZaakObject(models.Model):
    """
    Modelleer een object behorende bij een ZAAK.

    Het OBJECT in kwestie kan in verschillende andere componenten leven,
    zoals het RSGB.
    """
    zaak = models.ForeignKey('Zaak', on_delete=models.CASCADE)
    object = models.URLField(help_text='URL naar de resource die het OBJECT beschrijft.')
    relatieomschrijving = models.CharField(
        max_length=80, blank=True,
        help_text='Omschrijving van de betrekking tussen de ZAAK en het OBJECT.'
    )

    class Meta:
        verbose_name = 'zaakobject'
        verbose_name_plural = 'zaakobjecten'


class DomeinData(models.Model):
    """
    Modelleer domeindata die behoort tot een ZAAK.

    Domeindata kan buiten het ZRC leven, zoals specifiek in een vakapplicatie.
    Dit model staat niet beschreven in RGBZ 2.0, maar er blijkt wel een
    noodzaak voor te zijn.

    TODO/vraagstukken:

    * hoe vendor locking voorkomen?
    * hoe mogelijk maken dat deze data door verschillende componenten/applicaties
     'begrepen' wordt?

    """
    zaak = models.ForeignKey('Zaak', on_delete=models.CASCADE)
    domein_data = models.URLField(help_text="URL naar de domein data resource")

    class Meta:
        verbose_name = 'domeindatareferentie'
        verbose_name_plural = 'domeindatareferenties'


class KlantContact(models.Model):
    """
    Modelleer het contact tussen een medewerker en een klant.

    Een uniek en persoonlijk contact van een burger of bedrijfsmedewerker met
    een MEDEWERKER van de zaakbehandelende organisatie over een onderhanden of
    afgesloten ZAAK.
    """
    zaak = models.ForeignKey('Zaak', on_delete=models.CASCADE)
    identificatie = models.CharField(
        max_length=14, unique=True,
        help_text='De unieke aanduiding van een KLANTCONTACT'
    )
    datumtijd = models.DateTimeField(
        help_text='De datum en het tijdstip waarop het KLANTCONTACT begint'
    )
    kanaal = models.CharField(
        blank=True, max_length=20,
        help_text='Het communicatiekanaal waarlangs het KLANTCONTACT gevoerd wordt'
    )

    class Meta:
        verbose_name = "klantcontact"
        verbose_name_plural = "klantcontacten"

    def __str__(self):
        return self.identificatie

    def save(self, *args, **kwargs):
        if not self.identificatie:
            gen_id = True
            while gen_id:
                identificatie = get_random_string(length=12)
                gen_id = self.__class__.objects.filter(identificatie=identificatie).exists()
            self.identificatie = identificatie
        super().save(*args, **kwargs)


class ZaakInformatieObject(models.Model):
    """
    Modelleer een INFORMATIEOBJECT horend bij een ZAAK.

    INFORMATIEOBJECTen zijn bestanden die in het DRC leven. Een collectie van
    (enkelvoudige) INFORMATIEOBJECTen wordt ook als 1 enkele resource ontsloten.
    """
    zaak = models.ForeignKey('Zaak', on_delete=models.CASCADE)
    informatieobject = models.URLField(help_text="URL naar het INFORMATIEOBJECT in het DRC.")

    class Meta:
        verbose_name = 'Zaakinformatieobject'
        verbose_name_plural = 'Zaakinformatieobjecten'
