import graphene

class Destination(graphene.ObjectType):
    destination_id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    user_id = graphene.Int()
    tags = graphene.List(graphene.String)

class GetDestinationParams(graphene.InputObjectType):
    destination_id = graphene.Int()

class GetDestinationsParams(graphene.InputObjectType):
    tag = graphene.String()
    offset = graphene.Int()
    limit = graphene.Int()


class DestinationNotFound(graphene.ObjectType):
    destination_id = graphene.Int()


class GetDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination,DestinationNotFound)

class GetDestinationsResponse(graphene.Union):
    class Meta:
        types = (graphene.List(Destination),DestinationNotFound)
