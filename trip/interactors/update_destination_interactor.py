from trip.interactors.storage_interfaces.storage_interface import StorageInterface, DestinationDTO


class UpdateDestinationInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_destination(self,
                 update_destination_dto: DestinationDTO
                 ) :



        self.storage.validate_admin_user(user_id=update_destination_dto.user_id)


        destination_dto = self.storage.update_destination(
            update_destination_dto= update_destination_dto
        )

        return destination_dto
