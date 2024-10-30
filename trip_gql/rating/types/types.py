import graphene

from trip_gql.common_errors import UserNotAuthorized, DestinationNotFound


class Rating(graphene.ObjectType):
    rating_id = graphene.Int()
    user_id = graphene.String()
    destination_id = graphene.Int()
    rating = graphene.Float()
    review = graphene.String()


class AddRatingParams(graphene.InputObjectType):
    destination_id = graphene.Int()
    rating = graphene.Float()
    review = graphene.String()

class RatingNotValid(graphene.ObjectType):
    rating = graphene.Float()

class AddRatingResponse(graphene.Union):
    class Meta:
        types = (Rating,DestinationNotFound,UserNotAuthorized, RatingNotValid)

