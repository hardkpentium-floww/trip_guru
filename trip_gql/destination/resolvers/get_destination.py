from trip.exceptions.custom_exceptions import InvalidHotel, InvalidDestination
from trip.interactors.get_destination_interactor import GetDestinationInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import GetDestinationsParams, GetDestinationsResponse, DestinationNotFound, \
    Destination, GetDestinationParams, GetDestinationResponse


def resolve_get_destination(root, info, params):
    storage = StorageImplementation()
    interactor = GetDestinationInteractor(storage=storage)

    try:
        destination_dto = interactor.get_destination(destination_id=params.destination_id)
    except InvalidDestination:
        return DestinationNotFound(destination_id=params.destination_id)

    return Destination(
            id = destination_dto.id,
            name = destination_dto.name,
            description = destination_dto.description,
            tags = destination_dto.tags,
            user_id= destination_dto.user_id
        )
