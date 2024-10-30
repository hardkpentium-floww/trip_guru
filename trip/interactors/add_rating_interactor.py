from trip.exceptions.custom_exceptions import InvalidUser, InvalidRating, InvalidDestination
from trip.interactors.storage_interfaces.storage_interface import StorageInterface, RatingDTO, MutateHotelDTO, \
    AddRatingDTO


class AddRatingInteractor:

    def __init__(self, storage: StorageInterface):
        self.storage = storage

    def add_rating(self,
                 add_rating_dto: AddRatingDTO
                 ) :

        check = self.storage.validate_destination_id(destination_id=add_rating_dto.destination_id)
        if not check:
            raise InvalidDestination

        check = self.storage.validate_hotel_customer(destination_id=add_rating_dto.destination_id,user_id=add_rating_dto.user_id)
        if not check:
            raise InvalidUser

        if add_rating_dto.rating <=0 or add_rating_dto.rating >5:
            raise InvalidRating

        rating_dto = self.storage.add_rating(
            add_rating_dto= add_rating_dto
        )

        return rating_dto
