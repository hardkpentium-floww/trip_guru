from trip.exceptions.custom_exceptions import InvalidHotel, InvalidDestination
from trip.interactors.get_destinations_interactor import GetDestinationsInteractor
from trip.storages.storage_implementation import StorageImplementation
from trip_gql.destination.types.types import GetDestinationsParams, GetDestinationsResponse, DestinationNotFound, \
    Destination


def resolve_get_destinations(self, info):
    class Arguments:
        params = GetDestinationsParams(required=True)

    storage = StorageImplementation()
    interactor = GetDestinationsInteractor(storage=storage)

    try:
        hotel_dtos = interactor.get_destinations(destination_id=self.params.id)
    except InvalidDestination:
        return DestinationNotFound(id=self.params.id)

    return GetDestinationsResponse(
        [Destination(
            id=hotel_dto.id,
            name=hotel_dto.name,
            description=hotel_dto.description,
            tags=hotel_dto.tags,
            user_id=hotel_dto.user_id
        )
        for hotel_dto in hotel_dtos]
    )