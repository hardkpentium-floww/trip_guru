import graphene

from trip.exceptions.custom_exceptions import InvalidAdminUser
from trip.interactors.add_destination_interactor import AddDestinationInteractor
from trip.interactors.storage_interfaces.storage_interface import MutateDestinationDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import Destination, AddDestinationParams, InvalidUser, AddDestinationResponse


class AddDestination(graphene.Mutation):
    class Arguments:
        params = AddDestinationParams(required=True)

    Output = AddDestinationInteractor

    @staticmethod
    def mutate(root, info, params):
        storage = StorageImplementation()
        interactor = AddDestinationInteractor(storage=storage)

        add_destination_dto = MutateDestinationDTO(
            name = params.name,
            description = params.description,
            tags = params.tags,
            user_id = params.user_id
        )
        try:
            destination_dto = interactor.add_destination(add_destination_dto=add_destination_dto)
        except InvalidAdminUser:
            return InvalidUser(user_id=params.user_id)


        return AddDestinationResponse(
            Destination(
                destination_id = destination_dto.id,
                name = destination_dto.name,
                description = destination_dto.description,
                tags = destination_dto.tags,
                user_id = destination_dto.user_id
            )
        )