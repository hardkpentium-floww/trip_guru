import graphene

from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidUser
from trip.interactors.add_destination_interactor import AddDestinationInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateDestinationDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.common_errors import UserNotAdmin
from trip_gql.destination.types.types import Destination, AddDestinationParams, AddDestinationResponse


class AddDestination(graphene.Mutation):
    class Arguments:
        params = AddDestinationParams(required=True)

    Output = AddDestinationResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = AddDestinationInteractor(storage=storage)

        add_destination_dto = MutateDestinationDTO(
            name = params.name,
            description = params.description,
            tags = params.tags,
            user_id = info.context.user.user_id
        )
        try:
            destination_dto = interactor.add_destination(add_destination_dto=add_destination_dto)
        except InvalidAdminUser:
            return UserNotAdmin(user_id= info.context.user.user_id)


        return  Destination(
                id = destination_dto.id,
                name = destination_dto.name,
                description = destination_dto.description,
                tags = destination_dto.tags,
                user_id = destination_dto.user_id
            )
