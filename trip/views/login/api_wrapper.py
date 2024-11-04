
from django_swagger_utils.drf_server.utils.decorator.interface_decorator \
    import validate_decorator

from trip.views.login.validator_class import ValidatorClass
from ...models.user import User
from ...interactors.login_interactor import LoginInteractor
from ...storages.storage_implementation import StorageImplementation


@validate_decorator(validator_class=ValidatorClass)
def api_wrapper(*args, **kwargs):
    phone_no = kwargs['request_data']['phone_no']
    user_id = User.objects.get(phone_no = phone_no).id

    storage = StorageImplementation()
    interactor = LoginInteractor(storage=storage)

    return interactor.login(user_id=user_id)
