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
from trip_gql.hotel.resolvers.get_hotels_for_destination import resolve_get_hotels_for_destination
from trip_gql.hotel.types.types import GetHotelResponse, GetHotelParams, GetHotelsResponse, GetHotelsParams
from trip_gql.rating.mutations.add_rating import AddRating
from graphql_service.utils.logger import log_error
from graphql_service.middlewares import middlewares
from graphql_service import context
from typing import Dict, Sequence
from graphql.error import GraphQLError


class Query(graphene.ObjectType):
    get_hotel = graphene.Field(
        GetHotelResponse,
        params=GetHotelParams(required=True),
        resolver=resolve_get_hotel
    )

    get_hotels_for_destination = graphene.Field(
        GetHotelsResponse,
        params=GetHotelsParams(required=True),
        resolver=resolve_get_hotels_for_destination
    )

    get_destination = graphene.Field(
        GetDestinationResponse,
        params=GetDestinationParams(required=True),
        resolver=resolve_get_destination
    )

    get_destinations = graphene.Field(
        GetDestinationsResponse,
        params=GetDestinationsParams(required=True),
        resolver=resolve_get_destinations
    )

    get_bookings_for_user = graphene.Field(
        GetBookingsForUserResponse,
        params=GetBookingsForUserParams(required=True),
        resolver=resolve_get_bookings_for_user
    )


class Mutation(graphene.ObjectType):
    add_destination = AddDestination.Field(required=True)
    add_hotel = AddHotel.Field(required=True)
    add_rating = AddRating.Field(required=True)
    book_hotel = BookHotel.Field(required=True)
    update_booking = UpdateBooking.Field(required=True)
    update_destination = UpdateDestination.Field(required=True)
    update_hotel = UpdateHotel.Field(required=True)


schema = graphene.Schema(query=Query, mutation=Mutation)


def execute_graphql_as_sync(query, variables, middleware, context_obj):
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(
        schema.execute_async(
            query,
            variables=variables,
            middleware=middleware,
            context=context_obj,
        )
    )
    loop.close()
    return result


def handle_graphql_errors(errors: Sequence[GraphQLError], operation_name):
    if errors is None:
        return
    try:
        for error in errors:
            _ = log_error(error=error, logger_name=operation_name)
    except Exception:
        pass


def execute_schema(query, variables, user_id):
    result = execute_graphql_as_sync(
        query=query,
        variables=variables,
        middleware=middlewares,
        context_obj=context.get_context(user_id),
    )
    handle_graphql_errors(result.errors, operation_name="Graphene Error")
    return result
