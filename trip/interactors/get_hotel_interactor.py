from trip.exceptions.custom_exceptions import InvalidHotel
from trip.interactors.storage_interfaces.storage_interface import StorageInterface


class GetHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_hotel(self,
                 hotel_id: int
                 ) :

        check = self.storage.validate_hotel_id(hotel_id=hotel_id)

        if not check:
            raise InvalidHotel

        hotel_dto = self.storage.get_hotel(
            hotel_id= hotel_id
        )

        return hotel_dto
