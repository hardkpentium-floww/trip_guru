import graphene


class Hotel(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    tariff = graphene.Int()
    image_urls = graphene.List(graphene.String)
    destination_id = graphene.Int()

class GetHotelParams(graphene.InputObjectType):
    id = graphene.String(required=True)

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

