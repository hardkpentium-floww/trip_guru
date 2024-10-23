from trip.interactors.storage_interfaces.storage_interface import StorageInterface, BookingDTO, MutateHotelDTO, \
    MutateBookingDTO


class BookHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def book_hotel(self, hotel_id: int,
                 book_hotel_dto: MutateBookingDTO
                 ) :



        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        hotel_dto = self.storage.book_hotel(
            hotel_id= hotel_id,
            book_hotel_dto= book_hotel_dto
        )

        return hotel_dto
