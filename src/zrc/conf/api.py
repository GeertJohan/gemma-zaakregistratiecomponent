from zds_schema.conf.api import *  # noqa - imports white-listed

REST_FRAMEWORK = BASE_REST_FRAMEWORK.copy()

REST_FRAMEWORK['PAGE_SIZE'] = 100


SWAGGER_SETTINGS = BASE_SWAGGER_SETTINGS.copy()
SWAGGER_SETTINGS.update({
    'DEFAULT_INFO': 'zrc.api.schema.info',
})

GEMMA_URL_INFORMATIEMODEL_VERSIE = '1.0'
