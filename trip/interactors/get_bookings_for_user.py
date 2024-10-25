from trip.interactors.storage_interfaces.storage_interface import StorageInterface


class GetBookingsForUserInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def get_bookings_for_user(self,
                 user_id: str,
                 offset: int,
                 limit: int
                 ) :



        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        destination_dto = self.storage.get_bookings_for_user(
            user_id= user_id,
            offset= offset,
            limit= limit
        )

        return destination_dto
