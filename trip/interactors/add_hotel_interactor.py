from trip.interactors.storage_interfaces.storage_interface import HotelDTO, StorageInterface, MutateHotelDTO


class AddHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_hotel(self,
                 add_hotel_dto: MutateHotelDTO
                 ) :



        self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        hotel_dto = self.storage.add_hotel(
            add_hotel_dto= add_hotel_dto
        )

        return hotel_dto
