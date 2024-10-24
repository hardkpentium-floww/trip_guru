
from trip.interactors.logout_interactor import LogoutInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip.views.logout.validator_class import ValidatorClass
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    user_id = kwargs['user'].id

    storage = StorageImplementation()
    interactor = LogoutInteractor(storage=storage)

    return interactor.logout(user_id=user_id)

