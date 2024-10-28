from trip.exceptions.custom_exceptions import InvalidTariff
from trip.interactors.storage_interfaces.storage_interface import HotelDTO, StorageInterface, MutateHotelDTO, \
    AddHotelDTO


class AddHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_hotel(self,
                  user_id: str,
                  add_hotel_dto: AddHotelDTO
                 ) :



        self.storage.validate_admin_user(user_id=user_id)
        self.storage.check_duplicate_hotels(add_hotel_dtos=[add_hotel_dto])

        check = add_hotel_dto.tariff >0
        if not check:
            raise InvalidTariff

        hotel_dto = self.storage.add_hotel(
            user_id=user_id,
            add_hotel_dto= add_hotel_dto
        )

        return hotel_dto
