import os
import sys

from zds_schema.conf.api import *  # noqa - imports white-listed

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()


SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()
SWAGGER_SETTINGS.update({
    'DEFAULT_INFO': 'zrc.api.schema.info',
})

GEMMA_URL_INFORMATIEMODEL_VERSIE = '1.0'


NLX_SERVICE = os.getenv('NLX_SERVICE', 'zrc')
NLX_INWAY_ADDRESS = os.getenv('NLX_ADDRESS', 'localhost:8000')  # TODO: support subpaths?
NLX_ORGANISATION = os.getenv('NLX_ORGANISATION', 'vng-realisatie')
NLX_OUTWAY_ADDRESS = os.getenv('NLX_OUTWAY_ADDRESS', 'http://localhost:2018')

if 'test' in sys.argv:
    NLX_URL_REWRITE_ENABLED = False
