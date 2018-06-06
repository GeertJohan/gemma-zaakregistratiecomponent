REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    # 'DEFAULT_AUTHENTICATION_CLASSES': (
    #     'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    #     # 'rest_framework.authentication.SessionAuthentication',
    #     # 'rest_framework.authentication.BasicAuthentication'
    # ),
    # 'DEFAULT_PERMISSION_CLASSES': (
    #     'oauth2_provider.contrib.rest_framework.TokenHasReadWriteScope',
    #     # 'rest_framework.permissions.IsAuthenticated',
    #     # 'rest_framework.permissions.AllowAny',
    # ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning',
    #
    # # Generic view behavior
    # 'DEFAULT_PAGINATION_CLASS': 'ztc.api.utils.pagination.HALPagination',
    # 'DEFAULT_FILTER_BACKENDS': (
    #     'django_filters.rest_framework.DjangoFilterBackend',
    #     'rest_framework.filters.SearchFilter',
    #     'rest_framework.filters.OrderingFilter',
    # ),
    #
    # # Filtering
    # 'SEARCH_PARAM': 'zoek',  # 'search',
    # 'ORDERING_PARAM': 'sorteer',  # 'ordering',
    #
    # Versioning
    'DEFAULT_VERSION': 1,
    'ALLOWED_VERSIONS': (1, ),
    'VERSION_PARAM': 'version',
    #
    # # Exception handling
    # 'EXCEPTION_HANDLER': 'ztc.api.utils.exceptions.exception_handler',
}
