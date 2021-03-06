"""
Als KCC medewerker wil ik een behandelaar kunnen toewijzen zodat de melding
kan worden gerouteerd.

Ref: https://github.com/VNG-Realisatie/gemma-zaken/issues/45
"""
from rest_framework import status
from rest_framework.test import APITestCase
from zds_schema.constants import RolOmschrijving, RolTypes
from zds_schema.tests import JWTScopesMixin, TypeCheckMixin, get_operation_url

from zrc.api.scopes import SCOPE_ZAKEN_CREATE
from zrc.datamodel.tests.factories import RolFactory, ZaakFactory

WATERNET = 'https://waternet.nl/api/organisatorische-eenheid/1234'


class US45TestCase(JWTScopesMixin, TypeCheckMixin, APITestCase):

    scopes = [SCOPE_ZAKEN_CREATE]

    def test_zet_behandelaar(self):
        zaak = ZaakFactory.create()
        zaak_url = get_operation_url('zaak_read', uuid=zaak.uuid)
        url = get_operation_url('rol_create')

        response = self.client.post(url, {
            'zaak': zaak_url,
            'betrokkene': WATERNET,
            'betrokkeneType': RolTypes.organisatorische_eenheid,
            'rolomschrijving': RolOmschrijving.behandelaar,
            'roltoelichting': 'Verantwoordelijke behandelaar voor de melding',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, response.json())

        response_data = response.json()
        self.assertIn('url', response_data)
        del response_data['url']
        self.assertEqual(response_data, {
            'zaak': f'http://testserver{zaak_url}',
            'betrokkene': WATERNET,
            'betrokkeneType': RolTypes.organisatorische_eenheid,
            'rolomschrijving': RolOmschrijving.behandelaar,
            'roltoelichting': 'Verantwoordelijke behandelaar voor de melding',
        })

    def test_meerdere_initiatoren_verboden(self):
        """
        Uit RGBZ 2.0, deel 2, Attribuutsoort Rolomschrijving (bij relatieklasse
        ROL):

        Bij een ZAAK kan maximaal één ROL met als Rolomschrijving generiek
        'Initiator' voor komen.
        """
        zaak = ZaakFactory.create()
        RolFactory.create(
            zaak=zaak,
            betrokkene_type=RolTypes.natuurlijk_persoon,
            rolomschrijving=RolOmschrijving.initiator
        )
        zaak_url = get_operation_url('zaak_read', uuid=zaak.uuid)
        url = get_operation_url('rol_create')

        response = self.client.post(url, {
            'zaak': zaak_url,
            'betrokkene': WATERNET,
            'betrokkeneType': RolTypes.organisatorische_eenheid,
            'rolomschrijving': RolOmschrijving.initiator,
            'roltoelichting': 'Melder',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_meerdere_coordinatoren_verboden(self):
        """
        Uit RGBZ 2.0, deel 2, Attribuutsoort Rolomschrijving (bij relatieklasse
        ROL):

        Bij een ZAAK kan maximaal één ROL met als Rolomschrijving generiek
        'Initiator' voor komen.
        """
        zaak = ZaakFactory.create()
        RolFactory.create(
            zaak=zaak,
            betrokkene_type=RolTypes.natuurlijk_persoon,
            rolomschrijving=RolOmschrijving.zaakcoordinator
        )
        zaak_url = get_operation_url('zaak_read', uuid=zaak.uuid)
        url = get_operation_url('rol_create')

        response = self.client.post(url, {
            'zaak': zaak_url,
            'betrokkene': WATERNET,
            'betrokkeneType': RolTypes.organisatorische_eenheid,
            'rolomschrijving': RolOmschrijving.zaakcoordinator,
            'roltoelichting': 'Melder',
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
