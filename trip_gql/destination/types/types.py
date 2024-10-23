import graphene

class Destination(graphene.ObjectType):
    destination_id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    user_id = graphene.Int()
    tags = graphene.List(graphene.String)


class AddDestinationParams(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    user_id = graphene.String()
    tags = graphene.List(graphene.String)


class InvalidUser(graphene.ObjectType):
    user_id = graphene.String()

class AddDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination,InvalidUser)

class DestinationNotFound(graphene.ObjectType):
    destination_id = graphene.Int()

class UpdateDestinationParams(graphene.InputObjectType):
    destination_id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    user_id = graphene.String()
    tags = graphene.List(graphene.String)

class UpdateDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination,InvalidUser, DestinationNotFound)

class GetDestinationParams(graphene.InputObjectType):
    destination_id = graphene.Int()

class GetDestinationsParams(graphene.InputObjectType):
    tag = graphene.String()
    offset = graphene.Int()
    limit = graphene.Int()

class GetDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination,DestinationNotFound)

class GetDestinationsResponse(graphene.Union):
    class Meta:
        types = (graphene.List(Destination),DestinationNotFound)
