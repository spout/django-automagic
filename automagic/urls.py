from .utils import get_app_models


def app_urlpatterns(app_label, models=[], actions={}):
    urlpatterns = []
    for model in get_app_models(app_label, models):
        model_instance = model()
        actions_list = actions.get(model_instance.__class__.__name__, [])
        urlpatterns += model_instance.get_urlpatterns(model, actions_list)
    return urlpatterns