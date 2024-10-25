import graphene

from trip_gql.common_errors import BookingNotPossible, BookingsNotFound


class Booking(graphene.ObjectType):
    id = graphene.Int()
    user_id = graphene.String()
    destination_id = graphene.Int()
    hotel_id = graphene.Int()
    checkin_date = graphene.String()
    checkout_date = graphene.String()
    tariff = graphene.Int()
    total_amount = graphene.Int()

class UpdateBookingParams(graphene.InputObjectType):
    booking_id = graphene.Int()
    checkin_date = graphene.String()
    checkout_date = graphene.String()
    total_amount = graphene.Int()

class Bookings(graphene.ObjectType):
    bookings = graphene.List(Booking)


class UserNotFound(graphene.ObjectType):
    user_id = graphene.String()

class GetBookingsForUserResponse(graphene.Union):
    class Meta:
        types = (Bookings,BookingsNotFound)

class GetBookingsForUserParams(graphene.InputObjectType):
    user_id = graphene.String()
    offset = graphene.Int()
    limit = graphene.Int()


class UpdateBookingResponse(graphene.Union):
    class Meta:
        types = (Booking,BookingNotPossible)

class BookHotelResponse(graphene.Union):
    class Meta:
        types = (Booking,BookingNotPossible)


class BookHotelParams(graphene.InputObjectType):
    user_id = graphene.String()
    checkin_date = graphene.String()
    checkout_date = graphene.String()
    hotel_id = graphene.Int()
    destination_id = graphene.Int()
    tariff = graphene.Int()
