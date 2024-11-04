from trip.exceptions.custom_exceptions import InvalidHotel
from trip.interactors.get_hotel_interactor import GetHotelInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.hotel.types.types import GetHotelParams, HotelNotFound, Hotel, GetHotelResponse


def resolve_get_hotel(root, info,params):

    storage = StorageImplementation()
    interactor = GetHotelInteractor(storage=storage)


    try:
        hotel_dto = interactor.get_hotel(hotel_id=params.hotel_id)
    except InvalidHotel:
        return HotelNotFound(id=params.hotel_id)

    return Hotel(
            id=hotel_dto.id,
            name=hotel_dto.name,
            description=hotel_dto.description,
            tariff=hotel_dto.tariff,
            image_urls=hotel_dto.image_urls,
            destination_id=hotel_dto.destination_id
        )
