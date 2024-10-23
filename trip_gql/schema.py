import graphene

from setup import required
from trip.interactors.get_hotels_interactor import GetHotelsInteractor
from trip.interactors.storage_interfaces.storage_interface import GetDestinationsDTO
from trip_gql.destination.resolvers.get_destination import resolve_get_destination
from trip_gql.destination.resolvers.get_destinations import resolve_get_destinations
from trip_gql.destination.types.types import GetDestinationsResponse, GetDestinationsParams
from trip_gql.hotel.resolvers.get_hotel import resolve_get_hotel
from trip_gql.hotel.resolvers.get_hotels import resolve_get_hotels
from trip_gql.hotel.types.types import GetHotelResponse, GetHotelParams, GetHotelsResponse, GetHotelsParams


class Query(graphene.ObjectType):

    get_hotel = graphene.Field(
        GetHotelResponse,
        params = GetHotelParams(required=True),
        resolver=resolve_get_hotel
    )

    get_hotels_for_destination = graphene.Field(
        GetHotelsResponse,
        params=GetHotelsParams,
        resolver=resolve_get_hotels()
    )

    get_destination = graphene.Field(
        GetDestinationsResponse,
        params = GetDestinationsParams(required=True),
        resolver=resolve_get_destination
    )

    get_destinations = graphene.Field(
        GetDestinationsResponse,
        params = GetDestinationsParams,
        resolver=resolve_get_destinations
    )


class Mutation(graphene.ObjectType):
    add_destination = AddDestination.Field(required=True)
    add_hotel =AddHotel.Field(required=True)
    add_rating = AddRating.Field(required=True)
    book_hotel = BookHotel.Field(required=True)
    update_booking = UpdateBooking.Field(required=True)
    update_destination = UpdateDestination.Field(required=True)
    update_hotel = UpdateHotel.Field(required=True)


schema = graphene.Schema(query=Query, mutation=Mutation)
