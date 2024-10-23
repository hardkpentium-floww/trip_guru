from trip.exceptions.custom_exceptions import InvalidHotel, InvalidDestination
from trip.interactors.get_hotels_interactor import GetHotelsInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import DestinationNotFound
from trip_gql.hotel.types.types import GetHotelParams, HotelNotFound, Hotel, GetHotelResponse, GetHotelsParams, \
    GetHotelsResponse


def resolve_get_hotels(self, info):
    class Arguments:
        params = GetHotelsParams(required=True)

    storage = StorageImplementation()
    interactor = GetHotelsInteractor(storage=storage)

    try:
        hotel_dtos = interactor.get_hotels(destination_id=self.params.destination_id)
    except InvalidDestination:
        return DestinationNotFound(id=self.params.destination_id)

    return GetHotelsResponse(
        [Hotel(
            id=str(hotel_dto.id),
            name=hotel_dto.name,
            description=hotel_dto.description,
            tariff=hotel_dto.tariff,
            image_urls=hotel_dto.image_urls,
            destination_id=hotel_dto.destination_id
        )
        for hotel_dto in hotel_dtos]
    )