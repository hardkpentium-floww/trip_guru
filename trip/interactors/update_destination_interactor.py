from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidDestination
from trip.interactors.storage_interfaces.storage_interface import StorageInterface, DestinationDTO, MutateDestinationDTO


class UpdateDestinationInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_destination(self,
                destination_id: int,
                 update_destination_dto: MutateDestinationDTO
                 ) :

        check = self.storage.validate_admin_user(user_id=update_destination_dto.user_id)

        if not check:
            raise InvalidAdminUser

        check = self.storage.check_duplicate_destination(add_destination_dto=update_destination_dto)
        if check:
            raise InvalidDestination



        destination_dto = self.storage.update_destination(
            destination_id=destination_id,
            update_destination_dto= update_destination_dto
        )

        return destination_dto
