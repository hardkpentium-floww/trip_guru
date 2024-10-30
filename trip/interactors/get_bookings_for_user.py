from trip.exceptions.custom_exceptions import NoBookingsExists
from trip.interactors.storage_interfaces.storage_interface import StorageInterface


class GetBookingsForUserInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_bookings_for_user(self,
                 user_id: str,
                 offset: int,
                 limit: int
                 ) :


        check = self.storage.validate_booking_for_user(user_id=user_id)
        if not check:
            raise NoBookingsExists

        destination_dto = self.storage.get_bookings_for_user(
            user_id= user_id,
            offset= offset,
            limit= limit
        )

        return destination_dto
