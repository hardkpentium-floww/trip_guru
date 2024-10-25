import graphene

from trip_gql.booking.mutations.book_hotel import BookHotel
from trip_gql.booking.mutations.update_booking import UpdateBooking
from trip_gql.booking.resolvers.get_bookings_for_user import resolve_get_bookings_for_user
from trip_gql.booking.types.types import GetBookingsForUserResponse, GetBookingsForUserParams
from trip_gql.destination.mutations.add_destination import AddDestination
from trip_gql.destination.mutations.update_destination import UpdateDestination
from trip_gql.destination.resolvers.get_destination import resolve_get_destination
from trip_gql.destination.resolvers.get_destinations import resolve_get_destinations
from trip_gql.destination.types.types import GetDestinationsResponse, GetDestinationsParams, GetDestinationParams, \
    GetDestinationResponse
from trip_gql.hotel.mutations.add_hotel import AddHotel
from trip_gql.hotel.mutations.update_hotel import UpdateHotel
from trip_gql.hotel.resolvers.get_hotel import resolve_get_hotel
from trip_gql.hotel.resolvers.get_hotels_for_destination import  resolve_get_hotels_for_destination
from trip_gql.hotel.types.types import GetHotelResponse, GetHotelParams, GetHotelsResponse, GetHotelsParams
from trip_gql.rating.mutations.add_rating import AddRating


class Query(graphene.ObjectType):

    get_hotel = graphene.Field(
        GetHotelResponse,
        params = GetHotelParams(required=True),
        resolver=resolve_get_hotel
    )

    get_hotels_for_destination = graphene.Field(
        GetHotelsResponse,
        params=GetHotelsParams(required=True),
        resolver=resolve_get_hotels_for_destination
    )

    get_destination = graphene.Field(
        GetDestinationResponse,
        params = GetDestinationParams(required=True),
        resolver=resolve_get_destination
    )

    get_destinations = graphene.Field(
        GetDestinationsResponse,
        params = GetDestinationsParams(required=True),
        resolver=resolve_get_destinations
    )

    get_bookings_for_user = graphene.Field(
        GetBookingsForUserResponse,
        params = GetBookingsForUserParams(required=True),
        resolver=resolve_get_bookings_for_user
    )



class Mutation(graphene.ObjectType):
    add_destination = AddDestination.Field(required=True)
    add_hotel =AddHotel.Field(required=True)
    add_rating = AddRating.Field(required=True)
    book_hotel = BookHotel.Field(required=True)
    update_booking = UpdateBooking.Field(required=True)
    update_destination = UpdateDestination.Field(required=True)
    update_hotel = UpdateHotel.Field(required=True)
    # login = Login.Field(required=True)
    # logout = Logout.Field(required=True)

schema = graphene.Schema(query=Query, mutation=Mutation)
