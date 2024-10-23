from trip.interactors.storage_interfaces.storage_interface import DestinationDTO, StorageInterface
from typing import List

class GetDestinationsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_destinations(self,
                 get_destinations_dto : List[DestinationDTO]
                 ) :



        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        destination_dtos = self.storage.get_destinations(
            get_destinations_dto = get_destinations_dto
        )

        return destination_dtos
