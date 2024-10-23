from feasto_core_clean_arch.exceptions.custom_exceptions import InvalidRestaurantId
from feasto_core_clean_arch.interactors.storage_interfaces.storage_interface import UpdateRestaurantDTO
from feasto_core_clean_arch.interactors.update_restaurant_interactor import UpdateRestaurantInteractor
from feasto_core_clean_arch.presenters.presenter_implementation import PresenterImplementation
from feasto_core_clean_arch.storages.storage_implementation import StorageImplementation
from feasto_gql.restaurant.types.types import UpdateRestaurantParams, Restaurant, RestaurantResponse, RestaurantNotFound
import graphene
from feasto_core_clean_arch.models import Restaurant as RestaurantModel

class UpdateRestaurant(graphene.Mutation):
    class Arguments:
        params = UpdateRestaurantParams(required=True)

    Output = RestaurantResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = UpdateRestaurantInteractor(storage=storage)

        update_restaurant_dto = UpdateRestaurantDTO(rest_id=params.id, name=params.name, status=params.status,
                                                 user_id=params.user_id)
        try:
            rest = interactor.update_restaurant(update_restaurant_dto=update_restaurant_dto)
        except InvalidRestaurantId:
            return RestaurantNotFound(restaurant_id=params.id)


        return RestaurantResponse(restaurant= Restaurant(
            id=str(rest.id),
            name=rest.name,
            location=rest.location,
            status=rest.status
        ))