import graphene

from trip.exceptions.custom_exceptions import InvalidAdminUser
from trip.interactors.add_hotel_interactor import AddHotelInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateHotelDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import InvalidUser
from trip_gql.hotel.types.types import Hotel, AddHotelResponse, AddHotelParams


class AddHotel(graphene.Mutation):
    class Arguments:
        params = AddHotelParams(required=True)

    Output = AddHotelResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = AddHotelInteractor(storage=storage)

        add_hotel_dto = MutateHotelDTO(
            name = params.name,
            description = params.description,
            tariff=params.tariff,
            image_urls = params.image_urls,
            destination_id = params.destination_id
        )

        try:
            hotel_dto = interactor.add_hotel(add_hotel_dto=add_hotel_dto)
        except InvalidAdminUser:
            return InvalidUser(user_id=info.context.user.id)


        return AddHotelResponse(
            Hotel(
                id = hotel_dto.id,
                name = hotel_dto.name,
                description = hotel_dto.description,
                total_amount = hotel_dto.total_amount,
                image_urls = hotel_dto.image_urls,
                tariff = hotel_dto.tariff
            )
        )