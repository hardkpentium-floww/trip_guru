import graphene

class UserNotAuthorized(graphene.ObjectType):
    user_id = graphene.String()


class DestinationNotFound(graphene.ObjectType):
    destination_id = graphene.Int()


class UserNotAdmin(graphene.ObjectType):
    user_id = graphene.String()


class HotelNotFound(graphene.ObjectType):
    id = graphene.Int()


class BookingNotPossible(graphene.ObjectType):
    hotel_id = graphene.Int()


class BookingsNotFound(graphene.ObjectType):
    user_id = graphene.String()

