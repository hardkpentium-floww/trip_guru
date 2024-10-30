from trip.exceptions.custom_exceptions import InvalidTariff, InvalidAdminUser, InvalidDestination, InvalidHotel
from trip.interactors.storage_interfaces.storage_interface import HotelDTO, StorageInterface, MutateHotelDTO, \
    AddHotelDTO


class AddHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_hotel(self,
                  user_id: str,
                  add_hotel_dto: AddHotelDTO
                 ) :

        check = self.storage.validate_admin_user(user_id=user_id)

        if not check:
            raise InvalidAdminUser

        check = self.storage.check_duplicate_hotels(add_hotel_dtos=[add_hotel_dto])
        if check:
            raise InvalidHotel

        check = self.storage.validate_destination_id(destination_id=add_hotel_dto.destination_id)
        if not check:
            raise InvalidDestination

        check = add_hotel_dto.tariff >0
        if not check:
            raise InvalidTariff

        hotel_dto = self.storage.add_hotel(
            user_id=user_id,
            add_hotel_dto= add_hotel_dto
        )

        return hotel_dto
