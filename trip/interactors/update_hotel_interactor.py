from trip.interactors.storage_interfaces.storage_interface import HotelDTO, StorageInterface


class UpdateHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_hotel(self,
                 update_hotel_dto: HotelDTO
                 ) :



        self.storage.validate_admin_user(user_id=update_hotel_dto.user_id)


        hotel_dto = self.storage.update_hotel(
            update_hotel_dto= update_hotel_dto
        )

        return hotel_dto
