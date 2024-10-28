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



        self.storage.validate_admin_user(user_id=user_id)
        self.storage.validate_destination_id(destination_id=destination_id)
        self.storage.check_duplicate_hotels(add_hotel_dtos=add_hotel_dtos)

        hotel_dtos = self.storage.add_hotels(
            user_id=user_id,
            add_hotel_dtos= add_hotel_dtos,
            destination_id=destination_id
        )

        return hotel_dtos
