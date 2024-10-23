import graphene

from trip.exceptions.custom_exceptions import InvalidAdminUser
from trip.interactors.add_rating_interactor import AddRatingInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateHotelDTO, MutateRatingDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import InvalidUser
from trip_gql.rating.types.types import AddRatingResponse, AddRatingParams, Rating, UserNotFound


class AddRating(graphene.Mutation):
    class Arguments:
        params = AddRatingParams(required=True)

    Output = AddRatingResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = AddRatingInteractor(storage=storage)

        add_rating_dto = MutateRatingDTO(
            rating=params.rating,
            review=params.review,
            destination_id=params.destination_id,
            user_id=info.context.user.id
        )

        try:
            rating_dto = interactor.add_rating(add_rating_dto=add_rating_dto)
        except InvalidUser:
            return UserNotFound(user_id=info.context.user.id)


        return AddRatingResponse(
            Rating(
                rating_id= rating_dto.id,
                rating=rating_dto.rating,
                review=rating_dto.review,
                destination_id=rating_dto.destination_id,
                user_id=rating_dto.user_id
            )
        )