import graphene

from trip_gql.destination.types.types import InvalidUser


class Hotel(graphene.ObjectType):
    hotel_id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    total_amount = graphene.Int()
    image_urls = graphene.List(graphene.String)
    destination_id = graphene.Int()


class AddHotelParams(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    tariff = graphene.Int()
    image_urls = graphene.List(graphene.String)
    destination_id = graphene.Int()

class AddHotelResponse(graphene.Union):
    class Meta:
        types = (Hotel,InvalidUser)


class UpdateHotelParams(graphene.InputObjectType):
    hotel_id = graphene.String(required=True)
    name = graphene.String()
    description = graphene.String()
    total_amount = graphene.Int()
    image_urls = graphene.List(graphene.String)
    destination_id = graphene.Int()

class UpdateHotelResponse(graphene.Union):
    class Meta:
        types = (Hotel,InvalidUser)


class GetHotelParams(graphene.InputObjectType):
    hotel_id = graphene.String(required=True)

class GetHotelsParams(graphene.InputObjectType):
    destination_id = graphene.String(required=True)

class HotelNotFound(graphene.ObjectType):
    id = graphene.Int(graphene.Int)

class GetHotelResponse(graphene.ObjectType):
    class Meta:
        types = (Hotel,HotelNotFound)

class GetHotelsResponse(graphene.ObjectType):
    class Meta:
        types = (graphene.List(Hotel),HotelNotFound)

