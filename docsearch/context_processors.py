from django.apps import apps

import docsearch.models


def models(request):
    """
    Return all Models in the docsearch app corresponding to document types.
    """
    docs = [Model for Model in apps.get_app_config('docsearch').get_models()
            if issubclass(Model, docsearch.models.BaseDocumentModel)]
    return {'models': docs}
