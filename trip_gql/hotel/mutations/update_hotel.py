import graphene

from trip.exceptions.custom_exceptions import InvalidAdminUser
from trip.interactors.storage_interfaces.storage_interface import MutateHotelDTO
from trip.interactors.update_hotel_interactor import UpdateHotelInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.common_errors import UserNotAuthorized
from trip_gql.hotel.types.types import Hotel, AddHotelResponse, AddHotelParams, UpdateHotelParams, UpdateHotelResponse


class UpdateHotel(graphene.Mutation):
    class Arguments:
        params = UpdateHotelParams(required=True)

    Output = UpdateHotelResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = UpdateHotelInteractor(storage=storage)

        update_hotel_dto = MutateHotelDTO(
            hotel_id=params.hotel_id,
            name = params.name,
            description = params.description,
            tariff=params.tariff,
            image_urls = params.image_urls,
            destination_id = params.destination_id
        )

        try:
            hotel_dto = interactor.update_hotel(user_id=info.context.user.user_id,hotel_id=params.hotel_id, update_hotel_dto=update_hotel_dto)
        except InvalidAdminUser:
            return UserNotAuthorized(user_id=info.context.user.user_id)


        return Hotel(
                id = hotel_dto.id,
                name = hotel_dto.name,
                description = hotel_dto.description,
                image_urls = hotel_dto.image_urls,
                tariff = hotel_dto.tariff
            )
