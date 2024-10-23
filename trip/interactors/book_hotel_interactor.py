from trip.interactors.storage_interfaces.storage_interface import StorageInterface, BookingDTO


class BookHotelInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def book_hotel(self,
                 book_hotel_dto: BookingDTO
                 ) :



        # self.storage.validate_admin_user(user_id=add_hotel_dto.user_id)


        hotel_dto = self.storage.book_hotel(
            book_hotel_dto= book_hotel_dto
        )

        return hotel_dto
