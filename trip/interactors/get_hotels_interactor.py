from trip.interactors.storage_interfaces.storage_interface import StorageInterface
from typing import List

class GetHotelsInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_hotels(self,
                 destination_ids: List[int]
                 ) :


        hotel_dtos = self.storage.get_hotels(
            destination_ids=destination_ids
        )

        return hotel_dtos
