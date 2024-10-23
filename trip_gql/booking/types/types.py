import graphene


class Booking(graphene.ObjectType):
    id = graphene.Int()
    user_id = graphene.String()
    destination_id = graphene.Int()
    hotel_id = graphene.Int()
    checkin_date = graphene.String()
    checkout_date = graphene.String()
    total_amount = graphene.Int()


class BookingNotPossible(graphene.ObjectType):
    hotel_id = graphene.Int()

class BookHotelResponse(graphene.ObjectType):
    class Meta:
        types = (Booking,BookingNotPossible)


class BookHotelParams(graphene.ObjectType):
    user_id = graphene.String()
    checkin_date = graphene.String()
    checkout_date = graphene.String()
    hotel_id = graphene.Int()
    destination_id = graphene.Int()
    total_amount = graphene.Int()