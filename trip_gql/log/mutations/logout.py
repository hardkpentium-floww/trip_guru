import graphene

from trip.interactors.logout_interactor import LogoutInteractor
from trip.interactors.storage_interfaces.storage_interface import StorageInterface
from trip_gql.destination.types.types import Destination, AddDestinationParams, InvalidUser, AddDestinationResponse
from trip_gql.log.types.types import LogoutParams, LogoutResponse, LoggedOutUser
from trip_gql.rating.types.types import UserNotFound


class Logout(graphene.Mutation):
    class Arguments:
        params = LogoutParams(required=True)

    Output = LogoutResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageInterface()
        interactor = LogoutInteractor(storage=storage)

        try:
            logout_dto = interactor.logout(phone_no = params.phone_no, password = params.password)
        except InvalidUser:
            return UserNotFound(user_id=params.user_id)


        return LogoutResponse(
                LoggedOutUser(
                    user_id=logout_dto.user_id

                )
            )
