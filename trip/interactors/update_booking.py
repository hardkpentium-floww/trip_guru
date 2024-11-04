from trip.exceptions.custom_exceptions import BookingScheduleOverlap
from trip.interactors.storage_interfaces.storage_interface import StorageInterface, MutateBookingDTO


class UpdateBookingInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def update_booking(self,
                 update_booking_dto: MutateBookingDTO
                 ) :

        check = self.storage.check_overlapping_bookings(
            user_id=update_booking_dto.user_id,
            checkin_date=update_booking_dto.checkin_date,
            checkout_date=update_booking_dto.checkout_date)

        if check:
            raise BookingScheduleOverlap

        booking_dto = self.storage.update_booking(
            booking_id= update_booking_dto.booking_id,
            update_booking_dto= update_booking_dto
        )

        return booking_dto
