from trip.interactors.storage_interfaces.storage_interface import StorageInterface, UpdateBookingDTO, MutateBookingDTO


class UpdateBookingInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_booking(self,
                 update_booking_dto: MutateBookingDTO
                 ) :



        # self.storage.validate_admin_user(user_id=update_destination_dto.user_id)


        booking_dto = self.storage.update_booking(
            booking_id= update_booking_dto.booking_id,
            update_booking_dto= update_booking_dto
        )

        return booking_dto
