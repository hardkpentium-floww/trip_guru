import graphene

from trip_gql.common_errors import UserNotAuthorized, DestinationNotFound, HotelNotFound, UserNotAdmin


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

class TariffNotValid(graphene.ObjectType):
    tariff = graphene.Int()


class AddHotelResponse(graphene.Union):
    class Meta:
        types = (Hotel,UserNotAuthorized, TariffNotValid, DestinationNotFound,)

class UpdateHotelParams(graphene.InputObjectType):
    hotel_id = graphene.Int(required=True)
    name = graphene.String()
    description = graphene.String()
    image_urls = graphene.String()
    destination_id = graphene.Int()
    tariff = graphene.Int()

class HotelWithNameAlreadyExists(graphene.ObjectType):
    hotel_name = graphene.String()

class UpdateHotelResponse(graphene.Union):
    class Meta:
        types = (Hotel,UserNotAuthorized, TariffNotValid,DestinationNotFound, HotelWithNameAlreadyExists)


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

