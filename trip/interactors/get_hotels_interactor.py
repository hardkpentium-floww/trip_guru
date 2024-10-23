from trip.interactors.storage_interfaces.storage_interface import StorageInterface


class GetHotelsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_hotels(self,
                 destination_id: int
                 ) :



        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        hotel_dtos = self.storage.get_hotels(
            destination_id=destination_id
        )

        return hotel_dtos
