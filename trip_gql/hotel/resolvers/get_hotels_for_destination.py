from trip.exceptions.custom_exceptions import InvalidHotel, InvalidDestination
from trip.interactors.get_hotels_interactor import GetHotelsInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import DestinationNotFound
from trip_gql.hotel.types.types import Hotel, Hotels


def resolve_get_hotels_for_destination(self, info,params):

    storage = StorageImplementation()
    interactor = GetHotelsInteractor(storage=storage)

    try:
        hotel_dtos = interactor.get_hotels(destination_ids=[params.destination_id])
    except InvalidDestination:
        return DestinationNotFound(destination_id=params.destination_id)

    hotel_list = [Hotel(
        id=hotel_dto.id,
        name=hotel_dto.name,
        description=hotel_dto.description,
        tariff=hotel_dto.tariff,
        image_urls=hotel_dto.image_urls,
        destination_id=hotel_dto.destination_id
    )
        for hotel_dto in hotel_dtos]


    return Hotels(hotels=hotel_list)