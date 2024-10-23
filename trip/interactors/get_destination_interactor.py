from trip.interactors.storage_interfaces.storage_interface import StorageInterface


class GetDestinationInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_destination(self,
                 destination_name: str
                 ) :



        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        destination_dto = self.storage.get_destination(
            destination_name= destination_name
        )

        return destination_dto
