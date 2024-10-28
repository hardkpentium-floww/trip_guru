from trip.interactors.storage_interfaces.storage_interface import StorageInterface, RatingDTO, MutateHotelDTO, \
    AddRatingDTO


class AddRatingInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_rating(self,
                 add_rating_dto: AddRatingDTO
                 ) :



        self.storage.validate_hotel_customer(destination_id=add_rating_dto.destination_id,user_id=add_rating_dto.user_id)
        self.storage.validate_rating(rating=add_rating_dto.rating)

        rating_dto = self.storage.add_rating(
            add_rating_dto= add_rating_dto
        )

        return rating_dto
