from trip.interactors.storage_interfaces.storage_interface import HotelDTO, StorageInterface, MutateHotelDTO


class UpdateHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_hotel(self,
                     hotel_id: int,
                     user_id: str,
                    update_hotel_dto: MutateHotelDTO
                 ) :

        self.storage.check_duplicate_hotels(add_hotel_dtos=[update_hotel_dto])
        self.storage.validate_tariff(tariff=update_hotel_dto.tariff)
        self.storage.validate_admin_user(user_id=user_id)


        hotel_dto = self.storage.update_hotel(
            hotel_id= hotel_id,
            update_hotel_dto= update_hotel_dto
        )

        return hotel_dto
