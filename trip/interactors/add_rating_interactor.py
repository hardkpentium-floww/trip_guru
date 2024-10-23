from trip.interactors.storage_interfaces.storage_interface import StorageInterface, RatingDTO, MutateHotelDTO, \
    MutateRatingDTO


class AddRatingInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_rating(self,
                 add_rating_dto: MutateRatingDTO
                 ) :



        # self.storage.validate_hotel_customer(user_id=add_rating_dto.user_id)


        rating_dto = self.storage.add_rating(
            add_rating_dto= add_rating_dto
        )

        return rating_dto
