from trip.exceptions.custom_exceptions import InvalidTariff, InvalidAdminUser, InvalidHotel, InvalidDestination
from trip.interactors.storage_interfaces.storage_interface import HotelDTO, StorageInterface, MutateHotelDTO


class UpdateHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_hotel(self,
                     hotel_id: int,
                     user_id: str,
                    update_hotel_dto: MutateHotelDTO
                 ) :

        check = self.storage.check_duplicate_hotels(add_hotel_dtos=[update_hotel_dto])
        if check:
            raise InvalidHotel

        check = self.storage.validate_admin_user(user_id=user_id)
        if not check:
            raise InvalidAdminUser

        if update_hotel_dto.tariff <=0:
            raise InvalidTariff

        check = self.storage.validate_destination_id(destination_id=update_hotel_dto.destination_id)
        if not check:
            raise InvalidDestination

        hotel_dto = self.storage.update_hotel(
            hotel_id= hotel_id,
            update_hotel_dto= update_hotel_dto
        )

        return hotel_dto
