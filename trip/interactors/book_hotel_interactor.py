from trip.exceptions.custom_exceptions import InvalidAdminUser, BookingScheduleOverlap, InvalidDestination, \
    InvalidCheckinCheckoutDate
from trip.interactors.storage_interfaces.storage_interface import StorageInterface, BookingDTO, MutateHotelDTO, \
    MutateBookingDTO, AddBookingDTO


class BookHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def book_hotel(self, hotel_id: int,
                 book_hotel_dto: AddBookingDTO
                 ) :

        check = self.storage.validate_checkin_checkout_date(
            checkin_date=book_hotel_dto.checkin_date,
            checkout_date=book_hotel_dto.checkout_date)
        if not check:
            raise InvalidCheckinCheckoutDate

        check = self.storage.validate_destination_id(destination_id=book_hotel_dto.destination_id)
        if not check:
            raise InvalidDestination

        check = self.storage.check_overlapping_bookings(user_id=book_hotel_dto.user_id, checkin_date=book_hotel_dto.checkin_date, checkout_date=book_hotel_dto.checkout_date)
        if check:
            raise BookingScheduleOverlap

        hotel_dto = self.storage.book_hotel(
            hotel_id= hotel_id,
            book_hotel_dto= book_hotel_dto
        )

        return hotel_dto
