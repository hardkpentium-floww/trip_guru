import graphene

from trip_gql.common_errors import DestinationNotFound, UserNotAuthorized, UserNotAdmin


class Destination(graphene.ObjectType):
    id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    user_id = graphene.String()
    tags = graphene.String()


class Destinations(graphene.ObjectType):
    destinations = graphene.List(Destination)



class AddDestinationParams(graphene.InputObjectType):
    name = graphene.String()
    description = graphene.String()
    tags = graphene.String()



class AddDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination,UserNotAdmin)

class UpdateDestinationParams(graphene.InputObjectType):
    destination_id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    user_id = graphene.String()
    tags = graphene.String()

class UpdateDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination, UserNotAuthorized, DestinationNotFound)

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
        types = (Destinations,DestinationNotFound)


