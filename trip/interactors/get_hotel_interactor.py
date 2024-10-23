from trip.interactors.storage_interfaces.storage_interface import StorageInterface


class GetHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_hotel(self,
                 hotel_id: int
                 ) :


        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        hotel_dto = self.storage.get_hotel(
            hotel_id= hotel_id
        )

        return hotel_dto
