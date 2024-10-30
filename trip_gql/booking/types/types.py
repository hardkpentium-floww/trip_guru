import graphene

from trip_gql.common_errors import BookingNotPossible, BookingsNotFound, DestinationNotFound


class Booking(graphene.ObjectType):
    id = graphene.Int()
    user_id = graphene.String()
    destination_id = graphene.Int()
    hotel_id = graphene.Int()
    checkin_date = graphene.DateTime()
    checkout_date = graphene.DateTime()
    tariff = graphene.Int()
    total_amount = graphene.Int()


class UpdateBookingParams(graphene.InputObjectType):
    booking_id = graphene.Int()
    checkin_date = graphene.DateTime()
    checkout_date = graphene.DateTime()
    total_amount = graphene.Int()


class Bookings(graphene.ObjectType):
    bookings = graphene.List(Booking)


class BookingDateNotValid(graphene.ObjectType):
    checkin_date = graphene.DateTime()
    checkout_date = graphene.DateTime()


class UserNotFound(graphene.ObjectType):
    user_id = graphene.String()


class GetBookingsForUserResponse(graphene.Union):
    class Meta:
        types = (Bookings, BookingsNotFound)


class GetBookingsForUserParams(graphene.InputObjectType):
    user_id = graphene.String()
    offset = graphene.Int()
    limit = graphene.Int()


class UpdateBookingResponse(graphene.Union):
    class Meta:
        types = (Booking, BookingNotPossible)


class BookHotelResponse(graphene.Union):
    class Meta:
        types = (Booking, BookingNotPossible, BookingDateNotValid, DestinationNotFound)


class BookHotelParams(graphene.InputObjectType):
    user_id = graphene.String()
    checkin_date = graphene.DateTime()
    checkout_date = graphene.DateTime()
    hotel_id = graphene.Int()
    destination_id = graphene.Int()
