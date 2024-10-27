from trip.interactors.storage_interfaces.storage_interface import StorageInterface, DestinationDTO, MutateHotelDTO, \
    MutateDestinationDTO


class AddDestinationInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_destination(self, add_destination_dto: MutateDestinationDTO):
        self.storage.validate_admin_user(user_id=add_destination_dto.user_id)
        destination_dto = self.storage.add_destination(
            add_destination_dto= add_destination_dto
        )
        return destination_dto
