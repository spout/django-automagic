from django.apps import apps


def get_app_models(app_label, models=[]):
    """
    Get all the models of an app, if models_list is not empty return only these
    """
    app_config = apps.get_app_config(app_label)

    if models:
        return [app_config.get_model(model_name) for model_name in models]
    else:
        return app_config.get_models()
