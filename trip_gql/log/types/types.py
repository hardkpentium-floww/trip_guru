import graphene

from trip_gql.common_errors import DestinationNotFound, UserNotAuthorized


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
    user_id = graphene.String()
    tags = graphene.List(graphene.String)

class LoginParams(graphene.InputObjectType):
    phone_no = graphene.String(required=True)

class LogoutParams(graphene.InputObjectType):
    user_id = graphene.String(required=True)

class AuthenticationResponse(graphene.ObjectType):
    access_token = graphene.String()
    refresh_token = graphene.String()
    token_type = graphene.String()
    scope = graphene.String()
    expires_in = graphene.Int()

class LoggedOutUser(graphene.ObjectType):
    user_id = graphene.String()

class LogoutResponse(graphene.Union):
    class Meta:
        types = (LoggedOutUser,)

class LoginResponse(graphene.Union):
    class Meta:
        types = (AuthenticationResponse, UserNotAuthorized)

class AddDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination,UserNotAuthorized)


class UpdateDestinationParams(graphene.InputObjectType):
    destination_id = graphene.Int()
    name = graphene.String()
    description = graphene.String()
    user_id = graphene.String()
    tags = graphene.List(graphene.String)

class UpdateDestinationResponse(graphene.Union):
    class Meta:
        types = (Destination,UserNotAuthorized, DestinationNotFound)

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
