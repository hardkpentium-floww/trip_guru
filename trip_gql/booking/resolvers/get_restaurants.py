
from feasto_core_clean_arch.exceptions.custom_exceptions import InvalidRestaurantId
from feasto_core_clean_arch.interactors.get_restaurants_interactor import GetRestaurantsInteractor
from feasto_core_clean_arch.interactors.storage_interfaces.storage_interface import GetRestaurantDTO
from feasto_core_clean_arch.presenters.presenter_implementation import PresenterImplementation
from feasto_core_clean_arch.storages.storage_implementation import StorageImplementation
from feasto_gql.restaurant.types.types import Restaurant, RestaurantNotFound, GetRestaurantsParams
from feasto_core_clean_arch.models import Restaurant as RestaurantModel

def resolve_get_restaurants(self, info):
    # Fetch all restaurants
    class Arguments:
        params = GetRestaurantsParams(required=True)

    storage = StorageImplementation()
    presenter = PresenterImplementation()
    interactor = GetRestaurantsInteractor(storage=storage)

    get_restaurant_dto = GetRestaurantDTO(
        status=self.params.status,
        location=self.params.location,
        offset=self.params.offset,
        limit=self.params.limit
    )
    try:
        restaurants_dto =  interactor.get_restaurants_wrapper(get_restaurant_dto=get_restaurant_dto, presenter= presenter)
    except InvalidRestaurantId:
        return RestaurantNotFound(restaurant_id=self.params.id)

    return [Restaurant(
        id=str(restaurant.id),
        name=restaurant.name,
        location=restaurant.location,
        status=restaurant.status,
    ) for restaurant in restaurants_dto]