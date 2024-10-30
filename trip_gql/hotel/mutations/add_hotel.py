import graphene

from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidDestination, InvalidTariff
from trip.interactors.add_hotel_interactor import AddHotelInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateHotelDTO, AddHotelDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import DestinationNotFound
from trip_gql.hotel.types.types import Hotel, AddHotelResponse, AddHotelParams, UserNotAuthorized, TariffNotValid


class AddHotel(graphene.Mutation):
    class Arguments:
        params = AddHotelParams(required=True)

    Output = AddHotelResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = AddHotelInteractor(storage=storage)

        add_hotel_dto = AddHotelDTO(
            name = params.name,
            description = params.description,
            tariff=params.tariff,
            image_urls = params.image_urls,
            destination_id = params.destination_id
        )

        try:
            hotel_dto = interactor.add_hotel(user_id=info.context.user_id, add_hotel_dto=add_hotel_dto)
        except InvalidAdminUser:
            return UserNotAuthorized(user_id=info.context.user_id)
        except InvalidDestination:
            return DestinationNotFound(destination_id=params.destination_id)
        except InvalidTariff:
            return TariffNotValid(tariff=params.tariff)


        return Hotel(
                id = hotel_dto.id,
                name = hotel_dto.name,
                description = hotel_dto.description,
                image_urls = hotel_dto.image_urls,
                tariff = hotel_dto.tariff,
                destination_id = hotel_dto.destination_id
            )
