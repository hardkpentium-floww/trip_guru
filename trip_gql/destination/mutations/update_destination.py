import graphene

from trip.exceptions.custom_exceptions import InvalidAdminUser, InvalidDestination
from trip.interactors.storage_interfaces.storage_interface import MutateDestinationDTO
from trip.interactors.update_destination_interactor import UpdateDestinationInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import Destination, InvalidUser,  \
    DestinationNotFound, UpdateDestinationResponse, UpdateDestinationParams


class UpdateDestination(graphene.Mutation):
    class Arguments:
        params = UpdateDestinationParams(required=True)

    Output = UpdateDestinationResponse

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = UpdateDestinationInteractor(storage=storage)

        update_destination_dto = MutateDestinationDTO(
            name = params.name,
            description = params.description,
            tags = params.tags,
            user_id = params.user_id
        )
        try:
            destination_dto = interactor.update_destination(destination_id=params.destination_id, update_destination_dto=update_destination_dto)
        except InvalidAdminUser:
            return InvalidUser(user_id=params.user_id)
        except InvalidDestination:
            return DestinationNotFound(restaurant_id=params.user_id)

        return UpdateDestinationResponse(
            Destination(
                destination_id = destination_dto.id,
                name = destination_dto.name,
                description = destination_dto.description,
                tags = destination_dto.tags,
                user_id = destination_dto.user_id
            )
        )