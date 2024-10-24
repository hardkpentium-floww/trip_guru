
from typing import List

from trip.storages.storage_implementation import StorageImplementation


class LogoutInteractor:

    def __init__(self, storage: StorageImplementation):
        self.storage = storage


    def logout(self,
                 user_id: int,
                 ) :

        self.storage.logout(
            user_id= user_id
        )
