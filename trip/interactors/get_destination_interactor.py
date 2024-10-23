from trip.interactors.storage_interfaces.storage_interface import StorageInterface


class GetDestinationInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_destination(self,
                 destination_id: int
                 ) :



        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        destination_dto = self.storage.get_destination(
            destination_id= destination_id
        )

        return destination_dto
