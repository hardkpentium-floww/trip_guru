from trip.exceptions.custom_exceptions import InvalidHotel, InvalidDestination
from trip.interactors.get_destination_interactor import GetDestinationInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import GetDestinationsParams, GetDestinationsResponse, DestinationNotFound, \
    Destination, GetDestinationParams, GetDestinationResponse


def resolve_get_destination(self, info):
    class Arguments:
        params = GetDestinationParams(required=True)

    storage = StorageImplementation()
    interactor = GetDestinationInteractor(storage=storage)

    try:
        hotel_dto = interactor.get_destination(destination_id=self.params.id)
    except InvalidDestination:
        return DestinationNotFound(id=self.params.id)

    return GetDestinationResponse(
        Destination(
            id = hotel_dto.id,
            name = hotel_dto.name,
            description = hotel_dto.description,
            tags = hotel_dto.tags,
            user_id= hotel_dto.user_id
        )
    )