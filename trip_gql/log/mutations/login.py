import graphene

from trip.interactors.login_interactor import LoginInteractor
from trip.interactors.storage_interfaces.storage_interface import StorageInterface
from trip_gql.destination.types.types import Destination, AddDestinationParams, InvalidUser, AddDestinationResponse
from trip_gql.log.types.types import LoginParams, LoginResponse, AuthenticationResponse
from trip_gql.rating.types.types import UserNotFound


class Login(graphene.Mutation):
    class Arguments:
        params = LoginParams(required=True)

    Output = LoginResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageInterface()
        interactor = LoginInteractor(storage=storage)

        try:
            authentication_response_dto = interactor.login(phone_no = params.phone_no, password = params.password)
        except InvalidUser:
            return UserNotFound(user_id=params.user_id)


        return LoginResponse(
            AuthenticationResponse(
                destination_id = authentication_response_dto.id,
                name = authentication_response_dto.name,
                description = authentication_response_dto.description,
                tags = authentication_response_dto.tags,
                user_id = authentication_response_dto.user_id
            )
        )