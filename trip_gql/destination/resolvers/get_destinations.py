from trip.exceptions.custom_exceptions import InvalidHotel, InvalidDestination
from trip.interactors.get_destinations_interactor import GetDestinationsInteractor
from trip.interactors.storage_interfaces.storage_interface import GetDestinationsDTO
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import GetDestinationsParams, GetDestinationsResponse, DestinationNotFound, \
    Destination, Destinations


def resolve_get_destinations(self, info,params):

    storage = StorageImplementation()
    interactor = GetDestinationsInteractor(storage=storage)

    get_destinations_dto = GetDestinationsDTO(
        tag = params.tag,
        offset = params.offset,
        limit = params.limit
    )


    try:
        destination_dtos = interactor.get_destinations(get_destinations_dto=get_destinations_dto)
    except InvalidDestination:
        return DestinationNotFound(destination_id=params.destination_id)

    return Destinations(destinations= [Destination(
            id=destination_dto.id,
            name=destination_dto.name,
            description=destination_dto.description,
            tags=destination_dto.tags,
            user_id=destination_dto.user_id
        )
        for destination_dto in destination_dtos])
