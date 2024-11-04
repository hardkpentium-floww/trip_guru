from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidDestination, InvalidHotel
from trip.interactors.storage_interfaces.storage_interface import HotelDTO, StorageInterface, MutateHotelDTO, \
    AddHotelDTO
from typing import List

class AddHotelsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_hotels(self,
                  user_id: str,
                  add_hotel_dtos:  List[AddHotelDTO],
                  destination_id: int
                 ) :



        check = self.storage.validate_admin_user(user_id=user_id)
        if not check:
            raise InvalidAdminUser

        check = self.storage.validate_destination_id(destination_id=destination_id)
        if not check:
            raise InvalidDestination

        check = self.storage.check_duplicate_hotels(add_hotel_dtos=add_hotel_dtos)
        if check:
            raise InvalidHotel

        hotel_dtos = self.storage.add_hotels(
            user_id=user_id,
            add_hotel_dtos= add_hotel_dtos,
            destination_id=destination_id
        )

        return hotel_dtos
