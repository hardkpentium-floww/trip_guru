import graphene

from trip_gql.common_errors import UserNotAuthorized, DestinationNotFound, HotelNotFound


class Hotel(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    image_urls = graphene.String()
    destination_id = graphene.Int()
    tariff = graphene.Int()


class AddHotelParams(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    tariff = graphene.Int()
    image_urls = graphene.String()
    destination_id = graphene.Int()



class AddHotelResponse(graphene.Union):
    class Meta:
        types = (Hotel,UserNotAuthorized, DestinationNotFound,)

class UpdateHotelParams(graphene.InputObjectType):
    hotel_id = graphene.Int(required=True)
    name = graphene.String()
    description = graphene.String()
    total_amount = graphene.Int()
    image_urls = graphene.String()
    destination_id = graphene.Int()
    tariff = graphene.Int()

class UpdateHotelResponse(graphene.Union):
    class Meta:
        types = (Hotel,UserNotAuthorized)


class GetHotelParams(graphene.InputObjectType):
    hotel_id = graphene.Int(required=True)

class GetHotelsParams(graphene.InputObjectType):
    destination_id = graphene.Int(required=True)


class GetHotelResponse(graphene.Union):
    class Meta:
        types = (Hotel,HotelNotFound)

class Hotels(graphene.ObjectType):
    hotels = graphene.List(Hotel)

class GetHotelsResponse(graphene.Union):
    class Meta:
        types = (Hotels,DestinationNotFound)

